import asyncio
from concurrent.futures import ThreadPoolExecutor
import functools
from os import path
import os
from pathlib import Path
from typing import Any, Callable, Generator, List, Optional, Protocol
import requests

from simple_proxy3.tools.simple_timer import SimpleTimer
from simple_proxy3.tools.random_user_agent import get_random as random_agent

from .proxy_pool import ProxyPool
from .proxy_info import ProxyInfo


LINE_SEPARATER = ' '


class ProxiedSessionCall(Protocol):
    def __call__(self, session: requests.Session, *args, **kwargs) -> Any:
        ...


class ProxyManager:
    def __init__(self,
                 test_url='https://www.google.com/',
                 concurrent_trials_per_session=32,
                 verbose=False,
                 new_session_fn=lambda: requests.Session()):
        self._test_url = test_url
        self._concurrent_trials_per_session = concurrent_trials_per_session
        self._verbose = verbose
        self._new_session_fn = new_session_fn

        self._executor = None
        self._pool = None
        self._started = False

        self._running_futures = set()

    def _load_from_file(self, folder: Path, files: List, extension: str) -> Generator[ProxyInfo, None, None]:
        for file in files:
            protocol = file
            file = path.join(folder, file + extension)
            if not path.exists(file):
                continue

            with open(file, 'r') as f:
                for row in f:
                    row = row.strip()
                    if not row or len(row) == 0:
                        continue

                    row = row.split(LINE_SEPARATER)
                    if len(row) < 1:
                        continue

                    yield ProxyInfo.from_row(protocol, row)

    async def load(self,
                   folder: Path = Path('./proxies'),
                   files=['http', 'https', 'socks4', 'socks5'],
                   extension='.txt',
                   loader: Generator[ProxyInfo, None, None] = None):
        """
        Load proxies from files in a folder.
        Each file must have name and extension as specified in the parameters.
        The format is following: <ip>:<port> [response_time] [fails]
          where square brackets are optional.

        :param folder: folder to load proxies from
        :param files: list of file names to load proxies from
        :param extension: extension of the files
        :param loader: function to load proxies from a file. If not None, it will be used
            instead of the specified files.
        :return: list of proxies
        """
        if loader is None:
            loader = self._load_from_file(folder, files, extension)

        infos = []
        for info in loader:
            infos.append(info)

        self._pool = ProxyPool(infos)

    async def save(self, folder: Path = Path('./proxies'), extension='.txt'):
        """
        Save proxies to files in a folder.

        :param folder: folder to save proxies to
        :param extension: extension of the files
        :return: None
        """
        proxy_dict = await self._pool.to_dict()

        for protocol, proxy_arr in proxy_dict.items():
            with open(path.join(folder, protocol + extension + ".tmp"), 'w') as f:
                for each_arr in proxy_arr:
                    f.write(LINE_SEPARATER.join(each_arr))
                    f.write('\n')
            os.rename(path.join(folder, protocol + extension + ".tmp"),
                      path.join(folder, protocol + extension))

    async def start(self):
        assert self._pool is not None, "ProxyManager must be loaded before starting"
        await self._pool.start()
        self._executor = ThreadPoolExecutor(
            max_workers=self._concurrent_trials_per_session)
        self._started = True

    async def stop(self):
        self._executor.shutdown(wait=True, cancel_futures=True)
        await self._pool.stop()
        self._started = False

    async def run_with_proxy(self,
                             fn: Callable[[ProxiedSessionCall], Optional[Any]],
                             callback_async: Callable[[
                                 Optional[Any]], None] = lambda x: None,
                             args: tuple = (),
                             kwargs: dict = {},
                             on_exc: Callable[[ProxyInfo | None, Exception],
                                              None] = lambda info, ex: print(info, ex),
                             block: bool = True):
        """
        Run a function with a requests Session wrapped with the randomly selected proxy server.

        :param fn: function to run
        :param callback_async: callback function to run after the function is finished
        :param args: arguments to pass to the function
        :param kwargs: keyword arguments to pass to the function
        :param on_exc: callback function to run when an exception is raised
        :param block: whether to block the current thread until the function is finished.
            setting this to False will return immediately, and the result will be passed to
            the callback_async function.
        """

        assert self._pool is not None, "ProxyManager is not initialized. Use load() first."
        assert self._pool._started, "ProxyManager is not running. Use start() (or context manager) first."

        loop = asyncio.get_running_loop()

        # event to keep track of concurrent trials and set to true when at least one trial is successful
        end_event = asyncio.Event()
        kwargs['end_event'] = end_event

        async def concurrent_trial_fn():
            success = False
            result_future = None

            # retry indefinitely until success or other task already succeeded
            while not end_event.is_set() and not success:
                async with await self._pool.poll() as proxy:
                    # create new session with the proxy
                    session = self._new_session_fn()
                    session.proxies.update(proxy.info.as_requests_dict())
                    session.headers.update({'user-agent': random_agent()})

                    timer = SimpleTimer()
                    try:
                        timer.start()

                        # keep monitor the end event so that we can stop the task
                        #   early if other task already succeeded
                        result_future = loop.run_in_executor(self._executor,
                                                             functools.partial(fn, session, *args, **kwargs))
                        # keep this future so that if 'concurrent_trial_fn' is cancelled,
                        #   we can cancel the running task at the end
                        self._running_futures.add(result_future)

                        while not result_future.done():
                            await asyncio.sleep(0)
                            if end_event.is_set():
                                result_future.cancel()
                                return None

                        result = await result_future

                        # end of the task
                        timer.stop()
                        session.close()
                        success = True

                        if block:
                            # return to the waiting thread
                            return result
                        else:
                            # return result to the callback function
                            if type(result) is tuple:
                                callback_async(*result)
                            else:
                                callback_async(result)

                    except Exception as exc:
                        on_exc(proxy.info, exc)

                        # retry if the task failed
                        if end_event.is_set():
                            break

                        continue
                    finally:
                        # delete future
                        self._running_futures.remove(result_future)

                        # update proxy response time
                        await proxy.response(timer.time_elapsed())

        # schedule concurrent trials
        futures = [asyncio.create_task(concurrent_trial_fn())
                   for _ in range(self._concurrent_trials_per_session)]

        # wait until at least one trial is successful
        done, pending = await asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
        while len(done) < 1:
            done, pending = await asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
        end_event.set()

        # cancel all pending tasks
        for future in pending:
            if not future.done():
                future.cancel()

        # wait for cancelled tasks and handle exceptions
        for future in self._running_futures:
            if not future.done():
                future.cancel()

            try:
                await future
            except asyncio.CancelledError:
                # ignore cancelled error
                continue
            except Exception as exc:
                on_exc(None, exc)
                continue

        self._running_futures = set()

        # return the result of the successful task
        return await next(iter(done))

    def __enter__(self):
        raise NotImplementedError("Use 'async with' instead")

    async def __aenter__(self):
        await self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError("Use 'async with' instead")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

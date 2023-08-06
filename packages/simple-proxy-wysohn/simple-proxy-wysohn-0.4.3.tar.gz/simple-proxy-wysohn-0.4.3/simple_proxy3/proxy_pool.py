from asyncio import PriorityQueue
import asyncio
from typing import Coroutine, List
from .proxy import Proxy

from .proxy_info import ProxyInfo


class ProxyPool:
    def __init__(self, proxy_infos: List[ProxyInfo]):
        self._pool = PriorityQueue()

        self._started = False
        # these info are surrogates for proxies so do not alter the list
        self._proxy_infos = proxy_infos

    async def _init_proxy(self, proxy_infos: List[ProxyInfo]):
        assert len(
            proxy_infos) > 0, "At least one proxy must exist for ProxyPool to work properly."

        futures = []
        for info in proxy_infos:
            proxy = Proxy(info=info)
            proxy.register_observer(self)

            futures.append(asyncio.create_task(self._pool.put(proxy)))

        await asyncio.gather(*futures)

    async def notify(self, proxy: Proxy):
        await self._pool.put(proxy)
        self._pool.task_done()

    async def start(self):
        await self._init_proxy(self._proxy_infos)

        self._started = True

    async def stop(self):
        self._started = False

    async def poll(self) -> Proxy:
        return await self._pool.get()

    async def to_dict(self) -> dict:
        assert not self._started, "ProxyPool must be stopped before saving."

        file_dict = {}
        for info in self._proxy_infos:
            if info.protocol not in file_dict:
                file_dict[info.protocol] = []

            file_dict[info.protocol].append(info.as_row())

        return file_dict

    async def __aenter__(self):
        await self.start()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

import asyncio
from multiprocessing.spawn import prepare
from pathlib import Path
import unittest

import pytest
from requests import Session
from simple_proxy3.proxy_info import ProxyInfo

from simple_proxy3.proxy_manager import ProxyManager


@pytest.fixture
def prepare_files(tmp_path: Path):
    file_content_http = """
        1.1.1.1:80
        1.1.1.2:80 0.3 6

        1.1.1.3:80
        """
    file_content_https = """
        2.1.1.1:500

        2.1.1.2:600
        """
    file_content_socks4 = """

        3.1.1.1:700
        """
    file_content_socks5 = """
        4.1.1.1:800

        """

    http_file = tmp_path / "http.txt"
    https_file = tmp_path / "https.txt"
    socks4_file = tmp_path / "socks4.txt"
    socks5_file = tmp_path / "socks5.txt"

    http_file.write_text(file_content_http)
    https_file.write_text(file_content_https)
    socks4_file.write_text(file_content_socks4)
    socks5_file.write_text(file_content_socks5)

    return tmp_path


@pytest.fixture
def prepare_folder_only(tmp_path: Path):
    return tmp_path


@pytest.mark.asyncio
async def test_proxy_manager_load(prepare_files):
    tmp_path = prepare_files

    # Arrange
    manager = ProxyManager()

    # Act
    await manager.load(tmp_path)

    # Assert
    assert len(manager._pool._proxy_infos) == 7
    assert manager._pool._proxy_infos[0].protocol == "http"
    assert manager._pool._proxy_infos[0].ip_addr == "1.1.1.1:80"
    assert manager._pool._proxy_infos[0].response_rate == 999.0
    assert manager._pool._proxy_infos[0].fails == 0

    assert manager._pool._proxy_infos[1].protocol == "http"
    assert manager._pool._proxy_infos[1].ip_addr == "1.1.1.2:80"
    assert manager._pool._proxy_infos[1].response_rate == 0.3
    assert manager._pool._proxy_infos[1].fails == 6

    assert manager._pool._proxy_infos[2].protocol == "http"
    assert manager._pool._proxy_infos[2].ip_addr == "1.1.1.3:80"
    assert manager._pool._proxy_infos[2].response_rate == 999.0
    assert manager._pool._proxy_infos[2].fails == 0

    assert manager._pool._proxy_infos[3].protocol == "https"
    assert manager._pool._proxy_infos[3].ip_addr == "2.1.1.1:500"
    assert manager._pool._proxy_infos[3].response_rate == 999.0
    assert manager._pool._proxy_infos[3].fails == 0

    assert manager._pool._proxy_infos[4].protocol == "https"
    assert manager._pool._proxy_infos[4].ip_addr == "2.1.1.2:600"
    assert manager._pool._proxy_infos[4].response_rate == 999.0
    assert manager._pool._proxy_infos[4].fails == 0

    assert manager._pool._proxy_infos[5].protocol == "socks4"
    assert manager._pool._proxy_infos[5].ip_addr == "3.1.1.1:700"
    assert manager._pool._proxy_infos[5].response_rate == 999.0
    assert manager._pool._proxy_infos[5].fails == 0

    assert manager._pool._proxy_infos[6].protocol == "socks5"
    assert manager._pool._proxy_infos[6].ip_addr == "4.1.1.1:800"
    assert manager._pool._proxy_infos[6].response_rate == 999.0
    assert manager._pool._proxy_infos[6].fails == 0


@pytest.mark.asyncio
async def test_proxy_manager_save(prepare_folder_only):
    tmp_path = prepare_folder_only

    # Arrange
    def loader():
        L = [
            ProxyInfo('http', '1.1.1.1:80', 999.0, 0),
            ProxyInfo('http', '1.1.1.2:80', 0.3, 6),
            ProxyInfo('http', '1.1.1.3:80', 999.0, 0),
            ProxyInfo('https', '2.1.1.1:500', 999.0, 0),
            ProxyInfo('https', '2.1.1.2:600', 999.0, 0),
            ProxyInfo('socks4', '3.1.1.1:700', 999.0, 0),
            ProxyInfo('socks5', '4.1.1.1:800', 999.0, 0)
        ]

        for each in L:
            yield each

    manager = ProxyManager()
    await manager.load(loader=loader())

    # Act
    await manager.save(tmp_path)

    # Assert
    assert (tmp_path / "http.txt").exists()
    assert (tmp_path / "https.txt").exists()
    assert (tmp_path / "socks4.txt").exists()
    assert (tmp_path / "socks5.txt").exists()

    A = (tmp_path / "http.txt").read_text()
    B = """1.1.1.1:80 999.0 0\n1.1.1.2:80 0.3 6\n1.1.1.3:80 999.0 0\n"""

    assert (tmp_path / "http.txt").read_text(
    ) == """1.1.1.1:80 999.0 0\n1.1.1.2:80 0.3 6\n1.1.1.3:80 999.0 0\n"""
    assert (tmp_path / "https.txt").read_text() == """2.1.1.1:500 999.0 0\n2.1.1.2:600 999.0 0\n"""
    assert (tmp_path / "socks4.txt").read_text() == """3.1.1.1:700 999.0 0\n"""
    assert (tmp_path / "socks5.txt").read_text() == """4.1.1.1:800 999.0 0\n"""


@pytest.mark.asyncio
async def test_proxy_manager_run_with_proxy():
    # Arrange
    exceptions = asyncio.queues.Queue()
    exceptions.put_nowait(Exception("test"))
    exceptions.put_nowait(Exception("test2"))
    exceptions.put_nowait(Exception("test3"))
    exceptions.put_nowait(Exception("test4"))
    exceptions.put_nowait(Exception("test5"))
    exceptions.put_nowait(Exception("test6"))
    exceptions.put_nowait(Exception("test7"))
    exceptions.put_nowait(Exception("test8"))
    exceptions.put_nowait(Exception("test9"))
    exceptions.put_nowait(Exception("test10"))

    def loader():
        L = [ProxyInfo.localhost()]

        for each in L:
            yield each

    manager = ProxyManager(concurrent_trials_per_session=4)
    await manager.load(loader=loader())

    def fn(session: Session, end_event: asyncio.Event):
        if end_event.is_set():
            return

        if not exceptions.empty():
            raise exceptions.get_nowait()

        result = session.get("https://httpbin.org/ip")
        return result

    # Act
    async with manager as proxy_manager:
        result = await proxy_manager.run_with_proxy(fn)

    # Assert
    assert result.status_code == 200
    assert 'origin' in result.json()

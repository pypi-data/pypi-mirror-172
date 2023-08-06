import unittest

import pytest
from simple_proxy3.proxy_info import ProxyInfo

from simple_proxy3.proxy_pool import ProxyPool


@pytest.mark.asyncio
async def test_proxy_pool_init():
    # Arrange
    pool = ProxyPool([ProxyInfo("http", "1.2.3.4:8008")])
    # Act
    await pool.start()
    # Assert
    assert pool._pool.get_nowait() is not None

    await pool.stop()


@pytest.mark.asyncio
async def test_proxy_pool_context_manager():
    # Arrange
    pool = ProxyPool([ProxyInfo("http", "3.4.5.6:8080")])
    # Act
    async with pool as p:
        # Assert
        assert p._started
        assert p._pool.get_nowait() is not None

    assert not pool._started


@pytest.mark.asyncio
async def test_proxy_pool_poll():
    # Arrange
    proxy_list = [ProxyInfo("http", "1.1.1.1:5005"),
                  ProxyInfo("https", "2.2.2.2:6006"),
                  ProxyInfo("socks4", "3.3.3.3:7007"),
                  ProxyInfo("socks5", "4.4.4.4:8008")]

    pool = ProxyPool(proxy_list)
    # Act
    await pool.start()

    # 1.1.1.1 fails 10 times
    # 2.2.2.2 fails 7 times
    # 3.3.3.3 fails 9 times
    # 4.4.4.4 fails 8 times
    for i in range(len(proxy_list)):
        proxy = await pool.poll()
        async with proxy as p:
            await p.fail(10 - i)

    # Assert
    proxy = await pool.poll()
    assert proxy.info == proxy_list[1]
    proxy = await pool.poll()
    assert proxy.info == proxy_list[3]
    proxy = await pool.poll()
    assert proxy.info == proxy_list[2]
    proxy = await pool.poll()
    assert proxy.info == proxy_list[0]

    await pool.stop()


@pytest.mark.asyncio
async def test_proxy_pool_poll2():
    # Arrange
    proxy_list = [ProxyInfo("http", "1.1.1.1:5005"),
                  ProxyInfo("https", "2.2.2.2:6006"),
                  ProxyInfo("socks4", "3.3.3.3:7007"),
                  ProxyInfo("socks5", "4.4.4.4:8008")]

    pool = ProxyPool(proxy_list)
    # Act
    await pool.start()

    # 1.1.1.1 response time 2000.0
    # 2.2.2.2 response time 1997.0
    # 3.3.3.3 response time 1999.0
    # 4.4.4.4 response time 1998.0
    for i in range(len(proxy_list)):
        proxy = await pool.poll()
        async with proxy as p:
            await p.response(2000.0 - i)

    # Assert
    proxy = await pool.poll()
    assert proxy.info == proxy_list[1]
    proxy = await pool.poll()
    assert proxy.info == proxy_list[3]
    proxy = await pool.poll()
    assert proxy.info == proxy_list[2]
    proxy = await pool.poll()
    assert proxy.info == proxy_list[0]

    await pool.stop()


@pytest.mark.asyncio
async def test_proxy_pool_to_dict():
    # Arrange
    proxy_list = [ProxyInfo("http", "1.1.1.1:5005"),
                  ProxyInfo("https", "2.2.2.2:6006"),
                  ProxyInfo("https", "2.2.2.3:6006"),
                  ProxyInfo("socks4", "3.3.3.3:7007"),
                  ProxyInfo("socks5", "4.4.4.4:8008")]

    pool = ProxyPool(proxy_list)

    # Act
    await pool.start()

    # 1.1.1.1 fails 10 times
    # 2.2.2.2 fails 7 times
    # 2.2.2.3 fails 9 times
    # 3.3.3.3 fails 6 times
    # 4.4.4.4 fails 8 times
    for i in range(len(proxy_list)):
        proxy = await pool.poll()
        async with proxy as p:
            await p.fail(10 - i)

    await pool.stop()

    # Assert
    assert await pool.to_dict() == {
        "http": [["1.1.1.1:5005", '999.0', '10']],
        "https": [["2.2.2.2:6006", '999.0', '7'], ["2.2.2.3:6006", '999.0', '9']],
        "socks4": [["3.3.3.3:7007", '999.0', '6']],
        "socks5": [["4.4.4.4:8008", '999.0', '8']]
    }

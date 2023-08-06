
import unittest

import pytest

from simple_proxy3.proxy import Proxy


@pytest.mark.asyncio
async def test_proxy_eq():
    # Arrange
    proxy1 = Proxy(protocol='http', ip_addr='1.2.3.4:8808')
    proxy2 = Proxy(protocol='http', ip_addr='4.5.6.6:8808')
    proxy3 = Proxy(protocol='http', ip_addr='8.8.7.8:8808')
    proxy4 = Proxy(protocol='http', ip_addr='9.9.9.9:5500')

    # Act
    await proxy1.fail()
    await proxy2.fail()
    await proxy3.fail()
    await proxy3.fail()

    await proxy1.response(0.1)
    await proxy2.response(0.1)
    await proxy4.response(2.3)

    # Assert
    assert proxy1 == proxy2
    assert proxy1 != proxy3
    assert proxy1 != proxy4
    assert proxy2 != proxy3
    assert proxy2 != proxy4
    assert proxy3 != proxy4


@pytest.mark.asyncio
async def test_proxy_lt():
    # Arrange
    proxy1 = Proxy(protocol='http', ip_addr='5.4.3.2:8808')
    proxy2 = Proxy(protocol='http', ip_addr='2.3.4.5:8808')

    # Act
    await proxy1.fail()
    await proxy2.fail()
    await proxy2.fail()

    await proxy1.response(0.1)
    await proxy2.response(0.1)

    # Assert
    assert proxy1 < proxy2


@pytest.mark.asyncio
async def test_proxy_lt2():
    # Arrange
    proxy1 = Proxy(protocol='http', ip_addr='5.4.3.2:8808')
    proxy2 = Proxy(protocol='http', ip_addr='2.3.4.5:8808')

    # Act
    await proxy1.fail()
    await proxy2.fail()

    await proxy1.response(3.4)
    await proxy2.response(0.1)

    # Assert
    assert proxy1 > proxy2


@pytest.mark.asyncio
async def test_context_manager():
    # Arrange
    class TempObservber:
        def __init__(self):
            self._called = False

        async def notify(self, observable):
            self._called = True

    proxy = Proxy(protocol='http', ip_addr='4.5.3.4:8808')
    observer = TempObservber()
    proxy.register_observer(observer)

    # Act
    async with proxy as p:
        await p.response(0.1)
        raise Exception('Test exception')

    # Assert
    assert observer._called
    assert proxy.info.fails == 1


def test_repr():
    # Arrange
    proxy = Proxy(protocol='http', ip_addr='4.3.2.3:9090')

    # Act
    result = str(proxy)

    # Assert
    assert result == 'Proxy(http://4.3.2.3:9090, 999.0, 0)'

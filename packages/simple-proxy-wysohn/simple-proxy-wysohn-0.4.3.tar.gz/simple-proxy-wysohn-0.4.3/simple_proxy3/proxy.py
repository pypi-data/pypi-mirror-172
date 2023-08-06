import os

from .observables.observable import Observable
from .proxy_info import ProxyInfo


RESPONSE_RATE_MAX = float(os.getenv('RESPONSE_RATE_MAX', 10000.0))
PROXY_ORDER_ALPHA = float(os.getenv('PROXY_ORDER_ALPHA', 0.2))
PROXY_ORDER_BETA = float(os.getenv('PROXY_ORDER_BETA', 1.0))


class Proxy(Observable):
    def __init__(self, info: ProxyInfo = None, protocol: str = None, ip_addr: str = None):
        super().__init__()

        self.info = info
        if info is None and protocol != None and ip_addr != None:
            self.info = ProxyInfo(protocol, ip_addr)
        assert self.info is not None

    async def fail(self, count=1):
        self.info.fails = self.info.fails + count

    async def response(self, response_time: float):
        assert response_time >= 0.0, "Response time must be non-negative."
        self.info.response_rate = response_time

    def order(self):
        return PROXY_ORDER_BETA * self.info.fails + PROXY_ORDER_ALPHA * self.info.response_rate / RESPONSE_RATE_MAX

    def __eq__(self, other):
        this_order = self.order()
        other_order = other.order()

        return this_order == other_order

    def __lt__(self, other):
        this_order = self.order()
        other_order = other.order()

        return this_order < other_order

    def __enter__(self):
        raise NotImplementedError("Use async with.")

    async def __aenter__(self):
        assert len(self.observers) > 0, "No observers found."

        return self

    def __exit__(self):
        raise NotImplementedError("Use async with.")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                await self.fail()
        finally:
            await self._notify_observers()
            return True

    def __repr__(self):
        return f'Proxy({self.info})'

from typing import List

from .observables.observable import Observable


class ProxyInfo(Observable):
    def from_row(protocol: str, row: List[str]):
        return ProxyInfo(protocol,
                         row[0],
                         row[1] if len(row) > 1 else 999.0,
                         row[2] if len(row) > 2 else 0)

    def localhost():
        return ProxyInfo('localhost', 'localhost', 0.0, 0)

    def __init__(self, protocol, ip_addr, response_rate=None, fails=None) -> None:
        self.protocol = protocol
        self.ip_addr = ip_addr
        self.response_rate = float(
            response_rate) if response_rate is not None else 999.0
        self.fails = int(fails) if fails is not None else 0

    def as_requests_dict(self) -> dict:
        if self.protocol == 'localhost':
            return {}

        proto = 'http' if self.protocol == 'https' else self.protocol
        formatted_host = "{}://{}".format(proto, self.ip_addr)
        return {'https': formatted_host}

    def as_row(self) -> List[str]:
        return [self.ip_addr, str(self.response_rate), str(self.fails)]

    def __repr__(self):
        return '{}://{}, {}, {}'.format(self.protocol, self.ip_addr, self.response_rate, self.fails)

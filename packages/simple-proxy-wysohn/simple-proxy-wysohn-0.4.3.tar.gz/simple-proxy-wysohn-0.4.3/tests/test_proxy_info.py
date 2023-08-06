import unittest


import unittest

from simple_proxy3.proxy_info import ProxyInfo


def test_proxy_info_http():
    # Arrange
    protocol = 'http'
    ip_addr = '1.2.3.4:8080'
    info = ProxyInfo(protocol, ip_addr)

    # Act
    result = info.as_requests_dict()

    # Assert
    for key, val in result.items():
        assert 'http://1.2.3.4:8080' == val


def test_proxy_info_https():
    # Arrange
    protocol = 'https'
    ip_addr = '1.2.3.4:8080'
    info = ProxyInfo(protocol, ip_addr)

    # Act
    result = info.as_requests_dict()

    # Assert
    for key, val in result.items():
        assert 'http://1.2.3.4:8080' == val


def test_proxy_info_repr():
    # Arrange
    protocol = 'socks5'
    ip_addr = '4.3.2.1:5050'
    info = ProxyInfo(protocol, ip_addr)

    # Act
    result = str(info)

    # Assert
    assert 'socks5://4.3.2.1:5050, 999.0, 0' == result

from socket import getaddrinfo, AddressFamily
from sys import stderr
from typing import List, Tuple, Optional
from urllib.parse import urlparse, urlunparse, ParseResult

from requests import Response

from .store import store

default_scheme = 'http'


def err(*args):
    if store().allow_error_messages:
        print(*args, file=stderr)


def scheme2port(scheme: str) -> int:
    if scheme == 'https' or scheme == '':  # https as default
        return 443
    if scheme == 'http':
        return 80
    raise RuntimeError('Scheme not supported')


def host2ip(r: ParseResult) -> Tuple[List[str], List[str]]:
    port = r.port or scheme2port(r.scheme)
    info = getaddrinfo(r.hostname, port)
    ipv4 = []
    ipv6 = []
    for ip in info:
        _ip = ip[-1][0]
        if ip[0] == AddressFamily.AF_INET and _ip not in ipv4:
            ipv4.append(_ip)
        elif ip[0] == AddressFamily.AF_INET6 and _ip not in ipv6:
            ipv6.append(_ip)
    return ipv4, ipv6


def normalize_url(url):
    result = urlparse(url)

    scheme = result.scheme
    path = result.path
    netloc = result.netloc
    query = result.query
    fragment = result.fragment
    params = result.params

    if '' == scheme:
        err('Scheme has empty. Use default (%s)\n' % default_scheme)
        scheme = default_scheme

    if '' == netloc:
        netloc = result.path
        path = ''

    return urlunparse((scheme, netloc, path, params, query, fragment))


def get_response_redirect_url(response: Response) -> Optional[str]:
    if 300 <= response.status_code < 400:
        return response.headers['location']
    return None


def cookies2dict(cookies: List[str]):
    _c = {}
    for c in cookies:
        key, value = c.split('=')
        _c[key] = value
    return _c

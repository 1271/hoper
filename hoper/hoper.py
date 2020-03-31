from socket import getaddrinfo, AddressFamily
from sys import stderr
from time import time
from typing import List, Tuple, NamedTuple, Optional
from urllib.parse import urlparse, urlunparse, ParseResult

from requests import request, Response
from requests.exceptions import *
from requests.utils import default_headers

from .args import arguments

Hope = NamedTuple('Hope', url=str, status=int, time=float)

default_scheme = 'http'
allow_error_messages = True


def err(*args):
    if allow_error_messages:
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


def cookies2dict(cookies: List[str]):
    _c = {}
    for c in cookies:
        key, value = c.split('=')
        _c[key] = value
    return _c


def get_response_redirect_url(response: Response) -> Optional[str]:
    if 300 <= response.status_code < 400:
        return response.headers['location']
    return None


def hope(url: str, **kwargs) -> Tuple[Response, Optional[str], float]:
    start_time = time()
    kwargs.setdefault('method', 'get')
    response = request(
        url=url,
        allow_redirects=False,
        stream=True,
        **kwargs,
    )
    return response, get_response_redirect_url(response), time() - start_time


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


def get_history(
        url: str, user_agent: str,
        cookies: dict, timeout: Optional[int] = None,
        use_post: bool = False
) -> List[Tuple[str, int, float]]:
    """
    :return: url, status, request_time
    """

    headers = default_headers()
    headers['User-Agent'] = user_agent
    _url = normalize_url(url)

    kwargs = {
        'headers': headers,
        'cookies': cookies,
        'timeout': timeout,
    }

    if use_post:
        kwargs['method'] = 'post'

    while _url is not None:
        response, _url, request_time = hope(
            url=_url,
            **kwargs
        )
        item = (response.url, response.status_code, request_time)
        response.close()
        yield item


def print_item(item: Tuple[str, int, float], show_ip: bool, show_time: bool):
    info = 'Hope:\t%s\nStatus:\t%i\n' % item[:-1]
    if show_time:
        info += 'Time:\t%0.2f\n' % item[-1]

    if show_ip:
        r = urlparse(item[0])
        ipv4, ipv6 = host2ip(r)
        for ip in ipv4:
            info += 'Ip4:\t%s\n' % ip
        for ip in ipv6:
            info += 'Ip6:\t%s\n' % ip

    print(info, end='')


def main():
    _args = arguments.parse_args()

    global allow_error_messages
    allow_error_messages = not _args.no_error_messages

    try:
        history = get_history(
            _args.url,
            _args.user_agent,
            cookies2dict(_args.cookies),
            _args.timeout
        )

        hops = 0
        for i, item in enumerate(history):
            i > 0 and print('')
            print_item(item, _args.show_ip, _args.show_request_time)
            hops = i

        if hops > 0 and not _args.no_statistic:
            print('\nRedirects for url %s: %d' % (_args.url, hops))

    except RuntimeError as e:
        err(e.args[0] if len(e.args) else 'Internal error')
        exit(1)

    except RequestException as e:
        err('Request error in class: {}'.format(e.__class__.__name__))
        exit(1)

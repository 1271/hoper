from sys import stderr
from urllib.parse import urlparse

from ._store import store
from ._types import Hope
from ._utils import host2ip


def err(*args):
    if store().allow_error_messages:
        print(*args, file=stderr)


def scheme2port(scheme: str) -> int:
    if scheme == 'https' or scheme == '':  # https as default
        return 443
    if scheme == 'http':
        return 80
    raise RuntimeError('Scheme not supported')


def print_item(item: Hope):
    info = 'Hope:\t%s\nStatus:\t%i\n' % (item.url, item.status)

    if store().args.try_js:
        info += 'Js: %s\n' % ('True' if 'js' == item.type else 'False')

    if store().args.show_request_time:
        info += 'Time:\t%0.2f\n' % item.time

    if store().args.show_ip:
        r = urlparse(item.url)
        ipv4, ipv6 = host2ip(r)
        for ip in ipv4:
            info += 'Ip4:\t%s\n' % ip
        for ip in ipv6:
            info += 'Ip6:\t%s\n' % ip

    print(info, end='')

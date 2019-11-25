from sys import stderr
from typing import List, Tuple
from urllib.parse import urlparse

from requests import request, Response
from requests.exceptions import *
from requests.utils import default_headers
import socket

from .args import arguments
from .meta import version


ips = {}


def host2ip(host: str) -> str:
    if host in ips:
        return ips[host]
    ip = socket.gethostbyname(host)
    ips.setdefault(host, ip)
    return ip


def cookies2dict(cookies: List[str]):
    _c = {}
    for c in cookies:
        key, value = c.split('=')
        _c[key] = value
    return _c


def get_history(url: str, user_agent: str, cookies: dict) -> List[Tuple[str, int]]:
    headers = default_headers()
    headers['User-Agent'] = user_agent
    result = urlparse(url)
    if '' == result.scheme:
        raise RuntimeError('Scheme has empty')
    response = request(
        method='head',
        headers=headers,
        cookies=cookies,
        url=url,
        allow_redirects=True
    )  # type: Response
    history = response.history  # type: List[Response]
    history.append(response)
    return [(i.url, i.status_code) for i in history]


def main():
    _args = arguments.parse_args()

    try:
        history = get_history(_args.url, _args.user_agent, cookies2dict(_args.cookies))
        if not len(history):
            raise RuntimeError('History empty')
        else:
            for i, item in enumerate(history):
                if i:
                    print('')
                print('Hop:\t%s\n Status:\t%i' % item)
                if _args.show_ip:
                    r = urlparse(item[0])
                    print(' Ip: %s' % host2ip(r.hostname))
    except RuntimeError as e:
        print(e.args[0] if len(e.args) else 'Internal error', file=stderr)
        exit(1)
    except RequestException as e:
        print('{}'.format(e.__class__.__name__), file=stderr)
        exit(1)


if __name__ == '__main__':
    main()

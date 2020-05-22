from typing import Dict, Optional

from .proxy_parser import parse_proxies
from .types import Args
from ..meta import version

__store = {}  # type: ignore


__all__ = ['store', 'Store', 'build_store']


class Store:
    __proxies: Optional[Dict[str, str]] = None
    args: Args

    def __init__(self, args: Args):
        self.args = args

    @property
    def allow_error_messages(self) -> bool:
        return not self.args.no_error_messages

    @property
    def proxies(self) -> Optional[Dict[str, str]]:
        if self.__proxies is None and self.args.proxy is not None:
            self.__proxies = parse_proxies(self.args.proxy)
        return self.__proxies


def build_store(**kwargs) -> Store:
    """
    :param str url: String url
    :param str user_agent: String user-agent
    :param list cookies: array of strings
            Format: ['key1=value1', 'key2=value2', ...]
    :param list proxy: array of strings
            Format: ['http://proxy:123'] (for http and https)
             or ['http=http://proxy:123', 'https=http://secured-proxy:321', 'ftp=http://ftp-proxy:332']
    :param bool show_ip: boolean (show ip for each host)
    :param bool timeout: int (optional). Timeout for each request (1/100 sec)
    :param bool show_request_time: Show request time for each request
    :param bool no_error_messages: Do not show any errors
    :param bool no_statistic: Do not show statistic of end
    :param bool count_only: Show requests count and exit
    :param bool try_js: Try check js redirects
    :param bool last_only: Show only last request url
    :param bool disallow_loops: Do not allow loops (url1->url2->url1-> end)

    :return:
    :rtype: Store
    """
    _ = Store(args=Args(
        user_agent=kwargs.get('user_agent', ('Python hoper: %s' % version)),
        cookies=kwargs.get('cookies', []),
        show_ip=kwargs.get('show_ip', False),
        timeout=kwargs.get('timeout'),
        show_request_time=kwargs.get('show_request_time', False),
        no_error_messages=kwargs.get('no_error_messages', False),
        no_statistic=kwargs.get('no_statistic', False),
        count_only=kwargs.get('count_only', False),
        try_js=kwargs.get('try_js', False),
        proxy=kwargs.get('proxy', None),
        last_only=kwargs.get('last_only', False),
        print_json=kwargs.get('print_json', False),
        pretty_json=kwargs.get('pretty_json'),
        disallow_loops=kwargs.get('disallow_loops', False),
        allow_hooks=kwargs.get('allow_hooks', False),
    ))
    set_store(_)
    return store()


def has_store() -> bool:
    return 'store' in __store.keys()


def set_store(_store: Store):
    __store['store'] = _store


def store() -> Store:
    return __store['store']

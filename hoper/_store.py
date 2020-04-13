from typing import Union, Dict, NamedTuple, Optional
from argparse import Namespace

from ._types import Args
from .proxy_parser import parse_proxies


_store = {}


class Store:
    __proxies: Optional[Dict] = None
    args: Args

    def __init__(self, args: Args):
        self.args = args

    @property
    def allow_error_messages(self) -> bool:
        return not self.args.no_error_messages

    @property
    def proxies(self) -> Union[Dict[str, str]]:
        if self.__proxies is None and self.args.proxy is not None:
            self.__proxies = parse_proxies(self.args.proxy)
        return self.__proxies


def build_store(args: Namespace):
    _store['store'] = Store(args=Args(
        url=args.url,
        user_agent=args.user_agent,
        cookies=args.cookies,
        show_ip=args.show_ip,
        timeout=args.timeout,
        show_request_time=args.show_request_time,
        no_error_messages=args.no_error_messages,
        no_statistic=args.no_statistic,
        # post=args.post,
        count_only=args.count_only,
        try_js=args.try_js,
        proxy=args.proxy,
        last_only=args.last_only,
        disallow_loops=args.disallow_loops,
    ))
    return _store['store']


def store() -> Store:
    return _store['store']

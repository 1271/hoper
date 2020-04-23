from json import dumps
from typing import List, Callable, Dict, Optional, Union, Iterator, Any

from requests.exceptions import *

from ._args import arguments
from ._print import print_item, err
from .util.history_util import get_history
from .util.store import build_store, store
from .util.types import Hope

MAX_LOOPS = 3
LOOP_DETECTED_MESSAGE = 'Loop detected "%s"'


class LoopDetectedError(RuntimeError):
    iterations: int = 0

    def __init__(self, message, iterations, *args):
        self.iterations = iterations
        super().__init__(message, *args)


def __iterate(history: Iterator[Hope], callback: Callable) -> int:
    urls: Dict[str, int] = {}

    hops = 0
    for i, item in enumerate(history):
        if store().args.disallow_loops and item.url in urls.keys():
            err(LOOP_DETECTED_MESSAGE % item.url)
            break

        urls.setdefault(item.url, 1)
        if item.url in urls.keys() and urls[item.url] > MAX_LOOPS:
            raise LoopDetectedError(LOOP_DETECTED_MESSAGE % item.url, i)
        urls[item.url] += 1

        callback(item, i)

        hops = i

    return hops


def __print_history(history: Iterator[Hope]):
    def _(item, i):
        if i > 0:
            print('')

        print_item(item)

    e: Optional[Union[LoopDetectedError, Exception]] = None
    try:
        hops = __iterate(history, _)
    except LoopDetectedError as _e:
        e = _e
        hops = e.iterations

    if hops > 0 and not store().args.no_statistic:
        print('\nRedirects: %d' % hops)

    if e is not None:
        raise e


def __print_json(history: Iterator[Hope]):
    items: List[Dict[str, Union[str, int, float]]] = []
    error: Optional[str] = None

    def _(item: Hope, i):
        _item = {f: getattr(item, f) for f in item._fields}
        _item['i'] = i
        items.append(_item)

    e: Optional[Union[LoopDetectedError, Exception]] = None
    try:
        __iterate(history, _)
    except LoopDetectedError as _e:
        e = _e
        error = e.args[0] if len(e.args) else 'Loop error'

    print(dumps({
        'items': items,
        'error': error,
    }, indent=(4 if store().args.pretty_json else None)))

    if e is not None:
        raise e


def __print_count(history: Iterator[Hope]):
    def _(*args):
        pass

    try:
        return print(__iterate(history, _))
    except LoopDetectedError as e:
        print(e.iterations)
        raise e


def __print_last_element(history: Iterator[Hope]):
    def _(item: Hope, *args):
        urls.append(item.url)

    urls: List[str] = []
    try:
        __iterate(history, _)
    except LoopDetectedError as e:
        print(urls[-1])
        raise e

    print(urls[-1])


def main():
    _kw = arguments.parse_args().__dict__
    url = _kw.pop('url')
    build_store(**_kw)

    if store().args.try_js:
        err('JS redirects in test mode')

    try:
        history = get_history(url)

        if store().args.count_only:
            __print_count(history)
            return

        if store().args.last_only:
            __print_last_element(history)
            return

        if store().args.print_json:
            __print_json(history)
            return

        __print_history(history)

    except RuntimeError as e:
        err(e.args[0] if len(e.args) else 'Internal error')
        exit(1)

    except RequestException as e:
        err('Request error in class: {}'.format(e.__class__.__name__))
        exit(1)

from requests.exceptions import *
from typing import List, Callable, Dict, Optional, Union, Iterator

from ._args import arguments
from ._print import print_item, err
from ._store import build_store, store
from ._utils import cookies2dict
from .history_util import get_history, Hope

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
    except LoopDetectedError as e:
        hops = e.iterations

    if hops > 0 and not store().args.no_statistic:
        print('\nRedirects for url %s: %d' % (store().args.url, hops))

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
    build_store(arguments.parse_args())

    if store().args.try_js:
        err('JS redirects in test mode')

    try:
        history = get_history(
            store().args.url,
            store().args.user_agent,
            cookies2dict(store().args.cookies),
            store().args.timeout
        )

        if store().args.count_only:
            __print_count(history)
            return

        if store().args.last_only:
            __print_last_element(history)
            return

        __print_history(history)

    except RuntimeError as e:
        err(e.args[0] if len(e.args) else 'Internal error')
        exit(1)

    except RequestException as e:
        err('Request error in class: {}'.format(e.__class__.__name__))
        exit(1)

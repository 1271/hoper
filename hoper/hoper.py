from requests.exceptions import *
from typing import List, Callable

from ._args import arguments
from ._print import print_item, err
from ._store import build_store, store
from ._utils import cookies2dict
from .history_util import get_history, Hope

MAX_LOOPS = 3
LOOP_DETECTED_MESSAGE = 'Loop detected "%s"'


def __iterate(history: List[Hope], callback: Callable) -> int:
    urls = {}

    hops = 0
    for i, item in enumerate(history):
        i > 0 and print('')

        if store().args.disallow_loops and item.url in urls.keys():
            err(LOOP_DETECTED_MESSAGE % item.url)
            break

        urls.setdefault(item.url, 1)
        if item.url in urls.keys() and urls[item.url] > MAX_LOOPS:
            raise RuntimeError(LOOP_DETECTED_MESSAGE % item.url)
        urls[item.url] += 1

        callback(item)

        hops = i

    return hops


def __print_history(history: List[Hope]):
    hops = __iterate(history, print_item)

    if hops > 0 and not store().args.no_statistic:
        print('\nRedirects for url %s: %d' % (store().args.url, hops))


def __print_count(history: List[Hope]):
    def _(*args):
        pass
    return print(__iterate(history, _))


def __print_last_element(history: List[Hope]):
    urls = []

    def _(item: Hope, *args):
        urls.append(item)

    n = __iterate(history, _)

    n > 0 and print(urls[-1])


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

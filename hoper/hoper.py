from requests.exceptions import *
from typing import List

from ._args import arguments
from ._print import print_item, err
from ._store import build_store, store
from ._utils import cookies2dict
from .history_util import get_history, Hope

MAX_LOOPS = 3


def __print_history(history: List[Hope]):
    urls = {}

    hops = 0
    for i, item in enumerate(history):
        i > 0 and print('')
        urls.setdefault(item.url, 1)
        if item.url in urls.keys() and urls[item.url] > MAX_LOOPS:
            raise RuntimeError('Loop detected')
        urls[item.url] += 1
        print_item(item)
        hops = i

    if hops > 0 and not store().args.no_statistic:
        print('\nRedirects for url %s: %d' % (store().args.url, hops))


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
            print(len([i for i in history]) - 1, end='')
            return

        if store().args.last_only:
            url = [i for i in history][-1]
            print(url.url)
            return

        __print_history(history)

    except RuntimeError as e:
        err(e.args[0] if len(e.args) else 'Internal error')
        exit(1)

    except RequestException as e:
        err('Request error in class: {}'.format(e.__class__.__name__))
        exit(1)

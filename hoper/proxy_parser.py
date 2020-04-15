from re import compile
from sys import stderr
from typing import List, Union, Dict, Optional

__all__ = ['parse_proxies']


RE = compile(r"""^(?:(?P<scheme>\w+)=)?(?P<url>\w+://.+)$""")


def parse_proxies(items: Optional[List]) -> Union[Dict[str, str]]:
    proxies: Dict[str, str] = {}
    if items is None:
        return proxies

    for i in items:
        _parsed = RE.search(i)

        if _parsed is None:
            print('Error parsing %s' % i, file=stderr)
            continue

        parsed = _parsed.groupdict()
        scheme = parsed.get('scheme', None)
        url = parsed['url']

        if scheme is None:
            proxies.setdefault('http', url)
            proxies.setdefault('https', url)
        else:
            proxies[scheme] = url

    return proxies

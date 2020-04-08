from typing import Optional

from requests import Response

import re

__all__ = ['find_js_redirect']


RE = (
    re.compile(
        r"""
        \blocation
        (?:
            (?:.href)?\s*=\s*
            (?P<quote11>")?(?P<quote12>')?
            (?P<location1>.+)
            (?(quote11)"|)(?(quote12)'|);?
        )?
        (?:
            \.(?:replace|assign)\(
                (?P<quote21>")?(?P<quote22>')?
                (?P<location2>.+)
                (?(quote21)"|)(?(quote22)'|)
            \);?
        )?
        """,
        re.X
    ),
)


def _parse_result(result) -> Optional[str]:
    if result is None:
        return None

    groups = result.groupdict()
    location = groups['location1'] or groups['location2']
    if location is None:
        return None
    return location.split(';')[0]


def find_js_redirect(response: Response) -> Optional[str]:
    if not response.headers.get('Content-Type', '').startswith('text/'):
        return

    try:
        for line in response.iter_lines():
            for i, reg in enumerate(RE):
                result = _parse_result(reg.search(line.decode()))
                if result is not None:
                    return result
    except Exception:
        pass
    return None

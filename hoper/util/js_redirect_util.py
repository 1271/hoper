import re
from typing import Optional

from requests import Response

__all__ = ['find_js_redirect']


RE = re.compile(
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
)


def _parse_result(line, js_start, js_end) -> Optional[str]:
    kwargs = {}

    if js_start is not None:
        kwargs['pos'] = js_start
    if js_end is not None:
        kwargs['endpos'] = js_end

    result = RE.search(line, **kwargs)

    if result is None:
        return None

    groups = result.groupdict()
    location = groups['location1'] or groups['location2']

    if location is not None:
        return location.split(';')[0]

    return None


def find_js_redirect(response: Response) -> Optional[str]:
    if not response.headers.get('Content-Type', '').startswith('text/'):
        return None

    is_js = False

    for line in response.iter_lines():

        js_start = None
        js_end = None
        _line = line.decode()  # type: str

        __js_start = _line.find('<script>')
        if ~__js_start:
            is_js = True
            js_start = __js_start

        __js_end = _line.find('</script>', js_start or 0)
        if ~__js_end:
            js_end = __js_end

        if is_js:
            result = _parse_result(_line, js_start, js_end)

            if result is not None:
                return result

        if ~__js_end:
            is_js = False

    return None

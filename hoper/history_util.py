from typing import List, Optional

from requests.utils import default_headers
from urllib.parse import urljoin

from ._store import store
from ._types import Hope
from ._utils import normalize_url
from .header_redirect_util import find_redirect
from .js_redirect_util import find_js_redirect


def __safe_js_redirect(response):
    try:
        return find_js_redirect(response)
    except Exception:
        return None


def get_history(
        url: str, user_agent: str,
        cookies: dict, timeout: Optional[int] = None,
        use_post: bool = False
) -> List[Hope]:
    """
    :return: url, status, request_time
    """

    headers = default_headers()
    headers['User-Agent'] = user_agent
    _url = normalize_url(url)

    kwargs = {
        'headers': headers,
        'cookies': cookies,
        'timeout': (timeout * 10 if timeout else None),
    }

    if use_post:
        kwargs['method'] = 'post'

    _prev_url = None

    while _url is not None:
        if _prev_url is not None:
            _url = urljoin(_prev_url, _url)

        response, _url, request_time = find_redirect(
            url=_url,
            **kwargs
        )

        item = Hope(type='header', url=response.url, status=response.status_code, time=request_time)

        if store().args.try_js and response.status_code < 300:  # only success codes
            js_location = __safe_js_redirect(response)

            if js_location is not None:
                _url = js_location
                item = Hope(type='js', url=response.url, status=response.status_code, time=request_time)

        response.close()
        _prev_url = _url
        yield item

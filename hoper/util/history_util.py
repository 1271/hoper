from typing import Optional, Iterator
from urllib.parse import urljoin

from requests.utils import default_headers

from .header_redirect_util import find_redirect
from .js_redirect_util import find_js_redirect
from .store import store, build_store
from .types import Hope
from .utils import normalize_url


def __safe_js_redirect(response):
    try:
        return find_js_redirect(response)
    except Exception:
        return None


def get_history(url: str, **_kw) -> Iterator[Hope]:
    """
    :return: url, status, request_time
    """

    if store() is None:
        build_store()

    headers = _kw.get('headers', default_headers())
    headers['User-Agent'] = _kw.get('user-agent', store().args.user_agent)
    _url = normalize_url(url)

    timeout = store().args.timeout

    kwargs = {
        'headers': headers,
        'cookies': _kw.get('cookies', store().args.cookies),
        'timeout': (timeout * 10 if timeout else None),
    }

    # if store().args.post:
    #     kwargs['method'] = 'post'

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

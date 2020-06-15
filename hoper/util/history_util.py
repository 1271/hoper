from typing import Iterator, Tuple
from urllib.parse import urljoin

from requests.utils import default_headers

from .header_redirect_util import find_redirect
from .js_redirect_util import find_js_redirect
from .store import store, has_store, build_store
from .types import Hope
from .utils import normalize_url
from .hooks import hooks_process


def __safe_js_redirect(response):
    try:
        return find_js_redirect(response)
    except Exception:
        return None


def get_history(url: str, **_kw) -> Iterator[Hope]:
    """
    :param str url: String url
    :param dict headers. See requests.structures.CaseInsensitiveDict
    :param str user_agent: String user-agent
    :param list cookies: array of strings
            Format: ['key1=value1', 'key2=value2', ...]
    :param list proxy: array of strings
            Format: ['http://proxy:123'] (for http and https)
             or ['http=http://proxy:123', 'https=http://secured-proxy:321', 'ftp=http://ftp-proxy:332']
    :param bool show_ip: boolean (show ip for each host)
    :param bool timeout: int (optional). Timeout for each request (1/100 sec)
    :param bool show_request_time: Show request time for each request
    :param bool no_error_messages: Do not show any errors
    :param bool no_statistic: Do not show statistic of end
    :param bool count_only: Show requests count and exit
    :param bool try_js: Try check js redirects
    :param bool last_only: Show only last request url
    :param bool disallow_loops: Do not allow loops (url1->url2->url1-> end)
    """

    headers = _kw.pop('headers', default_headers())

    if not has_store():
        build_store(**_kw)

    headers['User-Agent'] = store().args.user_agent
    _url = normalize_url(url)

    timeout = store().args.timeout

    kwargs = {
        'headers': headers,
        'cookies': store().args.cookies,
        'timeout': (timeout / 100 if timeout else None),
    }

    _prev_url = None

    while _url is not None:
        if _prev_url is None:
            _prev_url = _url

        original_url = _url

        _url, hook = with_hooks(_url)

        response, _url, request_time = find_redirect(
            url=urljoin(_prev_url, _url),
            **kwargs
        )

        item = Hope(
            type='header', url=response.url, status=response.status_code,
            time=request_time, headers=dict(response.headers),
            hook=hook, original_url=original_url,
        )

        if store().args.try_js and response.status_code < 300:  # only success codes
            js_location = __safe_js_redirect(response)

            if js_location is not None:
                _url = urljoin(_prev_url, js_location)
                item = Hope(
                    type='js', url=response.url, status=response.status_code,
                    time=request_time, headers=dict(response.headers),
                    hook=hook, original_url=original_url,
                )

        _prev_url = response.url

        response.close()

        yield item


def with_hooks(url) -> Tuple[str, bool]:
    if store().args.allow_hooks:
        _hook_url = hooks_process(url)
        if _hook_url is not None:
            return _hook_url, True
    return url, False


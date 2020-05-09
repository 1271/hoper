from time import time
from typing import Tuple, Optional

from requests import request, Response

from .store import store
from .utils import get_response_redirect_url, err


def find_redirect(url: str, **kwargs) -> Tuple[Response, Optional[str], float]:
    start_time = time()
    kwargs.setdefault('method', 'get')
    kwargs.pop('allow_redirects', None)
    kwargs.pop('stream', None)

    _proxies = store().proxies

    if _proxies is not None and len(_proxies):
        kwargs.setdefault('proxies', _proxies)

    try:
        response = request(
            url=url,
            allow_redirects=False,
            stream=True,
            **kwargs,
        )
    except Exception as e:
        err('Bug for url: "%s"' % url)
        raise e

    return response, get_response_redirect_url(response), time() - start_time

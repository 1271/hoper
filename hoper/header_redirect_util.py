from time import time
from typing import Tuple, Optional

from requests import request, Response

from ._store import store
from ._utils import get_response_redirect_url


def find_redirect(url: str, **kwargs) -> Tuple[Response, Optional[str], float]:
    start_time = time()
    kwargs.setdefault('method', 'get')
    kwargs.pop('allow_redirects', None)
    kwargs.pop('stream', None)

    _proxies = store().proxies

    if _proxies is not None and len(_proxies):
        kwargs.setdefault('proxies', _proxies)

    response = request(
        url=url,
        allow_redirects=False,
        stream=True,
        **kwargs,
    )

    return response, get_response_redirect_url(response), time() - start_time
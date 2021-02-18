from logging import info
from time import time
from typing import Tuple, Optional, List, Union

from requests import request, Response
from requests.exceptions import InvalidSchema

from .store import store
from .utils import get_response_redirect_url, err


class FakedResponseClass:
    url: str = None
    status_code: int = 200
    headers: List[str] = []

    def __init__(self, url: str, ):
        self.url = url

    def close(self):
        pass


def find_redirect(url: str, **kwargs) -> Tuple[Union[Response, FakedResponseClass], Optional[str], float]:
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
    except InvalidSchema as _e:
        info(_e.args)
        return FakedResponseClass(url), None, time() - start_time
    except Exception as e:
        err('Bug for url: "%s"' % url)
        raise e

    return response, get_response_redirect_url(response), time() - start_time

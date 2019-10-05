from requests import request, Response
from requests.utils import default_headers
from .args import arguments
from typing import List, Tuple
from sys import stderr
from .meta import version


def get_history(url: str, user_agent: str) -> List[Tuple[str, int]]:
    headers = default_headers()
    headers['User-Agent'] = user_agent
    response = request(method='head', headers=headers, url=url, allow_redirects=True)  # type: Response
    history = response.history  # type: List[Response]
    history.append(response)
    return [(i.url, response.status_code) for i in history]


def main():
    _args = arguments.parse_args()
    print('Python hoper v%s' % version)
    try:
        history = get_history(_args.url, _args.user_agent)
        if not len(history):
            print('History empty', file=stderr)
        else:
            for item in history:
                print('\nHop:\t%s\nStatus:\t%i' % item)
    except Exception:
        print('Connection error', file=stderr)
        exit(1)


if __name__ == '__main__':
    main()

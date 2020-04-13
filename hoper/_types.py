from typing import NamedTuple, List, Optional


class Hope(NamedTuple):
    type: str
    url: str
    status: int
    time: float


class Args(NamedTuple):
    url: str
    user_agent: str
    cookies: List[str]
    show_ip: bool
    timeout: int
    show_request_time: bool
    no_error_messages: bool
    no_statistic: bool
    # post: bool
    count_only: bool
    try_js: bool
    proxy: Optional[List[str]]
    last_only: bool
    disallow_loops: bool

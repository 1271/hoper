from typing import NamedTuple, List, Optional


class Hope(NamedTuple):
    type: str
    url: str
    status: int
    time: float


class Args(NamedTuple):
    user_agent: str
    cookies: List[str]
    show_ip: bool
    timeout: Optional[int]
    show_request_time: bool
    no_error_messages: bool
    no_statistic: bool
    count_only: bool
    try_js: bool
    proxy: Optional[List[str]]
    last_only: bool
    print_json: bool
    pretty_json: Optional[bool]
    disallow_loops: bool

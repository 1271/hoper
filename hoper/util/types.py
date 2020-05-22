from typing import NamedTuple, List, Optional, Dict


class Hope(NamedTuple):
    type: str
    url: str
    status: int
    time: float
    headers: Dict[str, str]
    hook: bool
    original_url: str


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
    allow_hooks: bool = False

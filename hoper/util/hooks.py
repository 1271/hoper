# special hooks for shortcut links
import re
from typing import Optional
from urllib.parse import unquote

hooks = [
    (
        re.compile(r'^https?://vk.com/away.php?.*to=(.+?)(?:&\w+=.*)?$'),
        lambda r: unquote(r.group(1)),
    ),
]


__all__ = ['hooks_process', ]


def hooks_process(url: str) -> Optional[str]:
    for hook in hooks:
        try:
            return hook[1](hook[0].search(url))
        except Exception:
            pass

    return None


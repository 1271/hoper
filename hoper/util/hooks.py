# special hooks for shortcut links
import re
from typing import Optional
from urllib.parse import unquote

_VK_HOOK = re.compile(r'^https?://vk.com/away.php?.*\bto=(.+?)(?:&\w+=.*)?$')
_YOUTUBE_HOOK = re.compile(r'^https?://www.youtube.com/redirect?.*\bq=(.+?)(?:&\w+=.*)?$')

hooks = [
    lambda url: unquote(_VK_HOOK.search(url).group(1)), # type: ignore
    lambda url: unquote(_YOUTUBE_HOOK.search(url).group(1)), # type: ignore
]


__all__ = ['hooks_process', ]


def hooks_process(url: str) -> Optional[str]:
    for hook in hooks:
        try:
            return hook(url)
        except Exception:
            pass

    return None


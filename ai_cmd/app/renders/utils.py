from functools import wraps
from typing import Any, Callable, Coroutine, Optional

from prompt_toolkit.layout import AnyContainer
from prompt_toolkit.shortcuts import print_container
from prompt_toolkit.styles import BaseStyle
from prompt_toolkit.widgets import Box, Frame


def simple_render_frame(title: str, class_name: Optional[str] = "", style:Optional[BaseStyle]=None):
    def decorator(func: Callable[..., Coroutine[Any, Any, "AnyContainer"]]):
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any):
            body = await func(*args, **kwargs)
            frame = Frame(
                Box(body, padding=1), title=title, style=f"class:{class_name}"
            )
            print_container(
                frame, style=style
            )
        return wrapper
    return decorator

from dataclasses import dataclass
from typing import Any, Callable, Coroutine, TypeVar


@dataclass(kw_only=True)
class Event:
    """Un evento"""

    type: str
    """Tipo del evento"""


E = TypeVar("E")
Listener = Callable[[E], None | Coroutine[Any, Any, None]]

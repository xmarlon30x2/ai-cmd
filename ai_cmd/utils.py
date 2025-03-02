from json import JSONDecodeError, loads
from typing import Any, Awaitable, Callable, ParamSpec, TypeVar


P = ParamSpec("P")
R = TypeVar("R")
SyncFunctio = Callable[P, R | Awaitable[R]]


async def wrapped_sync(func: SyncFunctio[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    value = func(*args, **kwargs)
    if isinstance(value, Awaitable):
        return await value  # type: ignore
    else:
        return value


def load_safe_json(arguments: str) -> dict[str, Any]:
    try:
        parameters: dict[str, Any] = loads(arguments)
    except JSONDecodeError:
        parameters = {}
    return parameters

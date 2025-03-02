from json import JSONDecodeError, loads
from os import getenv
from typing import Any, Awaitable, Callable, ParamSpec, TypeVar

import dotenv
from prompt_toolkit import HTML, print_formatted_text


def get_vars():
    """api_key, model, base_url, temperature"""
    dotenv.load_dotenv("app.env")
    api_key = getenv("apy_key") or ""
    model = getenv("model") or "deepseek"
    base_url = getenv("base_url") or "https://deepseek.com/"
    temperature = getenv("temperature")
    temperature = float(temperature) if temperature else 0.6
    print_formatted_text(
        HTML(
            f"<green>Usando el modelo <b>🤖 {model}</b> de {base_url} con temperatura de {temperature}🌡️</green>\n\n"
        )
    )
    return api_key, model, base_url, temperature


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

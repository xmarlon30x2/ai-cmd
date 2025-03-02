import functools
import inspect
import json
import shlex
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Type, Union, get_args, get_origin

from prompt_toolkit import HTML, print_formatted_text

from ..const import COMMAND_START


def dynamic_converter(
    converters: Optional[Dict[Type[Any], Callable[..., Any]]] = None,
    name: Optional[str] = None,
):
    func_name = name

    def decorator(func: Callable[..., Any]):

        @functools.wraps(func)
        def wrapper(arg_string: str) -> Any:
            # Manejo automático de --help
            if "--help" in arg_string.split():
                print_formatted_text(HTML(generate_help(func, name=func_name)))
                return None

            # Parseo inteligente con shlex para comillas
            try:
                tokens = shlex.split(arg_string)
            except ValueError as e:
                raise ValueError(f"Error parsing arguments: {e}")

            # Configuración inicial
            sig = inspect.signature(func)
            params = sig.parameters
            parsed_args: dict[str, str] = {}
            used_tokens: set[int] = set()

            # Procesar argumentos tipo --key value
            i = 0
            while i < len(tokens):
                if tokens[i].startswith("--"):
                    key = tokens[i][2:]
                    if key not in params:
                        raise ValueError(f"Parámetro desconocido: --{key}")

                    # Manejar flags booleanos sin valor
                    if i + 1 >= len(tokens) or tokens[i + 1].startswith("--"):
                        value = "True"
                    else:
                        value = tokens[i + 1]
                        used_tokens.add(i + 1)

                    parsed_args[key] = value
                    used_tokens.add(i)
                    i += 2 if value != "True" else 1
                else:
                    i += 1

            # Procesar argumentos posicionales
            positional_args = [t for i, t in enumerate(tokens) if i not in used_tokens]

            for param in params.values():
                if param.name not in parsed_args:
                    if positional_args:
                        parsed_args[param.name] = positional_args.pop(0)

            # Validación y conversión de tipos
            final_args = {}
            for name, param in params.items():
                if name not in parsed_args:
                    if param.default == inspect.Parameter.empty:
                        raise ValueError(f"Falta parámetro requerido: {name}")
                    final_args[name] = param.default
                    continue

                raw_value = parsed_args.get(name, "")
                final_args[name] = convert_value(
                    param.annotation, raw_value, param.default, converters or {}
                )

            return func(**final_args)

        return wrapper

    return decorator


def convert_value(
    param_type: Type[Any],
    raw_value: str,
    default: Any,
    converters: Dict[Type[Any], Callable[..., Any]],
) -> Any:
    if (not raw_value) and default is not None:
        return default

    if param_type in converters:
        return converters[param_type](raw_value)

    if param_type == bool:
        return raw_value.lower() in ("true", "1", "t", "y", "yes", "on")

    if param_type == list:
        return [x.strip() for x in raw_value.strip("[]").split(",")]

    if param_type == dict:
        return json.loads(raw_value.replace("'", '"'))

    if param_type == Path:
        return Path(raw_value)

    # Tipos genéricos (List[int], etc.)
    origin = get_origin(param_type)
    if origin:
        args = get_args(param_type)
        if origin == list:
            return [args[0](x) for x in raw_value.split(",")]
        elif origin == Union:
            return (
                convert_value(
                    args[0], raw_value=raw_value, default=default, converters=converters
                )
                if raw_value
                else None
            )

    # Conversión básica de tipos
    try:
        return param_type(raw_value)
    except ValueError:
        raise ValueError(f"No se puede convertir '{raw_value}' a {param_type.__name__}")


def generate_help(func: Callable[..., Any], name: Optional[str] = None) -> str:
    help_text = [
        f"\nUso: <white>{COMMAND_START+(name or func.__name__)}</white> [<blue>--help</blue>] [<orange>--parámetro</orange> <gray>valor</gray>]...\n"
    ]
    sig = inspect.signature(func)

    for param in sig.parameters.values():
        type_name = (
            param.annotation.__name__
            if param.annotation != inspect.Parameter.empty
            else "str"
        )
        required = param.default == inspect.Parameter.empty
        default = (
            f" (<blue>default</blue>: <gray>{param.default}</gray>)"
            if not required
            else ""
        )
        help_text.append(
            f"  <blue>--{param.name:20}</blue> <green>{type_name:15}</green> {'[<orange>REQUERIDO</orange>]' if required else ''}{default}"
        )

    return "\n".join(help_text)

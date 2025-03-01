"""Specs"""

import inspect
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

from .mappers import TypeToJSONSchemaMapper
from .parsers import DocstringParser

if TYPE_CHECKING:
    from .types import Tool


class FunctionSpec:
    """Genera el spec de una herramienta"""

    @classmethod
    def generate(
        cls,
        func: Callable[..., Any],
        custom_name: Optional[str] = None,
        custom_desc: Optional[str] = None,
    ) -> "Tool":
        """Genera la especificación completa para una herramienta"""
        sig = inspect.signature(func)
        base_desc, param_docs = DocstringParser.parse(inspect.getdoc(func) or "")
        parameters: Dict[str, Any] = {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        }
        for name, param in sig.parameters.items():
            if name == "self":
                continue
            param_spec = TypeToJSONSchemaMapper.map(param.annotation)
            param_spec["description"] = param_docs.get(name, "")
            parameters["properties"][name] = param_spec

            if param.default == inspect.Parameter.empty:
                parameters["required"].append(name)
        return {
            "type": "function",
            "function": {
                "name": custom_name or func.__name__,
                "description": custom_desc or base_desc,
                "parameters": parameters,
            },
        }

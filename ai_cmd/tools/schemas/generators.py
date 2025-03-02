import inspect
from typing import Any, Callable, Optional

from .mapper import TypeToJSONSchemaMapper
from .parsers import DocstringParser
from .types import FunctionSchema


def function_to_tool_schema(func: Callable[..., Any]) -> dict[str, Any]:
    """Converts a typed Python function into an OpenAI-compatible tool schema."""
    schema = FunctionSchemaGenerator.generate(func)
    return schema.to_schema()


class FunctionSchemaGenerator:
    """Generates the schema for a tool."""

    @classmethod
    def generate(
        cls,
        function: Callable[..., Any],
        custom_name: Optional[str] = None,
        custom_desc: Optional[str] = None,
    ) -> "FunctionSchema":
        """Generates the complete specification for a tool."""
        sig = inspect.signature(function)
        docstring = inspect.getdoc(function) or ""
        description, param_docs = DocstringParser.parse(docstring)

        parameters: dict[str, Any] = {
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

        return FunctionSchema(
            name=custom_name or function.__name__,
            description=custom_desc or description,
            parameters=parameters,
            callable=function,
        )

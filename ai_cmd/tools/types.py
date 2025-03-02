from dataclasses import dataclass, field
from typing import Any, Literal

from .schemas.types import FunctionSchema


@dataclass
class Tool:
    function: FunctionSchema
    type: Literal["function"] = field(default="function")

    def to_schema(self) -> dict[str, Any]:
        return {"type": self.type, "function": self.function.to_schema()}


@dataclass
class FunctionCall:
    name: str
    arguments: str


@dataclass
class ToolCall:
    id: str
    function: FunctionCall
    type: Literal["function"] = field(default="function")

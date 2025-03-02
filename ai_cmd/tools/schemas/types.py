from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class FunctionSchema:
    name: str
    description: str
    parameters: dict[str, Any]
    callable: Callable[..., Any]

    def to_schema(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }

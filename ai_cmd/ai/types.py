from dataclasses import dataclass, field
from typing import Literal, TypeAlias

from ..tools.types import ToolCall


@dataclass
class ContentToken:
    content: str
    type: Literal["content"] = field(default="content")


@dataclass
class ToolsCallsToken:
    tools_calls: list[ToolCall]
    type: Literal["tools_calls"] = field(default="tools_calls")


Token: TypeAlias = ContentToken | ToolsCallsToken

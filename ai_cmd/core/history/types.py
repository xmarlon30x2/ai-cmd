from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, Optional, TypeAlias

if TYPE_CHECKING:
    from ...tools.types import ToolCall

__all__ = [
    "UserMessage",
    "AssistantMessage",
    "ToolMessage",
    "SystemMessage",
]


@dataclass
class UserMessage:
    content: str
    name: Optional[str] = field(default=None)
    role: Literal["user"] = field(default="user")


@dataclass
class AssistantMessage:
    content: str = field(default="")
    tool_calls: Optional[list["ToolCall"]] = field(default=None)
    role: Literal["assistant"] = field(default="assistant")


@dataclass
class ToolMessage:
    name: Optional[str]
    content: str
    tool_call_id: str
    role: Literal["tool"] = field(default="tool")


@dataclass
class SystemMessage:
    content: str
    role: Literal["system"] = field(default="system")


Message: TypeAlias = UserMessage | AssistantMessage | ToolMessage | SystemMessage

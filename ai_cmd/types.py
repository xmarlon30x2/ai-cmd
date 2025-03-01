from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, TypeAlias


@dataclass
class FunctionCall:
    name: str
    arguments: str


@dataclass
class ToolCall:
    id: str
    function: FunctionCall
    type: Literal["function"] = field(default="function")


@dataclass
class ContentToken:
    content: str
    type: Literal["content"] = field(default="content")


@dataclass
class ToolsCallsToken:
    tools_calls: List[ToolCall]
    type: Literal["tools_calls"] = field(default="tools_calls")


@dataclass
class UserMessage:
    content: str
    name: Optional[str] = field(default=None)
    role: Literal["user"] = field(default="user")


@dataclass
class AssistantMessage:
    content: str = field(default="")
    tool_calls: Optional[List[ToolCall]] = field(default=None)
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


@dataclass
class FunctionDefinition:
    name: str
    description: str
    parameters: Dict[str, object]


@dataclass
class Tool:
    function: FunctionDefinition
    type: Literal["function"] = field(default="function")


Token: TypeAlias = ContentToken | ToolsCallsToken
Message: TypeAlias = UserMessage | AssistantMessage | ToolMessage | SystemMessage

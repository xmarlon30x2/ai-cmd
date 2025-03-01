from dataclasses import dataclass
from typing import Dict, List, Literal, Optional, TypeAlias, TypedDict


@dataclass
class FunctionCall:
    name: str
    arguments: str


@dataclass
class ToolCall:
    id: str
    type: Literal["function"]
    function: FunctionCall


@dataclass
class ContentToken:
    type: Literal["content"]
    content: str


@dataclass
class ToolsToken:
    type: Literal["tools"]
    tools_calls: List[ToolCall]


class UserMessage(TypedDict):
    role: Literal["user"]
    content: str
    name: Optional[str]


class AssistantMessage(TypedDict):
    role: Literal["assistant"]
    content: str
    tool_calls: Optional[str]


class ToolMessage(TypedDict):
    role: Literal["tool"]
    name: Optional[str]
    content: str
    tool_call_id: str


class SystemMessage(TypedDict):
    role: Literal["system"]
    content: str


class FunctionDefinition(TypedDict):
    name: str
    description: str
    parameters: Dict[str, object]


class Tool(TypedDict):
    type: Literal["function"]
    function: FunctionDefinition


Token: TypeAlias = ContentToken | ToolsToken
Message: TypeAlias = UserMessage | AssistantMessage | ToolMessage | SystemMessage

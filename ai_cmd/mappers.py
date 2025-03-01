"""Mappers"""

from asyncio import gather
from typing import (TYPE_CHECKING, Any, Callable, Dict, List, Literal,
                    Optional, get_args, get_origin)

from .types import FunctionCall, ToolCall

if TYPE_CHECKING:
    from openai.types.chat.chat_completion_assistant_message_param import \
        ChatCompletionAssistantMessageParam
    from openai.types.chat.chat_completion_chunk import ChoiceDeltaToolCall
    from openai.types.chat.chat_completion_message_param import \
        ChatCompletionMessageParam
    from openai.types.chat.chat_completion_message_tool_call_param import \
        ChatCompletionMessageToolCallParam
    from openai.types.chat.chat_completion_system_message_param import \
        ChatCompletionSystemMessageParam
    from openai.types.chat.chat_completion_tool_message_param import \
        ChatCompletionToolMessageParam
    from openai.types.chat.chat_completion_tool_param import \
        ChatCompletionToolParam
    from openai.types.chat.chat_completion_user_message_param import \
        ChatCompletionUserMessageParam

    from .types import Message, Tool, ToolCall


class _DefaultFunction:
    id = "unknow"
    name = "unknow"
    arguments = ""


class TypeToJSONSchemaMapper:
    """Convierte tipos Python a JSON Schema con soporte para tipos complejos"""

    TYPE_MAPPING: Dict[Any, Dict[str, Any]] = {
        str: {"type": "string"},
        int: {"type": "integer"},
        float: {"type": "number"},
        bool: {"type": "boolean"},
        list: {"type": "array"},
        dict: {"type": "object"},
        type(None): {"type": "null"},
    }

    @classmethod
    def map(cls, python_type: Any) -> Dict[str, Any]:
        """Genera schema recursivo para tipos complejos"""
        origin = get_origin(python_type) or python_type
        args = get_args(python_type)
        if schema := cls.TYPE_MAPPING.get(origin):
            return schema.copy()
        handler = cls._get_type_handler(origin)
        return handler(args) if handler else {"type": "string"}

    @classmethod
    def _get_type_handler(cls, origin: Any) -> Optional[Callable[[Any], Any]]:
        handlers: Dict[Any, Callable[[Any], Any]] = {
            list: cls._handle_list,
            List: cls._handle_list,
            dict: cls._handle_dict,
            Dict: cls._handle_dict,
            Literal: cls._handle_literal,
            Any: cls._handle_any,
        }
        return handlers.get(origin, None)

    @classmethod
    def _handle_any(cls, _args: Any) -> Any:
        return {}

    @classmethod
    def _handle_list(cls, args: tuple[Any, ...]) -> Any:
        return {"type": "array", "items": cls.map(args[0]) if args else {}}

    @classmethod
    def _handle_dict(cls, args: tuple[Any, ...]) -> Any:
        key_type = cls.map(args[0]) if args else {}
        value_type = cls.map(args[1]) if len(args) > 1 else {}
        return {
            "type": "object",
            "additionalProperties": value_type,
            "propertyNames": key_type,
        }

    @classmethod
    def _handle_literal(cls, args: tuple[Any, ...]) -> Any:
        return {"enum": list(args)}


class MessageMapper:
    @staticmethod
    async def to_openai_list(
        messages: List["Message"],
    ) -> List["ChatCompletionMessageParam"]:
        return await gather(*map(MessageMapper.to_openai, messages))

    @staticmethod
    async def to_openai(message: "Message") -> "ChatCompletionMessageParam":
        match message.role:
            case "user":
                message_param_user: "ChatCompletionUserMessageParam" = {
                    "role": "user",
                    "content": message.content,
                }
                if name := message.name:
                    message_param_user["name"] = name
                return message_param_user
            case "assistant":
                message_param_assistant: "ChatCompletionAssistantMessageParam" = {
                    "role": "assistant",
                    "content": message.content,
                }
                if message.tool_calls:
                    message_param_assistant["tool_calls"] = (
                        await ToolCallMapper.to_openai_list(message.tool_calls)
                    )
                return message_param_assistant
            case "tool":
                message_param_tool: "ChatCompletionToolMessageParam" = {
                    "role": "tool",
                    "content": message.content,
                    "tool_call_id": message.tool_call_id,
                }
                return message_param_tool
            case "system":
                message_param_system: "ChatCompletionSystemMessageParam" = {
                    "role": "system",
                    "content": message.content,
                }
                return message_param_system


class ToolCallMapper:
    @staticmethod
    async def to_openai(tool_call: "ToolCall") -> "ChatCompletionMessageToolCallParam":
        return {
            "id": tool_call.id,
            "type": "function",
            "function": {
                "name": tool_call.function.name,
                "arguments": tool_call.function.arguments,
            },
        }

    @staticmethod
    async def to_openai_list(
        tools_calls: List["ToolCall"],
    ) -> List["ChatCompletionMessageToolCallParam"]:
        return await gather(*map(ToolCallMapper.to_openai, tools_calls))

    @staticmethod
    async def to_domain(delta_tool_call: "ChoiceDeltaToolCall") -> "ToolCall":
        function = delta_tool_call.function or _DefaultFunction
        return ToolCall(
            id=delta_tool_call.id or _DefaultFunction.id,
            function=FunctionCall(
                name=function.name or _DefaultFunction.name,
                arguments=function.arguments or _DefaultFunction.arguments,
            ),
        )

    @staticmethod
    async def to_domain_list(
        delta_tools_calls: List["ChoiceDeltaToolCall"],
    ) -> List["ToolCall"]:
        return await gather(*map(ToolCallMapper.to_domain, delta_tools_calls))


class ToolMapper:
    @staticmethod
    async def to_openai(tool: "Tool") -> "ChatCompletionToolParam":
        parameters = tool.function.parameters
        return {
            "type": "function",
            "function": {
                "name": tool.function.name,
                "description": tool.function.description,
                "parameters": parameters,
            },
        }

    @staticmethod
    async def to_openai_list(tools: List["Tool"]) -> List["ChatCompletionToolParam"]:
        return await gather(*map(ToolMapper.to_openai, tools))

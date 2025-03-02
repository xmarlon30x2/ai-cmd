from asyncio import gather
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openai.types.chat.chat_completion_assistant_message_param import (
        ChatCompletionAssistantMessageParam,
    )
    from openai.types.chat.chat_completion_chunk import ChoiceDeltaToolCall
    from openai.types.chat.chat_completion_message_param import (
        ChatCompletionMessageParam,
    )
    from openai.types.chat.chat_completion_message_tool_call_param import (
        ChatCompletionMessageToolCallParam,
    )
    from openai.types.chat.chat_completion_system_message_param import (
        ChatCompletionSystemMessageParam,
    )
    from openai.types.chat.chat_completion_tool_message_param import (
        ChatCompletionToolMessageParam,
    )
    from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
    from openai.types.chat.chat_completion_user_message_param import (
        ChatCompletionUserMessageParam,
    )

    from ....core.history.types import Message
    from ....tools.types import FunctionCall, Tool, ToolCall


DEFAULT_ID = "unknow"
DEFAULT_NAME = "unknow"
DEFAULT_ARGUMENTS = ""


class _DefaultFunction:
    name = DEFAULT_NAME
    arguments = DEFAULT_ARGUMENTS


class MessageMapper:
    @staticmethod
    async def to_openai_list(
        messages: list["Message"],
    ) -> list["ChatCompletionMessageParam"]:
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
        tools_calls: list["ToolCall"],
    ) -> list["ChatCompletionMessageToolCallParam"]:
        return await gather(*map(ToolCallMapper.to_openai, tools_calls))

    @staticmethod
    async def to_domain(delta_tool_call: "ChoiceDeltaToolCall") -> "ToolCall":
        function = delta_tool_call.function or _DefaultFunction
        return ToolCall(
            id=delta_tool_call.id or DEFAULT_ID,
            function=FunctionCall(
                name=function.name or DEFAULT_NAME,
                arguments=function.arguments or DEFAULT_ARGUMENTS,
            ),
        )

    @staticmethod
    async def to_domain_list(
        delta_tools_calls: list["ChoiceDeltaToolCall"],
    ) -> list["ToolCall"]:
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
    async def to_openai_list(tools: list["Tool"]) -> list["ChatCompletionToolParam"]:
        return await gather(*map(ToolMapper.to_openai, tools))

from typing import TYPE_CHECKING, Any, AsyncGenerator, List

from openai import AsyncOpenAI

from ..ai import AI

if TYPE_CHECKING:
    from openai.types.chat.chat_completion_chunk import ChoiceDeltaToolCall
    from openai.types.chat.chat_completion_message_param import (
        ChatCompletionMessageParam,
    )
    from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam

    from ..types import (
        ContentToken,
        FunctionCall,
        Message,
        Token,
        Tool,
        ToolCall,
        ToolsToken,
    )


class _DefaultFunction:
    name = "unknow"
    arguments = ""


class OpenAI(AI):
    def __init__(self, api_key: str, base_url: str, model: str, temperature: float):
        self.openai = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.temperature = temperature

    async def chat(
        self, messages: List["Message"], tools: List["Tool"]
    ) -> AsyncGenerator["Token", None]:
        delta_tools_calls: List["ChoiceDeltaToolCall"] = []
        async for chunk in await self._create(messages, tools):
            delta = chunk.choices[0].delta
            if delta.content:
                yield ContentToken(type="content", content=delta.content)
            if delta.tool_calls:
                await self._collecte_tool_calls(delta_tools_calls, delta.tool_calls)
        if len(delta_tools_calls):
            yield ToolsToken(
                type="tools",
                tools_calls=await self._map_to_domain_tools(delta_tools_calls),
            )

    async def _map_to_openai_messages(
        self, messages: List["Message"]
    ) -> List['ChatCompletionMessageParam']:
        return messages  # type: ignore

    async def _map_to_openai_tools(
        self, tools: List["Tool"]
    ) -> List["ChatCompletionToolParam"]:
        return tools  # type: ignore

    async def _create(self, messages: List["Message"], tools: List["Tool"]):
        arguments: dict[str, Any] = {}
        if len(tools):
            arguments["tools"] = await self._map_to_openai_tools(tools)
            arguments["tool_choice"] = "auto"
        return await self.openai.chat.completions.create(
            messages=await self._map_to_openai_messages(messages),
            model=self.model,
            temperature=self.temperature,
            stream=True,
            **arguments
        )

    async def _map_to_domain_tools(
        self, delta_tools_calls: List["ChoiceDeltaToolCall"]
    ) -> List["ToolCall"]:

        def mapper(delta_tool_call: "ChoiceDeltaToolCall") -> "ToolCall":
            function = delta_tool_call.function or _DefaultFunction
            return ToolCall(
                id=delta_tool_call.id or "unknow",
                type="function",
                function=FunctionCall(
                    name=function.name or _DefaultFunction.name,
                    arguments=function.arguments or _DefaultFunction.arguments,
                ),
            )

        return list(map(mapper, delta_tools_calls))

    async def _collecte_tool_calls(
        self,
        delta_tools_calls: List["ChoiceDeltaToolCall"],
        tools_calls: List["ChoiceDeltaToolCall"],
    ):
        for tools_call in tools_calls:
            if tools_call.index >= len(delta_tools_calls):
                delta_tools_calls.append(tools_call)
            elif tools_call.function and tools_call.function.arguments:
                delta_tools_calls[
                    tools_call.index
                ].function.arguments += tools_call.function.arguments  # type: ignore

from typing import TYPE_CHECKING, Any, AsyncGenerator, List

from openai import APIConnectionError, AsyncOpenAI

from ai_cmd.exceptions import ConnectionError

from ..ai import AI
from ..mappers import MessageMapper, ToolCallMapper, ToolMapper
from ..types import ContentToken, ToolsCallsToken

if TYPE_CHECKING:
    from openai.types.chat.chat_completion_chunk import ChoiceDeltaToolCall

    from ..types import Message, Token, Tool


class OpenAI(AI):
    def __init__(self, api_key: str, base_url: str, model: str, temperature: float):
        self.openai = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.temperature = temperature

    async def chat(
        self, messages: List["Message"], tools: List["Tool"]
    ) -> AsyncGenerator["Token", None]:
        delta_tools_calls: List["ChoiceDeltaToolCall"] = []
        try:
            async for chunk in await self._create_chat(messages, tools):
                if not chunk: continue
                delta = chunk.choices[0].delta
                if delta.content:
                    yield ContentToken(content=delta.content)
                if delta.tool_calls:
                    await self._collecte_tool_calls(delta_tools_calls, delta.tool_calls)
        except APIConnectionError as exc:
            raise ConnectionError(
                "Error al establecer la conexion con el modelo"
            ) from exc
        if len(delta_tools_calls):
            yield ToolsCallsToken(
                tools_calls=await ToolCallMapper.to_domain_list(delta_tools_calls),
            )

    async def _create_chat(self, messages: List["Message"], tools: List["Tool"]):
        arguments: dict[str, Any] = {}
        if len(tools):
            arguments["tools"] = await ToolMapper.to_openai_list(tools)
            arguments["tool_choice"] = "auto"
        return await self.openai.chat.completions.create(
            messages=await MessageMapper.to_openai_list(messages[:-1]),
            model=self.model,
            temperature=self.temperature,
            stream=True,
            timeout=120,
            **arguments
        )

    async def _collecte_tool_calls(
        self,
        delta_tools_calls: List["ChoiceDeltaToolCall"],
        tools_calls: List["ChoiceDeltaToolCall"],
    ):
        for tools_call in tools_calls:
            if tools_call.index == None or tools_call.index >= len(delta_tools_calls):  # type: ignore
                delta_tools_calls.append(tools_call)
            elif tools_call.function and tools_call.function.arguments:
                delta_tools_calls[
                    tools_call.index
                ].function.arguments += tools_call.function.arguments  # type: ignore

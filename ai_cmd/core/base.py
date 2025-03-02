from asyncio import CancelledError
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, AsyncGenerator, Optional

from .events import (CoreGenerationEndEvent, CoreGenerationErrorEvent,
                     CoreGenerationRecvContentTokenEvent,
                     CoreGenerationRecvToolsCallsTokenEvent,
                     CoreGenerationStartEvent, CoreResetEvent,
                     CoreToolsLoadingEvent)
from .history.types import AssistantMessage, UserMessage

if TYPE_CHECKING:
    from ..ai.base import AI
    from ..ai.types import ContentToken, Token, ToolsCallsToken
    from ..controller.base import Controller
    from ..core.history.base import History
    from ..tools.base import Tools
    from ..tools.types import Tool


#
@dataclass(kw_only=True)
class Core:
    controller: "Controller"
    ai: "AI"
    history: "History"
    tools: Optional["Tools"]

    async def start_generation(self, content: str, name: Optional[str] = None) -> None:
        message = UserMessage(content=content, name=name)
        await self.history.add_user_message(message=message)
        await self.generation_loop()

    async def generation_loop(self) -> None:
        has_next_step = True
        while has_next_step:
            has_next_step = await self.generation_step()
            # if has_next_step:
            #     message = UserMessage(content="ok")
            #     await self.history.add_user_message(message=message)

    async def generation_step(self) -> bool:
        completion, message = await self.start_generation_step()
        has_next_step = False
        try:
            has_next_step = await self.process_generation_step(
                completion=completion, message=message
            )
        except RuntimeError as exc:
            raise CancelledError()
        except Exception as exc:
            has_next_step = await self.error_generation_step(error=exc)
        finally:
            has_next_step = await self.end_generation_step(
                message=message, has_next_step=has_next_step
            )
        return has_next_step

    async def start_generation_step(
        self,
    ) -> tuple[AsyncGenerator["ContentToken | ToolsCallsToken", Any], AssistantMessage]:
        event = CoreGenerationStartEvent(core=self)
        await self.controller.trigger(event=event)
        tools = await self.list_tools()
        completion = self.ai.chat(messages=self.history.messages, tools=tools)
        message = AssistantMessage()
        await self.history.add_assistant_message(message=message)
        return completion, message

    async def process_generation_step(
        self, completion: AsyncGenerator["Token", Any], message: "AssistantMessage"
    ) -> bool:
        has_next_step = False
        async for token in completion:
            if token.type == "content":
                if await self.handler_content_token(message=message, token=token):
                    has_next_step = True
            elif token.type == "tools_calls":
                if await self.handler_tools_calls_token(message=message, token=token):
                    has_next_step = True
        return has_next_step

    async def error_generation_step(self, error: Exception) -> bool:
        event = CoreGenerationErrorEvent(core=self, error=error)
        await self.controller.trigger(event=event)
        return False

    async def end_generation_step(
        self, message: "AssistantMessage", has_next_step: bool
    ) -> bool:
        event = CoreGenerationEndEvent(core=self)
        await self.controller.trigger(event=event)
        if message.content == "":
            message.content = "ok"
        return has_next_step

    async def handler_content_token(
        self, message: "AssistantMessage", token: "ContentToken"
    ) -> bool:
        event = CoreGenerationRecvContentTokenEvent(
            core=self, token=token, message=message
        )
        await self.controller.trigger(event=event)
        message.content += token.content
        return False

    async def handler_tools_calls_token(
        self, message: "AssistantMessage", token: "ToolsCallsToken"
    ) -> bool:
        event = CoreGenerationRecvToolsCallsTokenEvent(
            core=self, token=token, message=message
        )
        await self.controller.trigger(event=event)
        if len(token.tools_calls) == 0 or not self.tools:
            return False
        if not message.tool_calls:
            message.tool_calls = []
        for tool_call in token.tools_calls:
            message.tool_calls.append(tool_call)
            tool_message = await self.tools.execute(tool_call=tool_call)
            await self.history.add_tool_message(message=tool_message)
        return True

    async def list_tools(self) -> list["Tool"]:
        event = CoreToolsLoadingEvent(core=self)
        await self.controller.trigger(event=event)
        return (await self.tools.list()) if self.tools else []

    async def reset(self) -> None:
        event = CoreResetEvent(core=self)
        await self.controller.trigger(event=event)
        if self.tools:
            await self.tools.reset()
        await self.history.reset()

"""
with Progress(console=self.console) as progress:
task = progress.add_task(
                    f"[magenta]Ejecutando {tool_call.function.name}...[/magenta]",
                    total=None,
                )            
        self.console.print("\n")

                progress.update(task, completed=True)

"""

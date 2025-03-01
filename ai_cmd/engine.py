from typing import TYPE_CHECKING, List

from rich.live import Live
from rich.markdown import Markdown
from rich.progress import Progress

if TYPE_CHECKING:
    from rich.console import Console

    from .ai import AI
    from .tool_handler import ToolHandler
    from .types import Message, Tool, ToolCall, UserMessage


class Engine:
    def __init__(self, ai: "AI", console: "Console", tool_handler: "ToolHandler"):
        self.console = console
        self.messages: List[Message] = []
        self.tool_handler = tool_handler
        self.ai = ai

    async def generate(self, content: str) -> None:
        message: UserMessage = {"role": "user", "content": content, "name": "user"}
        self.messages.append(message)
        await self.loop()

    async def loop(self):
        steps = 1
        while steps > 0:
            steps -= 1
            has_next_step = await self.step()
            if has_next_step:
                steps += 1

    async def step(self):
        tools = await self.get_tools()
        has_next_step = False
        self.buffer = ""
        self.live = Live(console=self.console, auto_refresh=False)
        try:
            async for token in self.ai.chat(messages=self.messages, tools=tools):
                if token.type == "content":
                    await self.add_content(content=token.content)
                elif token.type == "tools":
                    result = await self.add_tools_calls(tools_calls=token.tools_calls)
                    if result:
                        has_next_step = True
        finally:
            if self.live.is_started:
                self.live.stop()
        return has_next_step

    async def get_tools(self) -> List["Tool"]:
        return await self.tool_handler.specs()

    async def add_content(self, *, content: str) -> None:
        self.buffer += content
        if not self.live.is_started:
            self.live.start()
        self.live.update(Markdown(self.buffer), refresh=True)

    async def add_tools_calls(self, *, tools_calls: List["ToolCall"]) -> bool:
        if self.live.is_started:
            self.live.stop()
        if len(tools_calls) == 0:
            return False
        with Progress(console=self.console) as progress:
            for tool_call in tools_calls:
                task = progress.add_task(
                    f"[magenta]Ejecutando {tool_call.function.name}...[/magenta]",
                    total=None,
                )
                await self.tool_handler.execute(tool_call)
                progress.update(task, completed=True)
        self.console.print("\n\n")
        return True

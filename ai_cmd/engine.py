from traceback import format_exception
from typing import TYPE_CHECKING, List

from rich.live import Live
from rich.markdown import Markdown
from rich.progress import Progress

from .exceptions import ConnectionError
from .types import AssistantMessage, SystemMessage, ToolCall, UserMessage

if TYPE_CHECKING:
    from rich.console import Console

    from .ai import AI
    from .tool_handler import ToolHandler
    from .types import Message, Tool


DEFAULT_SYSTEM_MESSAGE = "Eres un poderoso asistente de IA, tu deber es ayudar \
    al usuario de la manera mas autonoma posible. Tienes una gra variedad de \
    herramientas a tu dispocicion, usalas siempre que puedas y debas. Dirigete \
    al usuario solo cuendo hallas cumplido con su peticion, nesesites mas \
    informacion o tengas un problema que no puedas solucionar por tu cuenta, \
    recuera siempre intentar ser los mas autonomo posible. Tienes acceso total a \
    la PC del usario, utiliza eso y piensa fuera de la caja"


class Engine:
    def __init__(
        self, ai: "AI", console: "Console", tool_handler: "ToolHandler | None" = None
    ):
        self.console = console
        self.tool_handler = tool_handler
        self.ai = ai
        self.messages: List[Message] = [SystemMessage(content=DEFAULT_SYSTEM_MESSAGE)]

    async def reset(self):
        if self.tool_handler:
            await self.tool_handler.reset()
        self.messages: List[Message] = [SystemMessage(content=DEFAULT_SYSTEM_MESSAGE)]

    async def generate(self, content: str) -> None:
        message = UserMessage(content=content)
        self.messages.append(message)
        await self.loop()

    async def loop(self):
        steps = 1
        while steps > 0:
            steps -= 1
            has_next_step = await self.step()
            if has_next_step:
                steps += 1
                self.messages.append(UserMessage(content="ok"))

    async def step(self):
        has_next_step = False
        tools = await self.get_tools()
        completion = self.ai.chat(messages=self.messages, tools=tools)
        self.current_message_assistant = AssistantMessage()
        self.messages.append(self.current_message_assistant)
        self.index = len(self.messages) - 1
        self.live = Live(console=self.console, auto_refresh=False)
        try:
            async for token in completion:
                if token.type == "content":
                    await self.add_content(content=token.content)
                elif token.type == "tools_calls":
                    result = await self.add_tools_calls(tools_calls=token.tools_calls)
                    if result:
                        has_next_step = True
        except ConnectionError as exc:
            self.console.print(
                f"[red]⛔ Error de conexion[/red]\n[gray]{str(exc)}[/gray]"
            )
        except Exception as exc:
            exception = "\n".join(format_exception(exc))
            self.console.print(
                f"[red]⛔ Ha ocurrido un error inesperado.\n{exception}[/red]"
            )
            has_next_step = False
        finally:
            if self.live.is_started:
                self.live.stop()
        if self.current_message_assistant.content == "":
            self.current_message_assistant.content = "ok"
        return has_next_step

    async def get_tools(self) -> List["Tool"]:
        if self.tool_handler:
            return await self.tool_handler.specs()
        return []

    async def add_content(self, *, content: str) -> None:
        self.messages[self.index].content += content
        if not self.live.is_started:
            self.live.start()
        self.live.update(Markdown(self.current_message_assistant.content), refresh=True)

    async def add_tools_calls(self, *, tools_calls: List["ToolCall"]) -> bool:
        if self.live.is_started:
            self.live.stop()
        if len(tools_calls) == 0 or not self.tool_handler:
            return False
        if not self.current_message_assistant.tool_calls:
            self.current_message_assistant.tool_calls = []
        with Progress(console=self.console) as progress:
            for tool_call in tools_calls:
                assistant_message = self.messages[self.index]
                if type(assistant_message) == AssistantMessage:
                    if not assistant_message.tool_calls:
                        assistant_message.tool_calls = []
                    assistant_message.tool_calls.append(tool_call)
                    self.messages[self.index] = assistant_message
                task = progress.add_task(
                    f"[magenta]Ejecutando {tool_call.function.name}...[/magenta]",
                    total=None,
                )
                tool_message = await self.tool_handler.execute(tool_call)
                self.messages.append(tool_message)
                progress.update(task, completed=True)
        self.console.print("\n")
        return True

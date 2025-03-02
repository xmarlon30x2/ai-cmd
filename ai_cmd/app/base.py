from asyncio import CancelledError, Task, create_task
from dataclasses import dataclass, field
from traceback import format_exception
from typing import TYPE_CHECKING

from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.formatted_text.pygments import PygmentsTokens
from prompt_toolkit.shortcuts import PromptSession, print_formatted_text
from prompt_toolkit.styles import style_from_pygments_cls
from pygments import lex
from pygments.lexers.python import PythonTracebackLexer  # type: ignore
from pygments.styles.onedark import OneDarkStyle  # type: ignore
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.style import Style


from ..ai.exceptions import ConnectionError
from ..app.renders.tool_messages import (
    render_dirs_list_tool_message,
    render_generic_tool_message,
)
from ..controller.utils import decorator_listener
from ..core.events import (
    CoreGenerationEndEvent,
    CoreGenerationErrorEvent,
    CoreGenerationRecvContentTokenEvent,
    CoreGenerationStartEvent,
)
from ..core.history.types import ToolMessage
from ..tools.events import ToolsExecuteEndEvent, ToolsExecuteStartEvent
from .const import COMMAND_START
from .exceptions import AppClose
from .renders.tool_calls import (
    render_dirs_list_tool_call,
    render_files_read_tool_call,
    render_files_write_tool_call,
    render_generic_tool_call,
    render_os_shell_tool_call,
)

if TYPE_CHECKING:
    from ..controller.base import Controller
    from ..core.base import Core
    from ..tools.types import ToolCall
    from ..window.base import Window
    from .commands.base import Commands
    from ..settings.base import Settings


@dataclass(kw_only=True)
class App:
    controller: "Controller"
    core: "Core"
    commands: "Commands"
    window: "Window"
    settings: "Settings"
    prompt: str = field(default="+ ", init=False)

    task: Task[None] | None = None
    live: Live | None = None
    running: bool = False

    def __post_init__(self):
        self.commands.join(app=self)
        self.subscribe(controller=self.controller)
        self.session: PromptSession[str] = PromptSession(self.prompt)

    def subscribe(self, controller: "Controller"):
        @decorator_listener(controller=controller, event_type=CoreGenerationErrorEvent)
        async def _(event: "CoreGenerationErrorEvent"):
            await self.on_generation_error(event=event)

        @decorator_listener(controller=controller, event_type=CoreGenerationStartEvent)
        async def _(event: "CoreGenerationStartEvent"):
            await self.on_generation_start()

        @decorator_listener(
            controller=controller, event_type=CoreGenerationRecvContentTokenEvent
        )
        async def _(event: "CoreGenerationRecvContentTokenEvent"):
            await self.on_generation_content(event.token.content)

        @decorator_listener(controller=controller, event_type=CoreGenerationEndEvent)
        async def _(event: "CoreGenerationEndEvent"):
            await self.on_generation_end()

        @decorator_listener(controller=controller, event_type=ToolsExecuteStartEvent)
        async def _(event: "ToolsExecuteStartEvent"):
            await self.on_tool_call_start(event.tool_call)

        @decorator_listener(controller=controller, event_type=ToolsExecuteEndEvent)
        async def _(event: "ToolsExecuteEndEvent"):
            await self.on_tool_message(
                tool_call=event.tool_call, tool_message=event.tool_message
            )

    async def run(self):
        self.running = True
        while self.running:
            value = await self.session.prompt_async()
            await self.create_task(value)
            await self.wait_for_task()

    async def create_task(self, value: str):
        if value.startswith(COMMAND_START):
            coro = self.handler_command(value=value[len(COMMAND_START) :])
        else:
            coro = self.handler_generation(value=value)
        self.task = create_task(coro)

    async def handler_command(self, value: str):
        command, *args = value.split(" ")
        await self.commands.execute(command=command, args=args)

    async def handler_generation(self, value: str):
        if value.strip():
            await self.core.start_generation(content=value)
        else:
            await self.core.generation_loop()

    async def wait_for_task(self):
        if not self.task:
            return
        try:
            await self.task
        except (CancelledError, KeyboardInterrupt):
            await self.on_cancell_task()
        except AppClose:
            await self.on_app_close()
        finally:
            await self.clear_task()

    async def on_generation_error(self, event: "CoreGenerationErrorEvent"):
        try:
            raise event.error
        except ConnectionError:
            print_formatted_text("<red>Ha ocurrido en la conexion</red>")
        except Exception:
            await self.print_exception(error=event.error)

    async def print_exception(self, error: Exception):
        traceback = "\n".join(format_exception(error))
        formatted_text = PygmentsTokens(
            list(lex(traceback, lexer=PythonTracebackLexer()))
        )
        style = style_from_pygments_cls(OneDarkStyle)
        print_formatted_text(formatted_text, style=style)

    ### On Start Generation

    async def on_generation_start(self):
        self.content_buffer = ""
        self.live = Live(auto_refresh=False)
        self.live.start()

    async def on_generation_content(self, content: str):
        self.content_buffer += content
        markdown = Markdown(self.content_buffer)
        if not self.live:
            self.live = Live(auto_refresh=False)
            self.live.start()
        if self.live:
            self.live.update(
                Panel(
                    markdown,
                    title="Asistente",
                    padding=1,
                    border_style=Style(color="blue"),
                ),
                refresh=True,
            )

    async def on_generation_end(self):
        if self.live:
            self.live.stop()
            self.live = None

    async def on_cancell_task(self):
        pass

    async def on_app_close(self):
        self.running = False

    async def clear_task(self):
        self.task = None

    async def on_tool_call_start(self, tool_call: "ToolCall"):
        if self.live:
            self.live.stop()
            self.live = None
        match tool_call.function.name:
            case "files_read":
                await render_files_read_tool_call(tool_call=tool_call)
            case "files_write":
                await render_files_write_tool_call(tool_call=tool_call)
            case "os_shell":
                await render_os_shell_tool_call(tool_call=tool_call)
            case "dirs_list":
                await render_dirs_list_tool_call(tool_call=tool_call)
            case _:
                await render_generic_tool_call(tool_call=tool_call)

    async def on_tool_message(self, tool_call: "ToolCall", tool_message: "ToolMessage"):
        match tool_call.function.name:
            case "dirs_list":
                await render_dirs_list_tool_message(
                    tool_call=tool_call, tool_message=tool_message
                )
            case "os_shell":
                await render_os_shell_tool_call(
                    tool_call=tool_call, tool_message=tool_message
                )
            case _:
                await render_generic_tool_message(
                    tool_call=tool_call, tool_message=tool_message
                )

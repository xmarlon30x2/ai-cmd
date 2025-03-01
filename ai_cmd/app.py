from shlex import split
from typing import TYPE_CHECKING

from rich.console import Console

from ai_cmd.exceptions import AppClose

if TYPE_CHECKING:
    from .actions import Actions
    from .engine import Engine


class App:
    running: bool = False
    message: str = "+ "

    def __init__(self, console: Console, actions: "Actions", engine: "Engine"):
        self.console = console
        self.actions = actions
        self.engine = engine

    async def prompt(self) -> str:
        return self.console.input(f"[blue]{self.message}[/blue]")

    async def process(self, *, command: str) -> None:
        command = command.strip()
        if command == "":
            await self.none()
        elif command.startswith("/"):
            action, *args = split(command[1:])
            await self.actions.execute(action=action, args=args)
        else:
            await self.engine.generate(command)

    async def run(self) -> None:
        self.running = True
        try:
            while self.running:
                command = await self.prompt()
                await self.process(command=command)
        except (EOFError, AppClose):
            self.running = False
        finally:
            await self.ending()

    async def none(self):
        pass

    async def ending(self):
        self.console.log("[gray]Cerrando el programa...[/gray]")

import sys
from abc import ABC
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from typer import Typer

from .const import COMMAND_FUNCTION_PREFIX

if TYPE_CHECKING:
    from ...controller.base import Controller
    from ..base import App


@dataclass
class CommandPack(ABC):
    controller: "Controller"
    id: str = field(init=False)

    async def join(self, app: "App") -> None:
        self.app = app

    async def exists(self, *, command: str) -> bool:
        return command in self.scan()

    async def execute(self, *, command: str, args: list[str]) -> None:
        typer = Typer()

        await self.subscribe(typer)
        sys.argv = [command] + args
        try:
            await typer(sys.argv)
        except SystemExit:
            pass

    def scan(self) -> list[str]:
        return [
            attr[len(COMMAND_FUNCTION_PREFIX) :]
            for attr in dir(self)
            if attr.startswith(COMMAND_FUNCTION_PREFIX)
            and attr != COMMAND_FUNCTION_PREFIX
        ]

    async def subscribe(self, typer: Typer):
        for command_name in self.scan():
            command = getattr(self, f"{COMMAND_FUNCTION_PREFIX}{command_name}")
            typer.command(command_name)(command)

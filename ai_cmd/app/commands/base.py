from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from prompt_toolkit import HTML, print_formatted_text

if TYPE_CHECKING:
    from ...controller.base import Controller
    from ..base import App
    from .command_pack import CommandPack

DEFAULT_DISABLEDS: list[str] = []


@dataclass(kw_only=True)
class Commands:
    controller: "Controller"
    command_packs: list["CommandPack"]
    disableds: list[str] = field(default_factory=lambda: DEFAULT_DISABLEDS)

    def join(self, app: "App"):
        self.app = app
        for command_pack in self.command_packs:
            command_pack.join(app=app)

    async def execute(self, *, command: str, args: list[str]) -> None:
        for command_pack in self.command_packs:
            if await command_pack.exists(command=command):
                return await command_pack.execute(command=command, args=args)
        await self.not_found(command=command)

    async def not_found(self, *, command: str):
        print_formatted_text(HTML(f'<red>No se encontro el commando "{command}"</red>'))

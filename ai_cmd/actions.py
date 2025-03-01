from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from rich.console import Console

    from .app import App
    from .pack import Pack


class Actions:
    def __init__(self, *, console: "Console", packs: List["Pack"]):
        self.console = console
        self.packs = packs
    
    async def bind(self, app:'App'):
        for pack in self.packs:
            await pack.bind(app)

    async def execute(self, *, action: str, args: List[str]) -> None:
        for group in self.packs:
            if await group.exists(action=action):
                return await group.execute(action=action, args=args)
        await self.not_found(action=action, args=args)

    async def not_found(self, *, action: str, args: List[str]):
        self.console.print(f'[red]No se encontro el commando "{action}"[/red]')

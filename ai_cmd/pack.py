import sys
from abc import ABC
from typing import TYPE_CHECKING, List

from typer import Typer

if TYPE_CHECKING:
    from .app import App


class Pack(ABC):
    async def bind(self, app: "App"):
        self.app = app

    async def exists(self, *, action: str) -> bool:
        return action in self.scan()

    async def execute(self, *, action: str, args: List[str]) -> None:
        typer = Typer()
        self.collecte(typer)
        sys.argv = [action] + args
        try:
            typer(sys.argv)
        except SystemExit:
            pass

    def scan(self):
        return [attr[3:] for attr in dir(self) if attr.startswith("do_")]

    def collecte(self, typer: Typer):
        for action in self.scan():
            typer.command(action)(getattr(self, f"do_{action}"))

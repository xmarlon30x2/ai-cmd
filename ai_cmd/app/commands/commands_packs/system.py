import sys

from typer import Typer

from ...exceptions import AppClose
from ..command_pack import CommandPack


class SystemPack(CommandPack):
    def do_exit(self):
        """Cierra el programa"""
        raise AppClose()

    async def do_help(self):
        """Muestra ayuda sobre los comandos"""
        typer = Typer()
        for command_pack in self.app.commands.command_packs:
            await command_pack.subscribe(typer)
        sys.argv = ["--help"]
        typer(sys.argv)

import sys

from typer import Typer

from ..exceptions import AppClose
from ..pack import Pack


class BasePack(Pack):
    def do_exit(self):
        """Cierra el programa"""
        raise AppClose()

    def do_help(self):
        """Muestra ayuda sobre los comandos"""
        typer = Typer()
        for pack in self.app.actions.packs:
            pack.collecte(typer)
        sys.argv = ["--help"]
        typer(sys.argv)

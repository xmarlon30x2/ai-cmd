from typing import Any, Callable, Coroutine


from ....utils import wrapped_sync
from ...exceptions import AppClose
from ..command_pack import CommandPack


class SystemPack(CommandPack):
    def do_exit(self):
        """Cierra el programa"""
        raise AppClose()

    async def do_help(self):
        """Muestra ayuda sobre los comandos"""
        command_register: dict[
            str, Callable[[str], None | Coroutine[Any, Any, None]]
        ] = {}
        for pack in self.app.commands.command_packs:
            await pack.subscribe(command_register=command_register)
        for command in command_register.values():
            await wrapped_sync(command, "--help")

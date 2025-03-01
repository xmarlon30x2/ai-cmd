from subprocess import PIPE, run
from typing import Any

from ..tool_pack import ToolPack


class OSPack(ToolPack):
    """Herramientas para manejo del sistema operativo"""

    name = "os"

    async def tool_system(self, command: str) -> Any:
        """
        Ejecuta comandos en la terminal del sistema operativo directamente el la PC del usuario
        args:
            command: Commando a ejecutar
        """
        self.app.console.print(
            f"[yellow]Ejecutando {command if len(command)<20 else command[:20]}[/yellow]"
        )
        output = run(
            command,
            shell=True,
            text=True,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            check=False,
        )
        return {
            "stdout": output.stdout,
            "stderr": output.stderr,
            "returncode": output.returncode,
        }

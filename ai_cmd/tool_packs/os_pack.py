"""OSPack"""

from subprocess import PIPE, run
from typing import Any

from ..tool_pack import ToolPack


class OSPack(ToolPack):
    """Herramientas para manejo del sistema operativo"""

    name = "os"

    async def tool_system(self, command: str) -> Any:
        """
        Ejecuta comandos en la terminal del sistema operativo
        args:
            command: Commando a ejecutar
        """
        output = run(
            command, shell=True, text=True, stdin=PIPE, stdout=PIPE, check=False
        )
        return {
            "stdout": output.stdout,
            "stderr": output.stderr,
            "returncode": output.returncode,
        }

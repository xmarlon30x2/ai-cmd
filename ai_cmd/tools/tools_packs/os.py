from subprocess import PIPE, run
from typing import Any

from ..tool_pack import ToolPack


class OSPack(ToolPack):
    """Herramientas para manejo del sistema operativo"""

    name = "os"

    async def tool_shell(self, command: str) -> Any:
        """
        Ejecuta un comando en la terminal del sistema operativo, permitiendo la interacción directa con el sistema.

        Esta función toma una cadena de texto que representa un comando y la ejecuta directamente en el sistema operativo subyacente.
        Esto permite acceder a funcionalidades del sistema y ejecutar programas externos.

        Args:
            command: El comando a ejecutar como una cadena de texto.

        Returns:
            Un diccionario que contiene:
                stdout: La salida estándar del comando resultante de la ejecución.
                stderr: La salida de error estándar resultante de la ejecución.
                returncode: El código de retorno del comando.
        """
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

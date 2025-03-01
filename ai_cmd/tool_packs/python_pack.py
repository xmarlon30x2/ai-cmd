"""PythonPack"""

from contextlib import redirect_stdout
from io import StringIO
from typing import Any

from ..tool_pack import ToolPack


class PythonPack(ToolPack):
    """Herramientas para el uso de python"""

    name = "python"

    def __init__(self):
        super().__init__()
        self.globals = globals()

    async def tool_reset(self):
        """
        Reinicia las variables globales
        """
        self.globals = {}

    async def tool_exec(self, code: str):
        """
        Ejecuta codigo en un exec de python
        args:
            code: Codigo a ejecutar
        """
        stdout = StringIO()
        executor = exec
        try:
            with redirect_stdout(stdout):
                executor(code, self.globals)
            return {
                "stdout": stdout.getvalue(),
            }
        except Exception as exc:
            return {
                "stdout": stdout.getvalue(),
                "error": str(exc),
                "type_error": type(exc).__name__,
            }

    async def tool_eval(self, code: str) -> Any:
        """
        Evalua expreciones python en un eval
        args:
            code: Codigo a ejecutar
        """
        stdout = StringIO()
        executor = eval
        try:
            with redirect_stdout(stdout):
                value = executor(code, self.globals)
            return {"stdout": stdout.getvalue(), "value": value}
        except Exception as exc:
            return {
                "stdout": stdout.getvalue(),
                "error": str(exc),
                "type_error": type(exc).__name__,
            }

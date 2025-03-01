from contextlib import redirect_stdout
from io import StringIO
from typing import Any

import pip

from ..tool_pack import ToolPack


class PythonPack(ToolPack):
    name = "python"

    def __init__(self):
        super().__init__()
        self.globals = {}

    async def tool_reset(self, confirm: bool):
        """Reinicia las variables globales"""
        if not confirm:
            return {"success": False}
        self.globals = {"app": self.app}
        return {"success": True}

    async def tool_exec(self, code: str):
        """Ejecuta código Python en el entorno global directamente en la PC del usuario.

        Args:
            code (str): El código Python a ejecutar.

        Returns:
            dict: Un diccionario con la salida estándar (stdout) del código ejecutado en la clave 'stdout'.
                  Si ocurre un error, también incluye las claves 'error' (el mensaje de error) y 'type_error' (el tipo de error).
        """
        stdout = StringIO()
        executor = exec
        try:
            with redirect_stdout(stdout):
                executor(code, self.globals)
            return {"stdout": stdout.getvalue()}
        except Exception as exc:
            return {
                "stdout": stdout.getvalue(),
                "error": str(exc),
                "type_error": type(exc).__name__,
            }

    async def tool_eval(self, code: str) -> Any:
        """Evalúa una expresión Python en el entorno global directamente en la PC del usuario.

        Args:
            expresion (str): La expresión Python a evaluar.

        Returns:
            dict: Un diccionario con la salida estándar (stdout) en la clave 'stdout' y el resultado de la evaluación en la clave 'value'.
                  Si ocurre un error, también incluye las claves 'error' (el mensaje de error) y 'type_error' (el tipo de error).
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

    async def _tool_pip(self, args: list[str]):
        """Utiliza pip mediante argumentos

        Args:
            args (list): Lista de argumentos, por ejemplo ['install', 'package']

        """
        stdout = StringIO()
        try:
            with redirect_stdout(stdout):
                pip.main(args)
            return {"stdout": stdout.getvalue()}
        except Exception as exc:
            return {
                "stdout": stdout.getvalue(),
                "error": str(exc),
            }

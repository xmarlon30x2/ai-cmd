from contextlib import redirect_stdout
from io import StringIO
from traceback import format_exception

from ..tool_pack import ToolPack


class AppPack(ToolPack):
    name = "app"

    async def tool_mod(self, code: str):
        """Ejecuta codigo python dentro de la aplicacion.
        Tienes acceso a la aplicacion mediante la
        variable ROOT
        args:
            code: codigo a ejecutar
        """
        globals_ = globals()
        globals_["ROOT"] = self.controller
        stdout = StringIO()
        try:
            with redirect_stdout(stdout):
                exec(code, globals_)
        except Exception as exc:
            return {
                "stdout": stdout.getvalue(),
                "traceback": "\n".join(format_exception(exc)),
            }
        return {"stdout": stdout.getvalue()}

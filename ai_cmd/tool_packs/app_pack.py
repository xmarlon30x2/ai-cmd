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
        globals_["ROOT"] = self.app
        exec(code, globals_)

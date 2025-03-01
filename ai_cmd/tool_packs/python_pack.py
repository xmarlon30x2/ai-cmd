from typing import Any


from ..executors import PythonProgram

from ..tool_pack import ToolPack


class PythonPack(ToolPack):
    name = "python"

    def __init__(self):
        super().__init__()
        self.programs: dict[str, tuple[str, PythonProgram]] = {}

    async def tool_execute(self, code: str, description: str):
        """
        Ejecuta codigo python en un subproceso
        args:
            code: Codigo python a ejecutar
            description: Descripcion breve del codigo
        """
        try:
            program = PythonProgram(code=code)
            program.start()
            self.programs[program.id] = (description, program)
            return {"id": program.id}
        except Exception as exc:
            return {"error": str(exc)}

    async def tool_list(self, confirm: bool) -> dict[Any, Any]:
        """Muestar la lista de programas python disponibles"""
        if not confirm:
            return {"success": False}
        return {
            "programs": [
                {"id": id, "description": desc, "return_code": prog.return_code}
                for (id, (desc, prog)) in self.programs.items()
            ]
        }

    async def tool_comunicate(self, id: str, input: str = "", timeout: float = 0):
        """
        Interactua con un codigo python en ejecucion, enviando datos al stdin,
        espera a que el proceso termine y lee datos del stdout y stderr.
        args:
            id: La id del codigo en ejecucion
            input: El texto que se enviara al stdin, es opcional.
            timeout: El tiempo maximo de espera para que el proceso termine, utiliza 0 para indicar tiempo indefinido
        """
        data = self.programs.pop(id)
        if data:
            _, program = data
            try:
                stdin, stdout = program.comunicate(
                    input=input if input != "" else None,
                    timeout=timeout if timeout != 0 else None,
                )
            except Exception as exc:
                return {"error": str(exc)}
            else:
                return {"stdin": stdin, "stdout": stdout}
        else:
            return {"error": f'ID "{id}" no encontrada'}

    async def tool_kill(self, id: str):
        """Fuerza el cierre de un programa python en ejecucion"""
        data = self.programs.pop(id)
        if data:
            _, program = data
            try:
                program.kill()
            except Exception as exc:
                return {"error": str(exc)}
        else:
            return {"error": f'ID "{id}" no encontrada'}

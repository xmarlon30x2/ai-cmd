from asyncio import Lock
from json import dumps
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .tool_pack import ToolPack
    from .types import Tool, ToolCall, ToolMessage


class ToolHandler:
    """Controlador de herramientas"""

    def __init__(self, tool_packs: Optional[List["ToolPack"]] = None) -> None:
        self._tool_packs = tool_packs or []
        self._tool_packs_lock = Lock()

    async def add(self, tool_packs: List["ToolPack"]):
        """Agrega paquetes de herramientas"""
        names = map(lambda tool_pack: tool_pack.name, tool_packs)
        async with self._tool_packs_lock:
            installed_names = map(lambda tool_pack: tool_pack.name, self._tool_packs)
            repeats = list(filter(lambda name: name in installed_names, names))
            if repeats:
                raise KeyError(f'los paquetes {",".join(repeats)} ya existen')
            self._tool_packs.extend(tool_packs)

    async def pop(self, name: str):
        """Elimina una herramienta"""
        async with self._tool_packs_lock:
            tool_pack_query = list(
                filter(lambda tool_pack: tool_pack.name == name, self._tool_packs)
            )
            if not tool_pack_query:
                raise KeyError(f'No se encontro ningun paquete con el nombre "{name}"')
            tool_pack = tool_pack_query[0]
            self._tool_packs.remove(tool_pack)

    async def execute(self, tool_call: "ToolCall") -> "ToolMessage":
        """Ejecuta una herramienta"""
        try:
            match tool_call.type:
                case "function":
                    tool_pack = None
                    async with self._tool_packs_lock:
                        for element in self._tool_packs:
                            if await element.exists(tool_call.function.name):
                                tool_pack = element
                                break
                    if not tool_pack:
                        tool_message: "ToolMessage" = {
                            "content": dumps(
                                {
                                    "error": f"Herramienta '{tool_call.function.name}' no registrada"
                                }
                            ),
                            "name": "error_handler",
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                        }
                        return tool_message
                    return await tool_pack.execute(tool_call)
        except Exception as exc:
            return {
                "content": dumps({"error": f"Error procesando tool_call: {str(exc)}"}),
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": "error_handler",
            }

    async def reset(self) -> None:
        """Reinicia todas las herramientas"""
        async with self._tool_packs_lock:
            for tool_pack in self._tool_packs:
                await tool_pack.reset()

    async def specs(self) -> List["Tool"]:
        """Obtiene la especificaion de las herramientas"""
        specs: List["Tool"] = []
        async with self._tool_packs_lock:
            for tool_pack in self._tool_packs:
                specs.extend(await tool_pack.specs())
        return specs

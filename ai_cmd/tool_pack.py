from json import JSONDecodeError, dumps, loads
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Dict, List, Tuple, TypedDict

from .specs import FunctionSpec

if TYPE_CHECKING:
    from .types import FunctionCall, Tool, ToolCall, ToolMessage

    class RegTool(TypedDict):
        callable: Callable[..., Any]
        spec: Tool


class ToolPack:
    """Paquete de herramientas"""

    name: str = "tool"

    def __init__(self):
        self._tools = self._collecte()

    def _collecte(self):
        tools: Dict[str, "RegTool"] = {}
        for key, element in self._items():
            if isinstance(element, Callable):
                name = f"{self.name}_{key}"
                spec = FunctionSpec.generate(element, name)  # type: ignore
                tools[name] = {"callable": element, "spec": spec}
        return tools

    def _items(self) -> List[Tuple[str, Any]]:
        return [
            (key[5:], getattr(self, key))
            for key in dir(self)
            if key.startswith("tool_")
        ]

    async def specs(self) -> List["Tool"]:
        """Obtiene la especificaion de las herramientas"""
        return list(map(lambda tool: tool["spec"], self._tools.values()))

    async def exists(self, tool_name: str):
        """Comprueba si el nombre de una herramienta existe"""
        return tool_name in self._tools

    async def execute(self, tool_call: "ToolCall") -> "ToolMessage":
        """Ejecuta una herramienta"""
        content = {"message": "Sin datos que mostrar"}
        match tool_call.type:
            case "function":
                content = await self._execute_function(tool_call.function)
            case _:
                raise KeyError(f'Tipo de herramienta "{tool_call.type}" no es valido')
        return {
            "role": "tool",
            "content": dumps(content, ensure_ascii=False),
            "tool_call_id": tool_call.id,
            "name": tool_call.function.name,
        }

    async def _execute_function(self, function: "FunctionCall") -> Any:
        reg_tool = self._tools[function.name]
        try:
            parameters = loads(function.arguments)
        except JSONDecodeError:
            parameters = {}
        required = reg_tool["spec"]["function"]["parameters"]["required"]
        missing: List[str] = [p for p in required if p not in parameters]  # type: ignore
        if missing:
            return {
                "error": f"Parámetros faltantes: {', '.join(missing)}",
                "error_type": "TypeError",
            }
        try:
            value = reg_tool["callable"](**parameters)
            if isinstance(value, Coroutine):
                value: Any = await value
            return value or {"success": True}
        except Exception as exc:  # type: ignore
            return {"error": str(exc), "error_type": type(exc).__name__}

    async def reset(self) -> Any:
        """Reinicia el paquete de herramientas"""
        raise NotImplementedError()

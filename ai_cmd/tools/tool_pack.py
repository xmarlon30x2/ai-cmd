from typing import TYPE_CHECKING, Any, Callable, Coroutine, Dict

from ..utils import load_safe_json, wrapped_sync
from ..window.base import Window
from .schemas.generators import FunctionSchemaGenerator
from .types import Tool, ToolCall

if TYPE_CHECKING:
    from ..controller.base import Controller


class ToolPack:
    """A pack of tools."""

    name: str = "tool"
    custom_descs: dict[str, str] = {}

    def __init__(self, controller: "Controller", window: "Window"):
        self.controller = controller
        self.window = window
        self._tools: list[Tool] = self._collect_tools()

    async def tools(self) -> list["Tool"]:
        """Get all tools."""
        return self._tools

    async def exists(self, tool_name: str) -> bool:
        """Checks if a tool with the given name exists."""
        tool = self._get_tool(tool_name=tool_name)
        return True if tool else False

    async def execute(self, tool_call: "ToolCall") -> Dict[str, Any]:
        """Executes a tool.

        Args:
            tool_call (ToolCall): The tool call object.

        Returns:
            dict[str, Any]: The result of the tool execution.
        """
        tool = self._get_tool(tool_name=tool_call.function.name)
        if not tool:
            return {"error": f"Tool '{tool_call.function.name}' not found."}

        parameters, missing = self._transform_arguments(
            arguments=tool_call.function.arguments,
            required=tool.function.parameters.get("required", []),
        )
        if missing:
            return {"error": f"Missing parameters: {', '.join(missing)}"}

        try:
            value = await wrapped_sync(tool.function.callable, **parameters)
            return await self._as_dict(value)
        except Exception as e:
            return {"error": str(e), "error_type": type(e).__name__}

    async def reset(self) -> None:
        """Resets the tool pack."""
        pass

    async def _as_dict(self, value: Any) -> dict[str, Any]:
        data: Any = (await value) if isinstance(value, Coroutine) else value
        if isinstance(data, dict):
            return value  # type: ignore
        else:
            return {"success": True}

    def _get_tool(self, tool_name: str) -> "Tool | None":
        for tool in self._tools:
            if tool.function.name == tool_name:
                return tool
        return None

    def _get_tool_methods(self) -> list[tuple[str, Any]]:
        """Gets all methods starting with 'tool_'."""
        return [
            (key[5:], getattr(self, key))
            for key in dir(self)
            if key.startswith("tool_")
        ]

    def _transform_arguments(
        self, arguments: str, required: list[str]
    ) -> tuple[dict[str, Any], list[str]]:
        parameters = load_safe_json(arguments=arguments)
        missing = [p for p in required if p not in parameters]
        return parameters, missing

    def _collect_tools(self) -> list["Tool"]:
        """Collects tools from the tool pack."""
        tools: list[Tool] = []
        for key, element in self._get_tool_methods():
            if isinstance(element, Callable):
                name = f"{self.name}_{key}"
                function_schema = FunctionSchemaGenerator.generate(
                    function=element, custom_name=name, custom_desc=self.custom_descs.get(name, None)  # type: ignore
                )
                tools.append(Tool(function=function_schema))
        return tools

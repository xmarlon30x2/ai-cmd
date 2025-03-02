from dataclasses import dataclass, field
from json import dumps
from typing import TYPE_CHECKING

from ai_cmd.tools.events import (
    ToolsExecuteEndEvent,
    ToolsExecuteStartEvent,
    ToolsListEvent,
    ToolsRegistryAddEvent,
    ToolsRegistryRemoveEvent,
    ToolsResetEvent,
    ToolsStateDisableEvent,
    ToolsStateEnableEvent,
)

from ..core.history.types import ToolMessage

if TYPE_CHECKING:
    from ..controller.base import Controller
    from .tool_pack import ToolPack
    from .types import Tool, ToolCall

DEFAULT_DISABLEDS: list[str] = []


@dataclass(kw_only=True)
class Tools:
    """Handles multiple tool packs."""

    controller: "Controller"
    tool_packs: list["ToolPack"]
    disableds: list[str] = field(default_factory=lambda: DEFAULT_DISABLEDS)

    async def add(self, tool_pack: "ToolPack") -> None:
        """Add tool pack to the handler."""
        event = ToolsRegistryAddEvent(tools=self, tool_pack=tool_pack)
        await self.controller.trigger(event=event)
        for tp in self.tool_packs:
            if tool_pack.name == tp.name:
                raise ValueError(
                    f"ToolPack with name '{tool_pack.name}' already exists."
                )
        self.tool_packs.append(tool_pack)

    async def list(self) -> list["Tool"]:
        """Get all tools enableds."""
        tools: list["Tool"] = []
        for tool_pack in self.tool_packs:
            if not tool_pack.name in self.disableds:
                tools.extend(await tool_pack.tools())
        event = ToolsListEvent(tools=self, list=tools)
        await self.controller.trigger(event=event)
        return tools

    async def disable(self, name: str):
        for tp in self.tool_packs:
            if name == tp.name:
                if not name in self.disableds:
                    event = ToolsStateDisableEvent(tools=self, name=name)
                    await self.controller.trigger(event=event)
                    self.disableds.append(name)
                return
        raise ValueError(f"ToolPack with name '{name}' not found.")

    async def enable(self, name: str):
        for tp in self.tool_packs:
            if name == tp.name:
                if name in self.disableds:
                    event = ToolsStateEnableEvent(tools=self, name=name)
                    await self.controller.trigger(event=event)
                    self.disableds.remove(name)
                return
        raise ValueError(f"ToolPack with name '{name}' not found.")

    async def reset(self) -> None:
        """Resets all tool packs."""
        event = ToolsResetEvent(tools=self)
        await self.controller.trigger(event=event)
        for tool_pack in self.tool_packs:
            await tool_pack.reset()

    async def remove(self, name: str) -> None:
        """Removes a tool pack from the handler."""
        event = ToolsRegistryRemoveEvent(tools=self, name=name)
        await self.controller.trigger(event=event)
        self.tool_packs = [tp for tp in self.tool_packs if tp.name != name]
        if name in self.disableds:
            self.disableds.remove(name)

    async def execute(self, tool_call: "ToolCall") -> ToolMessage:
        """Executes a tool.

        Args:
            tool_call (ToolCall): The tool call object.

        Returns:
            ToolMessage: A message of the tool execution.
        """
        event = ToolsExecuteStartEvent(tools=self, tool_call=tool_call)
        await self.controller.trigger(event=event)
        tool_pack = None
        name: None | str = None
        try:
            for element in self.tool_packs:
                if await element.exists(tool_name=tool_call.function.name):
                    tool_pack = element
                    break
            if not tool_pack:
                content = {
                    "error": f"Herramienta '{tool_call.function.name}' no registrada"
                }
            else:
                content = await tool_pack.execute(tool_call=tool_call)
        except Exception as exc:
            name = "error_handler"
            content = {"error": f"Error procesando la llamada: {str(exc)}"}
        tool_message = ToolMessage(
            content=dumps(obj=content),
            name=name,
            tool_call_id=tool_call.id,
        )
        event = ToolsExecuteEndEvent(
            tools=self, tool_call=tool_call, tool_message=tool_message
        )
        await self.controller.trigger(event=event)
        return tool_message

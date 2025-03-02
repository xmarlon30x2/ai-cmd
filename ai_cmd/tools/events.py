"""
- ToolsEvent
    - ToolsRegistryEvent
        - ToolsRegistryAddEvent
        - ToolsRegistryRemoveEvent
    - ToolsStateEvent
        - ToolsStateEnableEvent
        - ToolsStateDisableEvent
    - ToolsExecuteEvent
        - ToolsExecuteStartEvent
        - ToolsExecuteEndEvent
    - ToolsResetEvent
    - ToolsListEvent
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..controller.types import Event

if TYPE_CHECKING:
    from ..core.history.types import ToolMessage
    from .base import Tools
    from .tool_pack import ToolPack
    from .types import Tool, ToolCall


@dataclass(kw_only=True)
class ToolsEvent(Event):
    """Evento de Tools"""

    tools: "Tools"
    type: str = field(default="tools")


@dataclass(kw_only=True)
class ToolsRegistryEvent(ToolsEvent):
    """Evento del registro de Tools"""

    type: str = field(default="tools_registry")


@dataclass(kw_only=True)
class ToolsRegistryAddEvent(ToolsRegistryEvent):
    """Se agrego un elemento al registro de Tools"""

    tool_pack: "ToolPack"
    type: str = field(default="tools_registry_add")


@dataclass(kw_only=True)
class ToolsRegistryRemoveEvent(ToolsRegistryEvent):
    """Se elimino un elemento al registro de Tools"""

    name: str
    type: str = field(default="tools_registry_remove")


@dataclass(kw_only=True)
class ToolsStateEvent(ToolsEvent):
    """Evento del estado de Tools"""

    name: str
    type: str = field(default="tools_state")


@dataclass(kw_only=True)
class ToolsStateEnableEvent(ToolsStateEvent):
    """Avilitacion de una Tools"""

    name: str
    type: str = field(default="tools_state_enable")


@dataclass(kw_only=True)
class ToolsStateDisableEvent(ToolsStateEvent):
    """Desabilitacion de una Tools"""

    name: str
    type: str = field(default="tools_state_disable")


@dataclass(kw_only=True)
class ToolsExecuteEvent(ToolsEvent):
    """Evento ejecucion de Tools"""

    tool_call: "ToolCall"
    type: str = field(default="tools_execute")


@dataclass(kw_only=True)
class ToolsExecuteStartEvent(ToolsExecuteEvent):
    """Evento de inicio ejecucion de Tools"""

    tool_call: "ToolCall"
    type: str = field(default="tools_execute_start")


@dataclass(kw_only=True)
class ToolsExecuteEndEvent(ToolsExecuteEvent):
    """Evento de final de ejecucion de Tools"""

    tool_call: "ToolCall"
    tool_message: "ToolMessage"
    type: str = field(default="tools_execute_end")


@dataclass(kw_only=True)
class ToolsResetEvent(ToolsEvent):
    """Evento reinicio de Tools"""

    type: str = field(default="tools_reset")


@dataclass(kw_only=True)
class ToolsListEvent(ToolsEvent):
    """Evento listado de Tools"""

    list: list["Tool"]
    type: str = field(default="tools_list")

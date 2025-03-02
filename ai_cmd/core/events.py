"""
- CoreEvent
    - CoreGenerationEvent
        - CoreGenerationStartEvent
        - CoreGenerationRecvTokenEvent
            - CoreGenerationRecvContentTokenEvent
            - CoreGenerationRecvToolsCallsTokenEvent
        - CoreGenerationErrorEvent
        - CoreGenerationEndEvent
    - CoreToolsEvent
        - CoreToolsLoadingEvent
        - CoreToolsExecuteEvent
            - CoreToolsExecuteStartEvent
            - CoreToolsExecuteEndEvent
    
    - CoreResetEvent
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..controller.types import Event

if TYPE_CHECKING:
    from ..ai.types import ContentToken, Token, ToolsCallsToken
    from ..tools.types import ToolCall
    from .base import Core
    from .history.types import AssistantMessage, ToolMessage


@dataclass(kw_only=True)
class CoreEvent(Event):
    """Evento base de Core"""

    core: "Core"
    type: str = field(default="core")


@dataclass(kw_only=True)
class CoreGenerationEvent(CoreEvent):
    """Event de generacion de Core"""

    type: str = field(default="core_generation")


@dataclass(kw_only=True)
class CoreGenerationStartEvent(CoreGenerationEvent):
    """Se inicia la generacion"""

    type: str = field(default="core_generation_start")


@dataclass(kw_only=True)
class CoreGenerationRecvTokenEvent(CoreGenerationEvent):
    """Recivo de un token"""

    token: "Token"
    message: "AssistantMessage"
    type: str = field(default="core_generation_recv_token")


@dataclass(kw_only=True)
class CoreGenerationRecvContentTokenEvent(CoreGenerationRecvTokenEvent):
    """Recivo de un token de contenido"""

    token: "ContentToken"  # type: ignore
    type: str = field(default="core_recv_content_token")


@dataclass(kw_only=True)
class CoreGenerationRecvToolsCallsTokenEvent(CoreGenerationRecvTokenEvent):
    """Recivo de un token de llamada de herramientas"""

    token: "ToolsCallsToken"  # type: ignore
    type: str = field(default="core_recv_tools_calls_token")


@dataclass(kw_only=True)
class CoreGenerationErrorEvent(CoreGenerationEvent):
    """Se cancela la generacion"""

    error: Exception
    type: str = field(default="core_generation_error")


@dataclass(kw_only=True)
class CoreGenerationEndEvent(CoreGenerationEvent):
    """Se termina la generacion"""

    type: str = field(default="core_generation_end")


@dataclass(kw_only=True)
class CoreToolsEvent(CoreEvent):
    """Event de herramientas de Core"""

    type: str = field(default="core_tools")


@dataclass(kw_only=True)
class CoreToolsLoadingEvent(CoreToolsEvent):
    """Cargando herramientas de Core"""

    type: str = field(default="core_tools_loading")


@dataclass(kw_only=True)
class CoreToolsExecuteEvent(CoreToolsEvent):
    """Ejecutando herramientas de Core"""

    type: str = field(default="core_tools_execute")


@dataclass(kw_only=True)
class CoreToolsExecuteStartEvent(CoreToolsExecuteEvent):
    """Inicio de la ejecucion de herramientas de Core"""

    tool_call: "ToolCall"
    type: str = field(default="core_tools_execute_start")


@dataclass(kw_only=True)
class CoreToolsExecuteEndEvent(CoreToolsExecuteEvent):
    """Inicio de la ejecucion de herramientas de Core"""

    tool_call: "ToolCall"
    tool_message: "ToolMessage"
    type: str = field(default="core_tools_execute_end")


@dataclass(kw_only=True)
class CoreResetEvent(CoreEvent):
    """Event de reinicio del core"""

    type: str = field(default="core_reset")

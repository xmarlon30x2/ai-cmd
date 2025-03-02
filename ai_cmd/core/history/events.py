"""
- HistoryEvent
    - HistoryMessageEvent
        - HistoryMessageAddEvent
            - HistoryMessageAddUserEvent
            - HistoryMessageAddAssistantEvent
            - HistoryMessageAddSystemEvent
            - HistoryMessageAddToolEvent
    - HistoryResetEvent
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ...controller.types import Event

if TYPE_CHECKING:
    from .base import History
    from .types import (
        AssistantMessage,
        Message,
        SystemMessage,
        ToolMessage,
        UserMessage,
    )


@dataclass(kw_only=True)
class HistoryEvent(Event):
    """Event de History"""

    history: "History"
    type: str = field(default="history")


@dataclass(kw_only=True)
class HistoryMessageEvent(HistoryEvent):
    """Event de mesage de History"""

    type: str = field(default="history_message")


@dataclass(kw_only=True)
class HistoryMessageAddEvent(HistoryMessageEvent):
    """Se agrego un mensaje de History"""

    message: "Message"
    type: str = field(default="history_message_add")


@dataclass(kw_only=True)
class HistoryMessageAddUserEvent(HistoryMessageAddEvent):
    """Se agrego un mensaje del user de History"""

    message: "UserMessage"  # type: ignore
    type: str = field(default="history_message_add_user")


@dataclass(kw_only=True)
class HistoryMessageAddAssistantEvent(HistoryMessageAddEvent):
    """Se agrego un mensaje del assistant de History"""

    message: "AssistantMessage"  # type: ignore
    type: str = field(default="history_message_add_assistant")


@dataclass(kw_only=True)
class HistoryMessageAddToolEvent(HistoryMessageAddEvent):
    """Se agrego un mensaje del tool de History"""

    message: "ToolMessage"  # type: ignore
    type: str = field(default="history_message_add_tool")


@dataclass(kw_only=True)
class HistoryMessageAddSystemEvent(HistoryMessageAddEvent):
    """Se agrego un mensaje del system de History"""

    message: "SystemMessage"  # type: ignore
    type: str = field(default="history_message_add_system")


@dataclass(kw_only=True)
class HistoryResetEvent(HistoryEvent):
    """Event de reinicio de History"""

    type: str = field(default="history_reset")

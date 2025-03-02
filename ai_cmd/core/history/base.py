from dataclasses import dataclass
from typing import TYPE_CHECKING

from .events import (
    HistoryMessageAddAssistantEvent,
    HistoryMessageAddSystemEvent,
    HistoryMessageAddToolEvent,
    HistoryMessageAddUserEvent,
    HistoryResetEvent,
)

if TYPE_CHECKING:
    from ...controller.base import Controller
    from .types import (
        AssistantMessage,
        Message,
        SystemMessage,
        ToolMessage,
        UserMessage,
    )


@dataclass(kw_only=True)
class History:
    controller: "Controller"
    messages: list["Message"]

    async def reset(self) -> None:
        event = HistoryResetEvent(history=self)
        await self.controller.trigger(event=event)
        self.messages = []

    async def add_user_message(self, message: "UserMessage") -> None:
        event = HistoryMessageAddUserEvent(history=self, message=message)
        await self.controller.trigger(event=event)
        self.messages.append(message)

    async def add_assistant_message(self, message: "AssistantMessage") -> None:
        event = HistoryMessageAddAssistantEvent(history=self, message=message)
        await self.controller.trigger(event=event)
        self.messages.append(message)

    async def add_tool_message(self, message: "ToolMessage") -> None:
        event = HistoryMessageAddToolEvent(history=self, message=message)
        await self.controller.trigger(event=event)
        self.messages.append(message)

    async def add_system_message(self, message: "SystemMessage") -> None:
        event = HistoryMessageAddSystemEvent(history=self, message=message)
        await self.controller.trigger(event=event)
        self.messages.append(message)

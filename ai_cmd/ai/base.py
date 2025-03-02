from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, AsyncGenerator

if TYPE_CHECKING:
    from ..core.history.types import Message
    from ..tools.types import Tool
    from .types import Token


class AI(ABC):
    temperature: float
    model: str

    @abstractmethod
    async def chat(
        self, messages: list["Message"], tools: list["Tool"]
    ) -> AsyncGenerator["Token", Any]: ...

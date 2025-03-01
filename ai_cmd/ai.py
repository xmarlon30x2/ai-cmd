from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, AsyncGenerator, List

if TYPE_CHECKING:
    from .types import Message, Token, Tool


class AI(ABC):
    temperature: float
    model: str

    @abstractmethod
    async def chat(
        self, messages: List["Message"], tools: List["Tool"]
    ) -> AsyncGenerator["Token", Any]: ...

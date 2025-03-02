from abc import ABC, abstractmethod


class Window(ABC):
    @abstractmethod
    async def prompt(self, message: str) -> str: ...

    @abstractmethod
    async def prompt_secret(self, message: str) -> str: ...

    @abstractmethod
    async def confirm(self, message: str) -> bool: ...

import sys
from abc import ABC
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Optional, Type

from ...utils import wrapped_sync
from .const import COMMAND_FUNCTION_PREFIX
from .parser import dynamic_converter

if TYPE_CHECKING:
    from ...controller.base import Controller
    from ..base import App


@dataclass
class CommandPack(ABC):
    controller: "Controller"
    id: str = field(init=False)
    converters: Optional[dict[Type[Any], Callable[..., Any]]] = None

    def join(self, app: "App") -> None:
        self.app = app

    async def exists(self, *, command: str) -> bool:
        return command in self.scan()

    async def execute(self, *, command: str, args: list[str]) -> None:
        command_register: dict[
            str, Callable[[str], None | Coroutine[Any, Any, None]]
        ] = {}

        await self.subscribe(command_register)
        sys.argv = [command] + args
        try:
            callable = command_register[command]
            await wrapped_sync(callable, " ".join(args))
        except SystemExit:
            pass

    def scan(self) -> list[str]:
        return [
            attr[len(COMMAND_FUNCTION_PREFIX) :]
            for attr in dir(self)
            if attr.startswith(COMMAND_FUNCTION_PREFIX)
            and attr != COMMAND_FUNCTION_PREFIX
        ]

    async def subscribe(
        self,
        command_register: dict[str, Callable[[str], None | Coroutine[Any, Any, None]]],
    ):
        for command_name in self.scan():
            function = getattr(self, f"{COMMAND_FUNCTION_PREFIX}{command_name}")
            command = dynamic_converter(converters=self.converters, name=command_name)(
                function
            )
            command_register[command_name] = command

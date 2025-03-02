from asyncio import sleep
from typing import TYPE_CHECKING, Any, AsyncGenerator

from ...ai.base import AI
from ...ai.types import ContentToken, Token
from ...tools.types import Tool

if TYPE_CHECKING:

    from ...core.history.types import Message

tokens_1 = "Okay la ecuacion es x**2 + 2 para x = 1. entoces seria (1)**2 + 2 resultante en 1*1+2 entonces 1 * 1 = 1 y 1 + 2 es igual a 3. Por tanto el resultado es 3".split(
    " "
)
tokens_2 = "Okay si al resultado le restamos 3 seria r - 3 que seria 3 - 3 que es igaul a 0. El resultado es 0".split(
    " "
)


class MockReasonerAI(AI):
    def __init__(self, *_: Any, **_1: Any):
        self.flag = 0

    async def chat(
        self,
        messages: list["Message"],
        tools: list[Tool],
    ) -> AsyncGenerator[Token, Any]:
        if not self.flag:
            self.flag = 1
            for token in tokens_1:
                yield ContentToken(token + " ")
                await sleep(0.2)
        elif self.flag == 1:
            self.flag = 0
            for token in tokens_2:
                yield ContentToken(token + " ")
                await sleep(0.2)

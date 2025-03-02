from asyncio import sleep
from typing import TYPE_CHECKING, Any, AsyncGenerator

from ...ai.base import AI
from ...ai.types import ContentToken, Token, ToolsCallsToken
from ...tools.types import FunctionCall, Tool, ToolCall

if TYPE_CHECKING:

    from ...core.history.types import Message


class MockAI(AI):
    def __init__(self):
        self.flag = 0

    async def chat(
        self,
        messages: list["Message"],
        tools: list[Tool],
    ) -> AsyncGenerator[Token, Any]:
        if not self.flag:
            self.flag = 1
            await sleep(0.2)
            yield ContentToken("Ahora")
            await sleep(0.2)
            yield ContentToken(" mismo")
            await sleep(0.2)
            yield ContentToken(" lo")
            await sleep(0.2)
            yield ContentToken(" hago")
            await sleep(0.2)
            yield ToolsCallsToken(
                tools_calls=[
                    ToolCall(
                        id="random-id",
                        function=FunctionCall(
                            name="files_read", arguments='{"path":"D:/readme.md"}'
                        ),
                    )
                ]
            )
            await sleep(0.2)
        elif self.flag == 1:
            self.flag = 2
            await sleep(0.2)
            yield ContentToken("El")
            await sleep(0.2)
            yield ContentToken(" archivo")
            await sleep(0.2)
            yield ContentToken(" no")
            await sleep(0.2)
            yield ContentToken(" existe")
            await sleep(0.2)
            yield ContentToken(" quieres")
            await sleep(0.2)
            yield ContentToken(" que")
            await sleep(0.2)
            yield ContentToken(" busque")
            await sleep(0.2)
            yield ContentToken(" nombres")
            await sleep(0.2)
            yield ContentToken(" similares")
            await sleep(0.2)
            yield ContentToken(" en")
            await sleep(0.2)
            yield ContentToken(" ese")
            await sleep(0.2)
            yield ContentToken(" directorio?")
            await sleep(0.2)
        elif self.flag == 2:
            self.flag = 3
            await sleep(0.2)
            yield ToolsCallsToken(
                tools_calls=[
                    ToolCall(
                        id="random-id",
                        function=FunctionCall(
                            name="dirs_list", arguments='{"path":"D:/"}'
                        ),
                    )
                ]
            )
            await sleep(0.2)
            yield ContentToken("No hay nada")
            await sleep(0.2)
            yield ContentToken(" ahi")
            await sleep(0.2)
        elif self.flag == 3:
            self.flag = 0
            await sleep(0.2)
            yield ContentToken("Revisa la")
            await sleep(0.2)
            yield ContentToken(" ruta")
            await sleep(0.2)
            yield ContentToken(" ruta")
            await sleep(0.2)
            yield ContentToken(" ruta")
            await sleep(0.2)
            yield ContentToken(" \n")
            await sleep(0.2)
            yield ContentToken(" ruta")
            await sleep(0.2)
            yield ContentToken(" ruta")
            await sleep(0.2)
            yield ContentToken(" ruta")
            await sleep(0.2)
            yield ContentToken(" ruta")
            await sleep(0.2)
            yield ContentToken(" ruta")
            await sleep(0.2)
            yield ContentToken(" ruta")
            await sleep(0.2)

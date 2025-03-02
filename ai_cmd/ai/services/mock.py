from asyncio import sleep
from typing import TYPE_CHECKING, Any, AsyncGenerator

from ...ai.base import AI
from ...ai.types import ContentToken, Token, ToolsCallsToken
from ...tools.types import FunctionCall, Tool, ToolCall

if TYPE_CHECKING:
    from ...core.history.types import Message

tokens_1 = (
    "Voy a buscar, en caso de no encotrar el archivo resolvere la ecuacion".split(" ")
)

tool_calls_1 = ToolsCallsToken(
    tools_calls=[
        ToolCall(
            id="random-id",
            function=FunctionCall(name="dirs_list", arguments='{"path":"D:/"}'),
        )
    ]
)
tokens_2 = "No se encontro el archivo, voy a resolver la ecuacion".split(" ")

tool_calls_2 = ToolsCallsToken(
    tools_calls=[
        ToolCall(
            id="random-ai-reasoner",
            function=FunctionCall(
                name="ai_reasoner_talk",
                arguments='{"content":"Resuelve esta ecuacion x ** 2 + 2 para x = 1"}',
            ),
        )
    ]
)

tokens_3 = "El resultado es 3".split(" ")

tool_calls_4 = ToolsCallsToken(
    tools_calls=[
        ToolCall(
            id="random-ai-reasoner",
            function=FunctionCall(
                name="ai_reasoner_talk",
                arguments='{"content":"Y si restas 3 al resultado?"}',
            ),
        )
    ]
)


tokens_5 = "Si restas 3 queda 0".split(" ")


class MockAI(AI):
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
            yield tool_calls_1
        elif self.flag == 1:
            self.flag = 2
            for token in tokens_2:
                yield ContentToken(token + " ")
                await sleep(0.2)
            yield tool_calls_2
        elif self.flag == 2:
            self.flag = 3
            for token in tokens_3:
                yield ContentToken(token + " ")
                await sleep(0.2)
        elif self.flag == 3:
            self.flag = 4
            yield tool_calls_4
        elif self.flag == 4:
            self.flag = 0
            for token in tokens_5:
                yield ContentToken(token + " ")
                await sleep(0.2)

from typing import Any, AsyncGenerator
from uuid import uuid4

from ..ai import AI
from ..types import ContentToken, FunctionCall, Token, ToolCall, ToolsCallsToken


class MockAI(AI):
    def __init__(self, model: str, temperature: float):
        self.model = model
        self.temperature = temperature
        self.flag = 0

    async def chat(self, *_args: Any, **_kwargs: Any) -> AsyncGenerator[Token, Any]:
        if self.flag == 0:
            self.flag = 1
            yield ContentToken(type="content", content="Hola")
            yield ContentToken(type="content", content=" como")
            yield ToolsCallsToken(
                type="tools",
                tools_calls=[
                    ToolCall(
                        id=str(uuid4()),
                        type="function",
                        function=FunctionCall(
                            name="file_read", arguments='{"path":"D:/readme.txt"}'
                        ),
                    )
                ],
            )
        else:
            yield ContentToken(type="content", content="Es")
            yield ContentToken(type="content", content="a ")
            yield ContentToken(type="content", content="dire")
            yield ContentToken(type="content", content="ccion")
            yield ContentToken(type="content", content=" no")
            yield ContentToken(type="content", content=" exis")
            yield ContentToken(type="content", content="te")
            yield ContentToken(type="content", content=" rev")
            yield ContentToken(type="content", content="isa")
            yield ContentToken(type="content", content=" la")
            yield ContentToken(type="content", content=" direc")
            yield ContentToken(type="content", content="cion\n")
            yield ContentToken(type="content", content="# Posible errores\n")
            yield ContentToken(type="content", content="- La direccion este mal\n")
            yield ContentToken(type="content", content="- El archivo no exista\n")

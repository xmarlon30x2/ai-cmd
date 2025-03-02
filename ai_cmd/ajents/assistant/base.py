from typing import TYPE_CHECKING

# from ...ai.services.openai.base import OpenAI
from ...ai.services.mock import MockAI
from ...core.base import Core
from ...core.history.base import History
from ...core.history.types import SystemMessage
from .const import ASSISTANT_SYSTEM_MESSAGE
from .tools import create_assistant_tools

if TYPE_CHECKING:
    from ...controller.base import Controller
    from ...settings.base import Settings
    from ...window.base import Window


def create_assistant_core(
    controller: "Controller", settings: "Settings", window: "Window"
) -> "Core":
    ai = MockAI(
        api_key=settings.api_key,
        base_url=settings.base_url,
        model=settings.model,
        temperature=settings.temperature,
    )
    history = History(
        controller=controller,
        messages=[SystemMessage(content=ASSISTANT_SYSTEM_MESSAGE)],
    )
    tools = create_assistant_tools(controller, settings=settings, window=window)
    return Core(controller=controller, ai=ai, history=history, tools=tools)

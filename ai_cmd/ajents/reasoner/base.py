from typing import TYPE_CHECKING

from ...ai.services.openai.base import OpenAI
from ...core.base import Core
from ...core.history.base import History
from ...core.history.types import SystemMessage
from .const import REASONER_SYSTEM_MESSAGE

if TYPE_CHECKING:
    from ...controller.base import Controller
    from ...settings.base import Settings


def create_reasoner_core(controller: "Controller", settings: "Settings") -> "Core":
    ai = OpenAI(
        api_key=settings.api_key_reasoner,
        base_url=settings.base_url_reasoner,
        model=settings.model_reasoner,
        temperature=settings.temperature_reasoner,
    )
    history = History(
        controller=controller, messages=[SystemMessage(content=REASONER_SYSTEM_MESSAGE)]
    )
    return Core(controller=controller, ai=ai, history=history, tools=None)

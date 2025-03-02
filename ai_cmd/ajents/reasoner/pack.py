from typing import TYPE_CHECKING

from ...tools.tools_packs.ia import REASONER_CAPACITY, IAPack
from .base import create_reasoner_core

if TYPE_CHECKING:
    from ...controller.base import Controller
    from ...settings.base import Settings
    from ...window.base import Window


def create_ia_reasoner_pack(
    controller: "Controller", settings: "Settings", window: "Window"
):
    reasoner_core = create_reasoner_core(controller=controller, settings=settings)
    return IAPack(
        reasoner_core,
        controller=controller,
        window=window,
        name="reasoner",
        capacity=REASONER_CAPACITY,
    )

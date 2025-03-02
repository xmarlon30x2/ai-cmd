from typing import TYPE_CHECKING

from ...settings.base import Settings
from ...tools.tools_packs.app import AppPack
from ...tools.tools_packs.dirs.base import DirsPack
from ...tools.tools_packs.display import DisplayPack
from ...tools.tools_packs.files import FilesPack
from ...tools.tools_packs.http import HttpPack
from ...tools.tools_packs.os import OSPack
from ...tools.tools_packs.paths import PathsPack
from ...tools.tools_packs.python.base import PythonPack
from ...tools.tools_packs.time import TimePack
from ...tools.tools_packs.web import WebPack
from ..reasoner.pack import create_ia_reasoner_pack

if TYPE_CHECKING:
    from ...controller.base import Controller
    from ...window.base import Window

from ...tools.base import Tools


def create_assistant_tools(
    controller: "Controller", settings: "Settings", window: "Window"
) -> Tools:
    ai_reasoner_pack = create_ia_reasoner_pack(
        controller=controller, settings=settings, window=window
    )
    return Tools(
        controller=controller,
        tool_packs=[
            FilesPack(controller=controller, window=window),
            PathsPack(controller=controller, window=window),
            HttpPack(controller=controller, window=window),
            DirsPack(controller=controller, window=window),
            PythonPack(controller=controller, window=window),
            OSPack(controller=controller, window=window),
            AppPack(controller=controller, window=window),
            DisplayPack(controller=controller, window=window),
            TimePack(controller=controller, window=window),
            WebPack(controller=controller, window=window),
            ai_reasoner_pack,
        ],
    )

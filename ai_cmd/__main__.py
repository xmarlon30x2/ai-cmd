from asyncio import run

from .ai.services.mock import MockAI
# from .ai.services.openai.base import OpenAI
from .app.base import App
from .app.commands.base import Commands
from .app.commands.commands_packs.ai_config import IAConfigPack
from .app.commands.commands_packs.history import HistoryPack
from .app.commands.commands_packs.system import SystemPack
from .app.window import WindowApp
from .controller.base import Controller
from .core.base import Core
from .core.const import DEFAULT_SYSTEM_MESSAGE
from .core.history.base import History
from .core.history.types import SystemMessage
from .tools.base import Tools
from .tools.tools_packs.app import AppPack
from .tools.tools_packs.dirs.base import DirsPack
from .tools.tools_packs.display import DisplayPack
from .tools.tools_packs.files import FilesPack
from .tools.tools_packs.http import HttpPack
from .tools.tools_packs.os import OSPack
from .tools.tools_packs.paths import PathsPack
from .tools.tools_packs.python.base import PythonPack
from .tools.tools_packs.time import TimePack
from .tools.tools_packs.web import WebPack
from .utils import get_vars


async def main():
    api_key, model, base_url, temperature = get_vars() # type: ignore
    window = WindowApp()
    controller = Controller()
    app = App(
        window=window,
        controller=controller,
        core=Core(
            tools=Tools(
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
                ],
            ),
            history=History(
                controller=controller,
                messages=[SystemMessage(content=DEFAULT_SYSTEM_MESSAGE)],
            ),
            controller=controller,
            # ai=OpenAI(
            ai=MockAI(
                # api_key=api_key, base_url=base_url, model=model, temperature=temperature
            ),
        ),
        commands=Commands(
            controller=controller,
            command_packs=[
                SystemPack(controller=controller),
                IAConfigPack(controller=controller),
                HistoryPack(controller=controller),
            ],
        ),
    )
    await app.run()


if __name__ == "__main__":
    run(main())

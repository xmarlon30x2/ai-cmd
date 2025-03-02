from .ajents.assistant.base import create_assistant_core
from .app.base import App
from .app.commands.base import Commands
from .app.commands.commands_packs.config import IAConfigPack
from .app.commands.commands_packs.history import HistoryPack
from .app.commands.commands_packs.system import SystemPack
from .app.window import WindowApp
from .controller.base import Controller
from .settings.base import Settings


async def main():
    settings = Settings.get_instance()
    controller = Controller()
    window = WindowApp()
    assistant_core = create_assistant_core(
        controller=controller, settings=settings, window=window
    )
    app = App(
        controller=controller,
        core=assistant_core,
        settings=settings,
        window=window,
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

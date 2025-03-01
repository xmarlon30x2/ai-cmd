from asyncio import run
from os import getenv
from typing import TYPE_CHECKING, List

import dotenv
from rich.console import Console

from ai_cmd.clients.mockai import MockAI

from .actions import Actions
from .app import App
from .commands.ai_config import IAConfigPack
from .commands.base import BasePack
from .engine import Engine
from .tool_handler import ToolHandler
from .tool_packs.file_pack import FilePack
from .tool_packs.os_pack import OSPack
from .tool_packs.python_pack import PythonPack

if TYPE_CHECKING:
    from .pack import Pack
    from .tool_pack import ToolPack


async def main():
    dotenv.load_dotenv("app.env")
    # api_key = getenv("api_key") or ""
    model = getenv("model") or "deepseek"
    base_url = getenv("base_url") or "https://deepseek.com/"
    temperature = getenv("temperature")
    temperature = float(temperature) if temperature else 0.6
    console = Console()
    console.print(
        f"[green]Usando [bold]{model}[/bold] en {base_url} con {temperature} [/green]"
    )
    # ai = OpenAI(
    #     api_key=api_key, base_url=base_url, model=model, temperature=temperature
    # )
    ai = MockAI(model=model, temperature=temperature)
    tool_packs: List["ToolPack"] = [FilePack(console=console), PythonPack(), OSPack()]
    tool_handler = ToolHandler(tool_packs=tool_packs)
    engine = Engine(console=console, ai=ai, tool_handler=tool_handler)
    packs: List[Pack] = [BasePack(), IAConfigPack()]
    actions = Actions(console=console, packs=packs)
    app = App(console=console, actions=actions, engine=engine)
    actions.bind(app)
    await app.run()


if __name__ == "__main__":
    run(main())

from asyncio import run
from os import getenv

import dotenv
from rich.console import Console

from .actions import Actions
from .app import App
from .clients.openai import OpenAI
from .commands.ai_config import IAConfigPack
from .commands.base import BasePack
from .engine import Engine
from .tool_handler import ToolHandler
from .tool_packs.dirs_pack import DirsPack
from .tool_packs.files_pack import FilesPack

# from .tool_packs.http_pack import HttpPack
from .tool_packs.os_pack import OSPack
from .tool_packs.paths_pack import PathsPack
from .tool_packs.python_pack import PythonPack

# from .tool_packs.web_pack import WebPack


async def main():
    dotenv.load_dotenv("app.env")
    api_key = getenv("apy_key") or ""
    model = getenv("model") or "deepseek"
    base_url = getenv("base_url") or "https://deepseek.com/"
    temperature = getenv("temperature")
    temperature = float(temperature) if temperature else 0.6
    console = Console()
    console.print(
        f"[green]Usando el modelo [bold]🤖 {model}[/bold] de {base_url} con temperatura de {temperature}🌡️[/green]\n\n"
    )
    ai = OpenAI(
        api_key=api_key, base_url=base_url, model=model, temperature=temperature
    )
    tool_handler = ToolHandler(
        tool_packs=[
            FilesPack(),
            PathsPack(),
            # HttpPack(),
            DirsPack(),
            PythonPack(),
            OSPack(),
            # WebPack(),
        ]
    )
    engine = Engine(console=console, ai=ai, tool_handler=tool_handler)
    actions = Actions(
        console=console,
        packs=[
            BasePack(),
            IAConfigPack(),
        ],
    )
    app = App(console=console, actions=actions, engine=engine)
    await actions.bind(app)
    await tool_handler.bind(app)
    await app.run()


if __name__ == "__main__":
    run(main())

from typing import Optional

from prompt_toolkit import print_formatted_text

from ....ajents.assistant.base import create_assistant_core
from ..command_pack import CommandPack

COLORS_BY_ROLE = {
    "user": "blue",
    "assistant": "green",
    "tool": "gray",
    "function": "orange",
    "system": "yellow",
}


class HistoryPack(CommandPack):
    async def do_info(self):
        """Muestar informacion sobre el historial de mensajes"""
        system_msgs = 0
        user_msgs = 0
        tool_msgs = 0
        assistant_msgs = 0
        for msg in self.app.core.history.messages:
            match msg.role:
                case "assistant":
                    assistant_msgs += 1
                case "system":
                    system_msgs += 1
                case "tool":
                    tool_msgs += 1
                case "user":
                    user_msgs += 1
        lenght = len(self.app.core.history.messages)
        print_formatted_text(f"{lenght} mensajes del usuario")
        print_formatted_text(f"{lenght} mensajes del asistente")
        print_formatted_text(f"{lenght} mensajes de las herramientas")
        print_formatted_text(f"<white>{lenght} mensajes en total<white>")

    async def do_schema(self, top: Optional[int] = 0):
        """Muesta el orden y el rol del historial de mensajes"""

        for i, message in enumerate(self.app.core.history.messages[top:]):
            style = COLORS_BY_ROLE[message.role]
            print_formatted_text(
                f"[{style}]index -> {i:0>3} role -> {message.role} lenght -> {len(message.content)}[/{style}]"
            )
            if message.role == "assistant" and message.tool_calls:
                for tool_call in message.tool_calls:
                    style = COLORS_BY_ROLE["function"]
                    print_formatted_text(
                        f"[{style}]tool_call {tool_call.function.name} lenght -> {len(tool_call.function.arguments)}[/{style}]"
                    )

    async def do_delete(self, index: Optional[int] = None):
        """Elimina mensajes del chat"""
        self.app.core.history.messages.pop(index if index else -1)
        print_formatted_text("[green]Mensaje borrado con exito[/green]")

    async def do_show(self, range: Optional[int] = None):
        """Muestra mensajes del chat"""
        messages = self.app.core.history.messages[(-(range) if range else -1) :]
        for message in messages:
            print_formatted_text(f"[green]{message.role} > {message.content}[/green]")

    async def do_reset(self):
        self.app.core = create_assistant_core(
            self.app.controller, self.app.settings, self.app.window
        )

from typing import Optional

from ..pack import Pack

COLORS_BY_ROLE = {
    "user": "blue",
    "assistant": "green",
    "tool": "gray",
    "function": "orange",
    "system": "yellow",
}


class HistoryPack(Pack):
    def do_history_info(self):
        """Muestar informacion sobre el historial de mensajes"""
        lenght = len(self.app.engine.messages)
        self.app.console.print(f"{lenght} mensajes")

    def do_history_schema(self, index: Optional[int] = 0):
        """Muesta el orden y el rol del historial de mensajes"""

        for i, message in enumerate(self.app.engine.messages[index:]):
            style = COLORS_BY_ROLE[message.role]
            self.app.console.print(
                f"[{style}]index -> {i:0>3} role -> {message.role} lenght -> {len(message.content)}[/{style}]"
            )
            if message.role == "assistant" and message.tool_calls:
                for tool_call in message.tool_calls:
                    style = COLORS_BY_ROLE["function"]
                    self.app.console.print(
                        f"[{style}]tool_call {tool_call.function.name} lenght -> {len(tool_call.function.arguments)}[/{style}]"
                    )

    def do_history_pop(self, index: Optional[int] = None):
        """Elimina mensajes del chat"""
        self.app.engine.messages.pop(index if index else -1)
        self.app.console.print("[green]Mensaje borrado con exito[/green]")

    def do_history_show(self, range: Optional[int] = None):
        """Elimina mensajes del chat"""
        messages = self.app.engine.messages[(-(range) if range else -1) :]
        for message in messages:
            self.app.console.print(f"[green]{message.role} > {message.content}[/green]")

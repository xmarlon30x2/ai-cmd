from typing import Optional

from ..command_pack import CommandPack

COLORS_BY_ROLE = {
    "user": "blue",
    "assistant": "green",
    "tool": "gray",
    "function": "orange",
    "system": "yellow",
}


class HistoryPack(CommandPack):
    async def do_history_info(self):
        """Muestar informacion sobre el historial de mensajes"""
        lenght = len(self.app.core.history.messages)
        await self.app.show_formatted_text_html(text=f"{lenght} mensajes")

    async def do_history_schema(self, index: Optional[int] = 0):
        """Muesta el orden y el rol del historial de mensajes"""

        for i, message in enumerate(self.app.core.history.messages[index:]):
            style = COLORS_BY_ROLE[message.role]
            await self.app.show_formatted_text_html(
                f"[{style}]index -> {i:0>3} role -> {message.role} lenght -> {len(message.content)}[/{style}]"
            )
            if message.role == "assistant" and message.tool_calls:
                for tool_call in message.tool_calls:
                    style = COLORS_BY_ROLE["function"]
                    await self.app.show_formatted_text_html(
                        f"[{style}]tool_call {tool_call.function.name} lenght -> {len(tool_call.function.arguments)}[/{style}]"
                    )

    async def do_history_pop(self, index: Optional[int] = None):
        """Elimina mensajes del chat"""
        self.app.core.history.messages.pop(index if index else -1)
        await self.app.show_formatted_text_html(
            "[green]Mensaje borrado con exito[/green]"
        )

    async def do_history_show(self, range: Optional[int] = None):
        """Elimina mensajes del chat"""
        messages = self.app.core.history.messages[(-(range) if range else -1) :]
        for message in messages:
            await self.app.show_formatted_text_html(
                f"[green]{message.role} > {message.content}[/green]"
            )

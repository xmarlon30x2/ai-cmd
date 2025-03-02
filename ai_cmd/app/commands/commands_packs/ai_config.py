from typing import Optional

from ....ai.services.openai.base import OpenAI
from ..command_pack import CommandPack


class IAConfigPack(CommandPack):
    async def do_model(
        self, model: Optional[str] = None, temperature: Optional[float] = None
    ):
        """Muestra ayuda sobre los comandos"""
        if model:
            self.app.core.ai.model = model
        if temperature:
            self.app.core.ai.temperature = temperature
        if not temperature and not model:
            if isinstance(self.app.core.ai, OpenAI):
                await self.app.show_formatted_text_html(
                    f'temperature=<bold>"{self.app.core.ai.temperature}"</bold>'
                )
                await self.app.show_formatted_text_html(
                    f'model=<bold>"{self.app.core.ai.model}"</bold>'
                )

    async def do_client(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ):
        """Muestra ayuda sobre los comandos"""
        if api_key:
            if isinstance(self.app.core.ai, OpenAI):
                self.app.core.ai.openai.api_key = api_key
        if base_url:
            if isinstance(self.app.core.ai, OpenAI):
                self.app.core.ai.openai.base_url = base_url
        if not base_url and not api_key:
            if isinstance(self.app.core.ai, OpenAI):
                await self.app.show_formatted_text_html(
                    f'base_url=[bold]"{self.app.core.ai.openai.base_url}"[/bold]'
                )

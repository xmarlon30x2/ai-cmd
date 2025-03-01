from typing import Optional

from ..clients.openai import OpenAI
from ..pack import Pack


class IAConfigPack(Pack):
    def do_model(self, model: Optional[str], temperature: Optional[float]):
        """Muestra ayuda sobre los comandos"""
        if model:
            self.app.engine.ai.model = model
        if temperature:
            self.app.engine.ai.temperature = temperature
        if not temperature and not model:
            if isinstance(self.app.engine.ai, OpenAI):
                self.app.console.print(
                    f'temperature=[bold]"{self.app.engine.ai.temperature}"[/bold]'
                )
                self.app.console.print(
                    f'model=[bold]"{self.app.engine.ai.model}"[/bold]'
                )

    def do_client(self, api_key: Optional[str], base_url: Optional[str]):
        """Muestra ayuda sobre los comandos"""
        if api_key:
            if isinstance(self.app.engine.ai, OpenAI):
                self.app.engine.ai.openai.api_key = api_key
        if base_url:
            if isinstance(self.app.engine.ai, OpenAI):
                self.app.engine.ai.openai.base_url = base_url
        if not base_url and not api_key:
            if isinstance(self.app.engine.ai, OpenAI):
                self.app.console.print(
                    f'base_url=[bold]"{self.app.engine.ai.openai.base_url}"[/bold]'
                )

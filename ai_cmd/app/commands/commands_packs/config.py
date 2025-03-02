from typing import Optional

from prompt_toolkit import HTML, print_formatted_text

from ..command_pack import CommandPack


class IAConfigPack(CommandPack):
    async def do_configure(
        self,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: Optional[float] = None,
        model_reasoner: Optional[str] = None,
        base_url_reasoner: Optional[str] = None,
        temperature_reasoner: Optional[float] = None,
    ):
        """Configura los modelos y provedores de IA"""
        if model:
            self.app.settings.model = model
        if base_url:
            self.app.settings.base_url = base_url
        if temperature:
            self.app.settings.temperature = temperature
        if model_reasoner:
            self.app.settings.model_reasoner = model_reasoner
        if base_url_reasoner:
            self.app.settings.base_url_reasoner = base_url_reasoner
        if temperature_reasoner:
            self.app.settings.temperature_reasoner = temperature_reasoner
        if (
            model
            or base_url
            or model_reasoner
            or model_reasoner
            or base_url_reasoner
            or temperature_reasoner
        ):
            self.app.settings.save()
            print_formatted_text(
                HTML("<green>Configuracion guardado con exito</green>")
            )
        else:
            print_formatted_text(HTML("<gray>Configuracion del modelo base</gray>"))
            print_formatted_text(HTML(f" - model: <b>{self.app.settings.model}</b>"))
            print_formatted_text(
                HTML(f" - base_url: <b>{self.app.settings.base_url}</b>")
            )
            print_formatted_text(
                HTML(f" - temperature: <b>{self.app.settings.temperature}</b>")
            )
            print_formatted_text(
                HTML("<gray>Configuracion del modelo rasonador</gray>")
            )
            print_formatted_text(
                HTML(f" - model: <b>{self.app.settings.model_reasoner}</b>")
            )
            print_formatted_text(
                HTML(f" - base_url: <b>{self.app.settings.model_reasoner}</b>")
            )
            print_formatted_text(
                HTML(f" - temperature: <b>{self.app.settings.model_reasoner}</b>")
            )

    async def do_api_key(self):
        """Configura la api_key"""
        print_formatted_text(
            "Introduce la nueva api_key deja vacio para mantener la actual"
        )
        api_key = await self.app.window.prompt_secret("modelo base>")
        api_key = api_key.strip()
        if api_key:
            self.app.settings.api_key = api_key

        api_key_reasoner = await self.app.window.prompt_secret("modelo rasonador>")
        api_key_reasoner = api_key_reasoner.strip()
        if api_key_reasoner:
            self.app.settings.api_key_reasoner = api_key_reasoner

        if api_key or api_key_reasoner:
            self.app.settings.save()

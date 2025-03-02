from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import PromptSession, yes_no_dialog

from ..window.base import Window


class WindowApp(Window):
    async def prompt(self, message: str) -> str:
        prompt_session: PromptSession[str] = PromptSession()
        return await prompt_session.prompt_async(message)

    async def prompt_secret(self, message: str) -> str:
        prompt_session: PromptSession[str] = PromptSession()
        return await prompt_session.prompt_async(message, is_password=True)

    async def confirm(self, message: str) -> bool:
        dialog = yes_no_dialog(title=message)
        return await dialog.run_async()

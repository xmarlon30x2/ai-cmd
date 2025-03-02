### en desarrollo ###
from typing import TYPE_CHECKING, Any, Dict, Optional

from ...controller.base import Controller
from ..tool_pack import ToolPack

from ...core.history.types import AssistantMessage, UserMessage

if TYPE_CHECKING:
    from ...window.base import Window
    from ...core.base import Core

class IAPack(ToolPack):
    def __init__(
        self,
        controller: "Controller",
        window: 'Window',
        name:str,
        core: 'Core',
    ):
        super().__init__(controller=controller, window=window)
        self.core = core
        self.name = name

    async def tool_reset(self, confirm: bool) -> Dict[str, Any]:
        """Reinicia el chat con la IA.

        Args:
            confirm: Confirmación para reiniciar el chat.

        Returns:
            Un diccionario con un mensaje de éxito si el chat se reinicia,
            o un mensaje de error si la confirmación es falsa.
        """
        if not confirm:
            return {
                "success": False,
                "message": "Se requiere confirmación para reiniciar el chat.",
            }

        self.core = Core(
            ai=self.core.ai,
            console=self.core.console,
            tool_handler=self.core.tool_handler,
        )
        return {"success": True, "message": "Chat reiniciado."}

    async def tool_talk(
        self, content: str, role: Optional[str] = None
    ) -> Dict[str, str]:
        """Envia un mensaje a la IA.

        Args:
            content: El contenido del mensaje a enviar.
            role: El rol con el que enviar el mensaje, puede ser: system|user. Por defecto, 'user'.

        Returns:
            El último mensaje generado por el asistente.
        """
        await self.core.generate(content)
        if isinstance(msg, AssistantMessage):

        for msg in reversed(self.core.messages):
                return {"role": "assistant", "content": msg.content}
        return {"role": "assistant", "content": "No se generó respuesta."}

    async def tool_retry(self, confirm: bool) -> Dict[str, Any]:
        """Reintenta la respuesta del modelo en caso de haber perdido la conexión.

        Args:
            confirm: Confirmación para reintentar el último mensaje.

        Returns:
            El último mensaje generado por el asistente, o un mensaje de error
            si no hay mensajes previos del usuario para reintentar o si la confirmación es falsa.
        """
        if not confirm:
            return {
                "success": False,
                "message": "Se requiere confirmación para reintentar el último mensaje.",
            }

        last_user_message = None
        for msg in reversed(self.core.history.messages):
            if isinstance(msg, UserMessage):
                last_user_message = msg.content
                break

        if last_user_message:
            await self.core.generate(last_user_message)
            for msg in reversed(self.core.history.messages):
                if isinstance(msg, AssistantMessage):
                    return {"role": "assistant", "content": msg.content}
            return {"role": "assistant", "content": "No se generó respuesta."}
        else:
            return {"message": "No hay mensajes previos del usuario para reintentar."}

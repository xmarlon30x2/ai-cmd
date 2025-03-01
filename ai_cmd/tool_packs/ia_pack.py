### en desarrollo ###
from typing import Any, Dict, List, Optional

from ai_cmd.types import AssistantMessage, UserMessage

from ..engine import Engine
from ..tool_pack import ToolPack


class IAPack(ToolPack):
    name = "ia"

    def __init__(
        self,
        engine: Engine,
        system_message: str,
        start_messages: Optional[List[Dict[str, str]]] = None,
    ):
        super().__init__()
        self.engine = engine
        self.system_message = system_message
        self.start_messages = start_messages or []

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

        self.engine = Engine(
            ai=self.engine.ai,
            console=self.engine.console,
            tool_handler=self.engine.tool_handler,
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
        await self.engine.generate(content)
        for msg in reversed(self.engine.messages):
            if isinstance(msg, AssistantMessage):
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
        for msg in reversed(self.engine.messages):
            if isinstance(msg, UserMessage):
                last_user_message = msg.content
                break

        if last_user_message:
            await self.engine.generate(last_user_message)
            for msg in reversed(self.engine.messages):
                if isinstance(msg, AssistantMessage):
                    return {"role": "assistant", "content": msg.content}
            return {"role": "assistant", "content": "No se generó respuesta."}
        else:
            return {"message": "No hay mensajes previos del usuario para reintentar."}

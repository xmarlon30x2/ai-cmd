### en desarrollo ###
from typing import TYPE_CHECKING, Any, Dict, Optional, Protocol

from ...controller.base import Controller
from ...core.history.types import AssistantMessage, SystemMessage
from ..tool_pack import ToolPack

if TYPE_CHECKING:
    from ...core.base import Core
    from ...window.base import Window


REASONER_CAPACITY = "capaz de rasonar antes de responder, util para planificacion, consultar sobre fallos y generar respuestas de alta calidad y en general para cualquier accion que requiera un minimo de pensamiento"


class WithDocstring(Protocol):
    __doc__: None | str


class IAPack(ToolPack):
    """Paquete de herramientas para integración con IA"""

    def __init__(
        self,
        core: "Core",
        controller: "Controller",
        window: "Window",
        name: str,
        capacity: str,
    ):
        self.name = f"ai_{name}"
        self.custom_descs = {
            f"ai_{name}_talk": f"""
                Manda un mensaje al modelo de IA {name}. Descripcion de la IA: {capacity}

                Args:
                    content: Contenido del mensaje a enviar
                    await_response: Esperar respuesta generada (default: True)

                Returns:
                    Resultado estructurado con respuesta o acciones
            """,
            f"ai_{name}_configure": f"""
                Configura el comportamiento del modelo de IA {name}

                Args:
                    system_prompt: Nuevo prompt del sistema

                Returns:
                    Estado de la configuración
            """,
            f"ai_{name}_state": f"""
                Obtiene el estado actual del historial de la IA {name} junto con su ultimo mensaje

                Returns:
                    Metadata del estado interno
            """,
        }
        self.core = core
        super().__init__(window=window, controller=controller)

    def configure_docstring_by(self, func: WithDocstring, name: str, capacity: str):
        docstring = func.__doc__ or ""
        docstring = docstring.replace("{name}", name).replace("{capacity}", capacity)
        func.__doc__ = docstring

    async def tool_talk(
        self, content: str, await_response: Optional[bool] = None
    ) -> Dict[str, Any]:

        try:
            await self.core.start_generation(content=content)
        except Exception as exc:
            return {"error": str(exc)}

        if not await_response:
            return {"status": "instruction_queued"}

        # Buscar última respuesta relevante
        for msg in reversed(self.core.history.messages):
            if isinstance(msg, AssistantMessage):
                return {
                    "ai_response": msg.content,
                    "actions": (
                        [
                            {
                                "type": call.type,
                                "function": call.function.name,
                                "arguments": call.function.arguments,
                            }
                            for call in msg.tool_calls
                        ]
                        if msg.tool_calls
                        else None
                    ),
                }
        return {"error": "No response generated"}

    async def tool_configure(self, system_prompt: str) -> Dict[str, str]:

        # Actualizar mensaje de sistema
        system_msg = next(
            (
                msg
                for msg in self.core.history.messages
                if isinstance(msg, SystemMessage)
            ),
            None,
        )

        if system_msg:
            system_msg.content = system_prompt
        else:
            self.core.history.messages.insert(0, SystemMessage(content=system_prompt))

        return {"status": "configured"}

    async def tool_state(self) -> Dict[str, Any]:
        """
        Obtiene el estado actual del historial de la IA {name} junto con su ultimo mensaje

        Returns:
            Metadata del estado interno
        """
        return {
            "message_count": len(self.core.history.messages),
            "last_response": (
                self.core.history.messages[-1].content
                if self.core.history.messages
                else None
            ),
        }

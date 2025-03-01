from typing import Optional
from ajent.model import Model

from ..tool_pack import ToolPack


class IAPack(ToolPack):
    def __init__(self, name:str, model:Model, system_message:str, start_messages = None):
        self.name = name
        self.model = model
        self.start_messages = start_messages
        self.system_message = system_message
        self.messages = [{'role':'system', 'content': self.system_message}, *(self.start_messages or [])]

    def _get_tools_funcs(self):
        return {key[3:]:getattr(self, key) for key in dir(self) if key.startswith('do_')}

    async def do_reset(self):
        """Reinicia el chat con la IA."""
        self.messages = [{'role':'system', 'content': self.system_message}, *(self.start_messages or [])]
        await self.model.reset()
        return {'success': True}
    
    async def do_talk(self, content:str, role:Optional[str]=None):
        """
        Manda un mensaje a la IA
        args:
            role: El rol con el que enviaras el mensaje, puede ser: system|user
            content: El contenido del mensaje a enviar
        """
        self.messages.append({ 'content':content, role:role or 'user'})
        return await self._generate()

    async def do_retry(self):
        """Reintenta la respuesta del modelo en caso de haber perdido la conexion"""
        return await self._generate()

    async def _generate(self):
        message = await self.model.generate(self.messages)
        self.messages.append(message)
        return message
 
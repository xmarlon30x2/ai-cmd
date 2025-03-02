### en desarrollo ###
from typing import Any, Dict

from ..tool_pack import ToolPack


class DisplayPack(ToolPack):
    name = "display"

    async def tool_capture_screen(
        self, filename: str = "screenshot.png"
    ) -> Dict[str, Any]:
        """Captura una captura de pantalla y la guarda en un archivo.

        Args:
            filename (str): El nombre del archivo para guardar la captura de pantalla.
                           Por defecto es "screenshot.png".

        Returns:
            dict: Un diccionario con información sobre el resultado.
                  Si la captura de pantalla se guarda correctamente, devuelve
                  {"success": True, "filename": filename}.
                  Si ocurre un error, devuelve {"success": False, "error": mensaje de error}.
        """
        try:
            import pyscreenshot as ImageGrab  # type: ignore
        except ImportError:
            return {
                "success": False,
                "error": "pyscreenshot is required to use this tool. Please install it with 'pip install pyscreenshot'",
            }
        try:
            im = ImageGrab.grab()  # type: ignore
            im.save(filename)  # type: ignore
            return {"success": True, "filename": filename}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def tool_click(self, x: int, y: int) -> Dict[str, Any]:
        """Hace clic en la posición especificada.

        Args:
            x (int): La coordenada x del clic.
            y (int): La coordenada y del clic.

        Returns:
            dict: Un diccionario con información sobre el resultado.
                  Si el clic se realiza correctamente, devuelve {"success": True}.
                  Si ocurre un error, devuelve {"success": False, "error": mensaje de error}.
        """
        try:
            from pynput.mouse import Button, Controller
        except ImportError:
            return {
                "success": False,
                "error": "pynput is required to use this tool. Please install it with 'pip install pynput'",
            }
        try:
            mouse = Controller()
            mouse.position = (x, y)
            mouse.click(Button.left, 1)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def tool_move_mouse(self, x: int, y: int) -> Dict[str, Any]:
        """Mueve el ratón a la posición especificada.

        Args:
            x (int): La coordenada x de la posición.
            y (int): La coordenada y de la posición.

        Returns:
            dict: Un diccionario con información sobre el resultado.
                  Si el movimiento se realiza correctamente, devuelve {"success": True}.
                  Si ocurre un error, devuelve {"success": False, "error": mensaje de error}.
        """
        try:
            from pynput.mouse import Controller
        except ImportError:
            return {
                "success": False,
                "error": "pynput is required to use this tool. Please install it with 'pip install pynput'",
            }
        try:
            mouse = Controller()
            mouse.position = (x, y)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def tool_keyboard_write(self, text: str) -> Dict[str, Any]:
        """Escribe el texto especificado.

        Args:
            text (str): El texto a escribir.

        Returns:
            dict: Un diccionario con información sobre el resultado.
                  Si el texto se escribe correctamente, devuelve {"success": True}.
                  Si ocurre un error, devuelve {"success": False, error: mensaje de error}.
        """
        try:
            from pynput.keyboard import Controller
        except ImportError:
            return {
                "success": False,
                "error": "pynput is required to use this tool. Please install it with 'pip install pynput'",
            }
        try:
            keyboard = Controller()
            keyboard.type(text)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

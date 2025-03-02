### en desarrollo ###

from typing import Any, Literal

from ..tool_pack import ToolPack


class GuiPack(ToolPack):
    name = "gui"

    async def tool_capture_screen(
        self, filename: str = "screenshot.png"
    ) -> dict[str, Any]:
        """Captura una captura de pantalla y la guarda en un archivo.

        Args:
            filename (str): El nombre del archivo para guardar la captura de pantalla.
                           Por defecto es "screenshot.png".

        Returns:
            dict: Un diccionario con informaci\u00f3n sobre el resultado.
                  Si la captura de pantalla se guarda correctamente, devuelve
                  {success: True, filename: filename}.
                  Si ocurre un error, devuelve {success: False, error: mensaje de error}.
        """
        try:
            import mss  # type: ignore
            import mss.tools  # type: ignore
        except ImportError:
            return {
                "error": "El módulo mss no está instalado. Por favor, instálalo con 'pip install mss'"
            }

        try:
            with mss.mss() as sct:  # type: ignore
                sct_img = sct.grab(sct.monitors[1])  # type: ignore
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)  # type: ignore
            return {"success": True, "filename": filename}  # type: ignore
        except Exception as e:
            return {"error": str(e)}

    async def tool_click(
        self, x: int, y: int, button: Literal["left"] | Literal["right"] = "left"
    ) -> dict[str, Any]:
        """Hace clic en la posici\u00f3n especificada.

        Args:
            x (int): La coordenada x del clic.
            y (int): La coordenada y del clic.
            button (str): El bot\u00f3n del rat\u00f3n a usar. Puede ser left, right o middle.
                         Por defecto es left.

        Returns:
            dict: Un diccionario con informaci\u00f3n sobre el resultado.
                  Si el clic se realiza correctamente, devuelve {success: True}.
                  Si ocurre un error, devuelve {success: False, error: mensaje de error}.
        """
        try:
            import pyautogui  # type: ignore
        except ImportError:
            return {
                "error": "El módulo pyautogui no está instalado. Por favor, instálalo con 'pip install pyautogui'"
            }
        try:
            pyautogui.click(x, y, button=button)
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

    async def tool_move_mouse(
        self, x: int, y: int, duration: float = 0.1
    ) -> dict[str, Any]:
        """Mueve el rat\u00f3n a la posici\u00f3n especificada.

        Args:
            x (int): La coordenada x de la posici\u00f3n.
            y (int): La coordenada y de la posici\u00f3n.
            duration (float): La duraci\u00f3n del movimiento en segundos. Por defecto es 0.1.

        Returns:
            dict: Un diccionario con informaci\u00f3n sobre el resultado.
                  Si el movimiento se realiza correctamente, devuelve {success: True}.
                  Si ocurre un error, devuelve {success: False, error: mensaje de error}.
        """
        try:
            import pyautogui  # type: ignore
        except ImportError:
            return {
                "error": "El módulo pyautogui no está instalado. Por favor, instálalo con 'pip install pyautogui'"
            }
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

    async def tool_write(self, text: str):
        """Escribe el texto especificado.

        Args:
            text (str): El texto a escribir.

        Returns:
            dict: Un diccionario con informaci\u00f3n sobre el resultado.
                  Si el texto se escribe correctamente, devuelve {success: True}.
                  Si ocurre un error, devuelve {success: False, error: mensaje de error}.
        """
        try:
            import pyautogui  # type: ignore
        except ImportError:
            return {
                "error": "El módulo pyautogui no está instalado. Por favor, instálalo con 'pip install pyautogui'"
            }
        try:
            pyautogui.write(text)
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

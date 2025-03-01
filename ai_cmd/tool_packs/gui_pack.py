import pyautogui
import mss
import mss.tools
from ..tool_pack import ToolPack

class GuiPack(ToolPack):
    name = "gui"

    def __init__(self):
        super().__init__()

    async def tool_capture_screen(self, filename="screenshot.png"):
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
            with mss.mss() as sct:
                sct_img = sct.grab(sct.monitors[1])
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)
            return {success: True, filename: filename}
        except Exception as e:
            return {success: False, error: str(e)}

    async def tool_click(self, x, y, button=left):
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
            pyautogui.click(x, y, button=button)
            return {success: True}
        except Exception as e:
            return {success: False, error: str(e)}

    async def tool_move_mouse(self, x, y, duration=0.1):
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
            pyautogui.moveTo(x, y, duration=duration)
            return {success: True}
        except Exception as e:
            return {success: False, error: str(e)}

    async def tool_write(self, text):
        """Escribe el texto especificado.

        Args:
            text (str): El texto a escribir.

        Returns:
            dict: Un diccionario con informaci\u00f3n sobre el resultado.
                  Si el texto se escribe correctamente, devuelve {success: True}.
                  Si ocurre un error, devuelve {success: False, error: mensaje de error}.
        """
        try:
            pyautogui.write(text)
            return {success: True}
        except Exception as e:
            return {success: False, error: str(e)}

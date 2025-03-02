import os

from ..tool_pack import ToolPack


class PathsPack(ToolPack):
    name = "paths"

    async def tool_exists(self, path: str):
        """Comprueba si un directorio o archivo existe.

        Args:
            path (str): La ruta del directorio o archivo.

        Returns:
            dict: Un diccionario con un valor booleano en la clave 'are_identical' (True si son idénticos, False si no) o un mensaje de error en la clave 'error'.
        """
        try:
            return {"exists": os.path.exists(path)}
        except OSError as e:
            return {"error": str(e)}

    async def tool_creation_date(self, path: str):
        """Obtiene la fecha de creación de un archivo (timestamp).

        Args:
            path (str): La ruta del archivo.

        Returns:
            dict: Un diccionario con la fecha de creación del archivo en formato timestamp en la clave 'creation_time' o un mensaje de error en la clave 'error'.
        """
        try:
            creation_time = os.path.getctime(path)
            return {"creation_time": creation_time}
        except OSError as e:
            return {"error": str(e)}

    async def tool_modification_date(self, path: str):
        """Obtiene la fecha de la última modificación de un archivo (timestamp).

        Args:
            path (str): La ruta del archivo.

        Returns:
            dict: Un diccionario con la fecha de modificación del archivo en formato timestamp en la clave 'modification_time' o un mensaje de error en la clave 'error'.
        """
        try:
            modification_time = os.path.getmtime(path)
            return {"modification_time": modification_time}
        except OSError as e:
            return {"error": str(e)}

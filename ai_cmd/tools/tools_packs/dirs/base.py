import os
from typing import Any

from ...tool_pack import ToolPack
from .utils import scan_dir


class DirsPack(ToolPack):
    name = "dirs"

    async def tool_list(self, path: str) -> dict[str, Any]:
        """lista los archivos y directorios en la ruta especificada.

        Args:
            path (str): La ruta del directorio a listar.

        Returns:
            dict: Un diccionario con una lista de archivos en la clave 'files' o un mensaje de error en la clave 'error'.
        """
        try:
            elements = os.listdir(path)
            return {"path": path, "elements": elements}
        except OSError as e:
            return {"error": str(e)}

    async def tool_create(self, path: str) -> dict[str, Any]:
        """Crea un directorio en la ruta especificada.

        Args:
            path (str): La ruta del directorio a crear.

        Returns:
            dict: Un diccionario con un mensaje de éxito en la clave 'message' o un mensaje de error en la clave 'error'.
        """
        try:
            os.makedirs(path, exist_ok=True)
            return {"created": True, "path": path}
        except OSError as e:
            return {"error": str(e)}

    async def tool_delete(self, path: str) -> dict[str, str]:
        """Elimina el directorio en la ruta especificada. El directorio debe estar vacío.

        Args:
            path (str): La ruta del directorio a eliminar.

        Returns:
            dict: Un diccionario con un mensaje de éxito en la clave 'message' o un mensaje de error en la clave 'error'.
        """
        try:
            os.rmdir(path)
            return {"message": f"Directory {path} deleted successfully"}
        except OSError as e:
            return {"error": str(e)}

    async def tool_rename(self, path: str, new_name: str) -> dict[str, str]:
        """Le cambia el nombre a un directorio.

        Args:
            path (str): La ruta del directorio a eliminar.
            new_name (str): El nuevo nombre del directorio

        Returns:
            dict: Un diccionario con un mensaje de éxito en la clave 'message' o un mensaje de error en la clave 'error'.
        """
        try:
            os.renames(path, new_name)
            return {"message": f"Directory {path} deleted successfully"}
        except OSError as e:
            return {"error": str(e)}

    async def tool_scan(self, path: str) -> dict[str, Any]:
        try:
            return scan_dir(path)
        except Exception as exc:
            return {"error": str(exc)}

    async def tool_find(self, path: str, pattern: str) -> dict[str, Any]:
        """Busca archivos que coincidan con un patrón en la ruta especificada.

        Args:
            path (str): La ruta del directorio a buscar.
            pattern (str): El patrón a buscar (ej., '*.txt').

        Returns:
            dict: Un diccionario con una lista de archivos que coinciden con el patrón en la clave 'files' o un mensaje de error en la clave 'error'.
        """
        import glob

        try:
            files = glob.glob(os.path.join(path, pattern))
            return {"elements": files}
        except OSError as e:
            return {"error": str(e)}

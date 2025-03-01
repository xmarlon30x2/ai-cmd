import os
from typing import Any, Dict, List

from ..tool_pack import ToolPack


def scan_dir(path: str) -> Dict[str, Any]:
    elements: List[Dict[str, Any]] = []
    for element in os.scandir(path):
        if element.is_dir():
            try:
                elements.append(scan_dir(element.path))
            except Exception as exc:
                elements.append(
                    {"path": element.path, "type": "dir", "error": str(exc)}
                )
        else:
            elements.append(
                {
                    path: "str",
                    "type": (
                        "file"
                        if element.is_file()
                        else ("symlink" if element.is_symlink() else "none")
                    ),
                }
            )
    return {"path": path, "type": "dir", "elements": elements}


class DirsPack(ToolPack):
    name = "dirs"

    async def tool_list(self, path: str) -> Dict[str, Any]:
        """Lista los archivos y directorios en la ruta especificada.

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

    async def tool_create(self, path: str):
        """Crea un directorio en la ruta especificada.

        Args:
            path (str): La ruta del directorio a crear.

        Returns:
            dict: Un diccionario con un mensaje de éxito en la clave 'message' o un mensaje de error en la clave 'error'.
        """
        try:
            os.makedirs(path, exist_ok=True)
            return {"message": f"Directory {path} created successfully"}
        except OSError as e:
            return {"error": str(e)}

    async def tool_delete(self, path: str):
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

    async def tool_rename(self, path: str, new_name: str):
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

    async def tool_scan(self, path: str):
        try:
            return scan_dir(path)
        except Exception as exc:
            return {"error": str(exc)}

    async def tool_find(self, path: str, pattern: str):
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

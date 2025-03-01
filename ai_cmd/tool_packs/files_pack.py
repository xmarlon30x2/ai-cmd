import os
import shutil

from ..tool_pack import ToolPack


class FilesPack(ToolPack):
    name = "files"

    async def tool_read(self, path: str):
        """
        Lee el contenido de un archivo en la ruta especificada.

        Args:
            path (str): La ruta del archivo a leer.

        Returns:
            dict: Un diccionario con el contenido del archivo en la clave 'content' o un mensaje de error en la clave 'error'.
        """
        self.app.console.print(f"[yellow]Leyendo [italic]{path}[/italic][/yellow]")
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            return {"content": content}
        except OSError as e:
            return {"error": str(e)}

    async def tool_write(self, path: str, content: str):
        """
        Escribe contenido en un archivo en la ruta especificada.

        Args:
            path (str): La ruta del archivo a escribir.
            content (str): El contenido a escribir en el archivo.

        Returns:
            dict: Un diccionario con un mensaje de éxito en la clave 'message' o un mensaje de error en la clave 'error'.
        """
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"message": f"File {path} written successfully"}
        except OSError as e:
            return {"error": str(e)}

    async def tool_delete(self, path: str):
        """
        Elimina el archivo en la ruta especificada.

        Args:
            path (str): La ruta del archivo a eliminar.

        Returns:
            dict: Un diccionario con un mensaje de éxito en la clave 'message' o un mensaje de error en la clave 'error'.
        """
        try:
            os.remove(path)
            return {"message": f"File {path} deleted successfully"}
        except OSError as e:
            return {"error": str(e)}

    async def tool_count_lines(self, path: str):
        """
        Cuenta el número de líneas en un archivo de texto.

        Args:
            path (str): La ruta del archivo de texto.

        Returns:
            dict: Un diccionario con el número de líneas en la clave 'line_count' o un mensaje de error en la clave 'error'.
        """
        try:
            with open(path, "r", encoding='utf-8') as f:
                line_count = sum(1 for _ in f)
            return {"line_count": line_count}
        except OSError as e:
            return {"error": str(e)}

    async def tool_size(self, path: str):
        """
        Obtiene el tamaño de un archivo en bytes.

        Args:
            path (str): La ruta del archivo.

        Returns:
            dict: Un diccionario con el tamaño del archivo en bytes en la clave 'size' o un mensaje de error en la clave 'error'.
        """
        try:
            size = os.path.getsize(path)
            return {"size": size}
        except OSError as e:
            return {"error": str(e)}

    async def tool_copy(self, source_path: str, destination_path: str):
        """
        Copia un archivo desde la ruta de origen a la ruta de destino.

        Args:
            source_path (str): La ruta del archivo de origen.
            destination_path (str): La ruta del archivo de destino.

        Returns:
            dict: Un diccionario con un mensaje de éxito en la clave 'message' o un mensaje de error en la clave 'error'.
        """
        try:
            shutil.copy(source_path, destination_path)

            return {
                "message": f"File {source_path} copied to {destination_path} successfully"
            }
        except OSError as e:
            return {"error": str(e)}

    async def tool_move(self, source_path: str, destination_path: str):
        """
        Mueve un archivo desde la ruta de origen a la ruta de destino.

        Args:
            source_path (str): La ruta del archivo de origen.
            destination_path (str): La ruta del archivo de destino.

        Returns:
            dict: Un diccionario con un mensaje de éxito en la clave 'message' o un mensaje de error en la clave 'error'.
        """
        try:
            shutil.move(source_path, destination_path)
            return {
                "message": f"File {source_path} moved to {destination_path} successfully"
            }
        except OSError as e:
            return {"error": str(e)}

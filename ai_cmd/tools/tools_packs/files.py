import difflib
import gzip
import hashlib
import os
import re
import shutil
import tarfile
import zipfile
from typing import Any, Dict, List, Optional, Union

from ..tool_pack import ToolPack

DEFAULT_ENCODING = "utf-8"


class FilesPack(ToolPack):
    name = "files"

    async def tool_read(self, path: str, encoding: Optional[str] = None):
        """
        Lee el contenido de un archivo en la ruta especificada.

        Args:
            path: La ruta del archivo a leer.
            encoding: La codificación del archivo (por defecto: utf-8).

        Returns:
            Un diccionario con el contenido del archivo en la clave 'content'
            o un mensaje de error en la clave 'error'.
        """
        try:
            with open(
                path, "r", encoding=encoding if encoding else DEFAULT_ENCODING
            ) as f:
                content = f.read()
            return {"content": content}
        except OSError as e:
            return {"error": str(e)}

    async def tool_write(
        self, path: str, content: str, encoding: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Escribe contenido en un archivo en la ruta especificada.

        Args:
            path: La ruta del archivo a escribir.
            content: El contenido a escribir en el archivo.
            encoding: La codificación del archivo (por defecto: "utf-8").

        Returns:
            Un diccionario con un mensaje de éxito en la clave 'message'
            o un mensaje de error en la clave 'error'.
        """
        try:
            with open(
                path, "w", encoding=encoding if encoding else DEFAULT_ENCODING
            ) as f:
                f.write(content)
            return {"message": f"File {path} written successfully"}
        except OSError as e:
            return {"error": str(e)}

    async def tool_delete(self, path: str) -> Dict[str, str]:
        """
        Elimina el archivo en la ruta especificada.

        Args:
            path: La ruta del archivo a eliminar.

        Returns:
            Un diccionario con un mensaje de éxito en la clave 'message'
            o un mensaje de error en la clave 'error'.
        """
        try:
            os.remove(path)
            return {"message": f"File {path} deleted successfully"}
        except OSError as e:
            return {"error": str(e)}

    async def tool_count_lines(self, path: str) -> Dict[str, Union[int, str]]:
        """
        Cuenta el número de líneas en un archivo de texto.

        Args:
            path: La ruta del archivo de texto.

        Returns:
            Un diccionario con el número de líneas en la clave 'line_count'
            o un mensaje de error en la clave 'error'.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                line_count = sum(1 for _ in f)
            return {"line_count": line_count}
        except OSError as e:
            return {"error": str(e)}

    async def tool_size(
        self, path: str, unit: Optional[str] = None
    ) -> Dict[str, Union[int, float, str]]:
        """
        Obtiene el tamaño de un archivo.

        Args:
            path: La ruta del archivo.
            unit: La unidad en la que se debe mostrar el tamaño ("bytes", "KB", "MB", "GB").
                  Por defecto, "bytes".

        Returns:
            Un diccionario con el tamaño del archivo en la clave 'size'
            o un mensaje de error en la clave 'error'.
        """
        try:
            size_bytes = os.path.getsize(path)
            if unit == "KB":
                size = size_bytes / 1024
            elif unit == "MB":
                size = size_bytes / (1024 * 1024)
            elif unit == "GB":
                size = size_bytes / (1024 * 1024 * 1024)
            else:
                size = size_bytes
                unit = "bytes"
            return {"size": size, "unit": unit}
        except OSError as e:
            return {"error": str(e)}

    async def tool_copy(
        self, source_path: str, destination_path: str
    ) -> Dict[str, str]:
        """
        Copia un archivo desde la ruta de origen a la ruta de destino.

        Args:
            source_path: La ruta del archivo de origen.
            destination_path: La ruta del archivo de destino.

        Returns:
            Un diccionario con un mensaje de éxito en la clave 'message'
            o un mensaje de error en la clave 'error'.
        """
        try:
            shutil.copy(source_path, destination_path)
            return {
                "message": f"File {source_path} copied to {destination_path} successfully"
            }
        except OSError as e:
            return {"error": str(e)}

    async def tool_move(
        self, source_path: str, destination_path: str
    ) -> Dict[str, str]:
        """
        Mueve un archivo desde la ruta de origen a la ruta de destino.

        Args:
            source_path: La ruta del archivo de origen.
            destination_path: La ruta del archivo de destino.

        Returns:
            Un diccionario con un mensaje de éxito en la clave 'message'
            o un mensaje de error en la clave 'error'.
        """
        try:
            shutil.move(source_path, destination_path)
            return {
                "message": f"File {source_path} moved to {destination_path} successfully"
            }
        except OSError as e:
            return {"error": str(e)}

    async def tool_create(self, path: str) -> Dict[str, str]:
        """
        Crea un nuevo archivo vacío.

        Args:
            path: La ruta del archivo a crear.

        Returns:
            Un diccionario con un mensaje de éxito en la clave 'message'
            o un mensaje de error en la clave 'error'.
        """
        if os.path.exists(path):
            return {"message": "File already created"}
        try:
            open(path, "w").close()  # Crea un archivo vacío
            return {"message": f"File {path} created successfully"}
        except OSError as e:
            return {"error": str(e)}

    async def tool_append(
        self, path: str, content: str, encoding: Optional[str] = "utf-8"
    ) -> Dict[str, str]:
        """
        Añade contenido al final de un archivo existente.

        Args:
            path: La ruta del archivo al que se va a añadir contenido.
            content: El contenido a añadir.
            encoding: La codificación del archivo (por defecto: "utf-8").

        Returns:
            Un diccionario con un mensaje de éxito en la clave 'message'
            o un mensaje de error en la clave 'error'.
        """
        try:
            with open(
                path, "a", encoding=encoding
            ) as f:  # Abre el archivo en modo "append"
                f.write(content)
            return {"message": f"Content appended to file {path} successfully"}
        except OSError as e:
            return {"error": str(e)}

    async def tool_replace(
        self,
        path: str,
        old_string: str,
        new_string: str,
        encoding: Optional[str] = "utf-8",
    ) -> Dict[str, str]:
        """
        Reemplaza todas las ocurrencias de una cadena dentro de un archivo.

        Args:
            path: La ruta del archivo en el que se va a realizar el reemplazo.
            old_string: La cadena a reemplazar.
            new_string: La cadena de reemplazo.
            encoding: La codificación del archivo (por defecto: "utf-8").

        Returns:
            Un diccionario con un mensaje de éxito en la clave 'message'
            o un mensaje de error en la clave 'error'.
        """
        try:
            with open(path, "r", encoding=encoding) as f:
                content = f.read()
            updated_content = content.replace(old_string, new_string)
            with open(path, "w", encoding=encoding) as f:
                f.write(updated_content)
            return {
                "message": f"String '{old_string}' replaced with '{new_string}' in file {path} successfully"
            }
        except OSError as e:
            return {"error": str(e)}

    async def tool_replace_regex(
        self,
        path: str,
        pattern: str,
        replacement: str,
        encoding: Optional[str] = "utf-8",
    ) -> Dict[str, str]:
        """
        Reemplaza todas las coincidencias de una expresión regular dentro de un archivo.

        Args:
            path: La ruta del archivo en el que se va a realizar el reemplazo.
            pattern: La expresión regular a buscar.
            replacement: La cadena de reemplazo.
            encoding: La codificación del archivo (por defecto: "utf-8").

        Returns:
            Un diccionario con un mensaje de éxito en la clave 'message'
            o un mensaje de error en la clave 'error'.
        """
        try:
            with open(path, "r", encoding=encoding) as f:
                content = f.read()
            updated_content = re.sub(pattern, replacement, content)
            with open(path, "w", encoding=encoding) as f:
                f.write(updated_content)
            return {
                "message": f"Regex '{pattern}' replaced with '{replacement}' in file {path} successfully"
            }
        except OSError as e:
            return {"error": str(e)}

    async def tool_insert_line(
        self,
        path: str,
        line_number: int,
        content: str,
        encoding: Optional[str] = "utf-8",
    ) -> Dict[str, str]:
        """
        Inserta una línea de texto en una posición específica dentro de un archivo.

        Args:
            path: La ruta del archivo en el que se va a realizar la inserción.
            line_number: El número de línea en el que se va a insertar el contenido (la primera línea es 1).
            content: El contenido a insertar.
            encoding: La codificación del archivo (por defecto: "utf-8").

        Returns:
            Un diccionario con un mensaje de éxito en la clave 'message'
            o un mensaje de error en la clave 'error'.
        """
        try:
            with open(path, "r", encoding=encoding) as f:
                lines = f.readlines()
            if 1 <= line_number <= len(lines) + 1:
                lines.insert(
                    line_number - 1, content + "\n"
                )  # Insertar en la posición correcta
                with open(path, "w", encoding=encoding) as f:
                    f.writelines(lines)
                return {
                    "message": f"Line inserted at line {line_number} in file {path} successfully"
                }
            else:
                return {
                    "error": f"Line number {line_number} is out of range (1-{len(lines) + 1})"
                }
        except OSError as e:
            return {"error": str(e)}

    async def tool_get_line(
        self, path: str, line_number: int, encoding: Optional[str] = "utf-8"
    ) -> Dict[str, str]:
        """
        Obtiene una línea específica de un archivo.

        Args:
            path: La ruta del archivo del que se va a obtener la línea.
            line_number: El número de línea a obtener (la primera línea es 1).
            encoding: La codificación del archivo (por defecto: "utf-8").

        Returns:
            Un diccionario con la línea en la clave 'line' o un mensaje de error en la clave 'error'.
        """
        try:
            with open(path, "r", encoding=encoding) as f:
                lines = f.readlines()
            if 1 <= line_number <= len(lines):
                return {
                    "line": lines[line_number - 1].rstrip("\n")
                }  # Eliminar el salto de línea
            else:
                return {
                    "error": f"Line number {line_number} is out of range (1-{len(lines)})"
                }
        except OSError as e:
            return {"error": str(e)}

    async def tool_search(
        self, path: str, query: str, encoding: Optional[str] = "utf-8"
    ) -> Dict[str, Any]:
        """
        Busca una cadena dentro de un archivo y devuelve las líneas que coinciden junto con su número de línea.

        Args:
            path: La ruta del archivo en el que se va a realizar la búsqueda.
            query: La cadena a buscar.
            encoding: La codificación del archivo (por defecto: "utf-8").

        Returns:
            Un diccionario con una lista de diccionarios, donde cada diccionario contiene el número de línea ('line_number') y la línea coincidente ('line'),
            o un mensaje de error en la clave 'error'.
        """
        try:
            with open(path, "r", encoding=encoding) as f:
                lines = f.readlines()
            matching_lines: list[dict[str, Any]] = []
            for i, line in enumerate(lines):
                if query in line:
                    matching_lines.append(
                        {"line_number": i + 1, "line": line.rstrip("\n")}
                    )
            return {"lines": matching_lines}
        except OSError as e:
            return {"error": str(e)}

    async def tool_diff(
        self, path1: str, path2: str
    ) -> Dict[str, Union[List[str], str]]:
        """
        Compara dos archivos y devuelve las diferencias.

        Args:
            path1: La ruta del primer archivo.
            path2: La ruta del segundo archivo.

        Returns:
            Un diccionario con una lista de líneas que muestran las diferencias en la clave 'diff'
            o un mensaje de error en la clave 'error'.
        """
        try:
            with open(path1, "r", encoding="utf-8") as f1, open(
                path2, "r", encoding="utf-8"
            ) as f2:
                file1_lines = f1.readlines()
                file2_lines = f2.readlines()
            diff = difflib.unified_diff(
                file1_lines, file2_lines, fromfile=path1, tofile=path2
            )
            diff_lines = list(diff)
            return {"diff": diff_lines}
        except OSError as e:
            return {"error": str(e)}

    async def tool_compress(
        self, path: str, archive_format: str = "zip"
    ) -> Dict[str, str]:
        """
        Comprime un archivo o directorio.

        Args:
            path: La ruta del archivo o directorio a comprimir.
            archive_format: El formato del archivo comprimido ("zip", "tar", "gzip"). Por defecto, "zip".

        Returns:
            Un diccionario con un mensaje de éxito en la clave 'message'
            o un mensaje de error en la clave 'error'.
        """
        try:
            if archive_format == "zip":
                with zipfile.ZipFile(
                    path + ".zip", "w", zipfile.ZIP_DEFLATED
                ) as zip_file:
                    if os.path.isfile(path):
                        zip_file.write(path, os.path.basename(path))
                    else:
                        for root, _, files in os.walk(path):
                            for file in files:
                                zip_file.write(
                                    os.path.join(root, file),
                                    os.path.relpath(os.path.join(root, file), path),
                                )
                return {
                    "message": f"File/directory '{path}' compressed to '{path}.zip' successfully"
                }
            elif archive_format == "tar":
                with tarfile.open(path + ".tar", "w") as tar_file:
                    tar_file.add(path, arcname=os.path.basename(path))
                return {
                    "message": f"File/directory '{path}' compressed to '{path}.tar' successfully"
                }
            elif archive_format == "gzip":
                if os.path.isfile(path):
                    with open(path, "rb") as f_in:
                        with gzip.open(path + ".gz", "wb") as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    return {
                        "message": f"File '{path}' compressed to '{path}.gz' successfully"
                    }
                else:
                    return {
                        "error": "gzip format is only supported for files, not directories"
                    }
            else:
                return {"error": f"Unsupported archive format: {archive_format}"}
        except OSError as e:
            return {"error": str(e)}

    async def tool_decompress(
        self, path: str, destination_path: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Descomprime un archivo.

        Args:
            path: La ruta del archivo a descomprimir.
            destination_path: La ruta donde se descomprimirán los archivos.
                             Si no se especifica, se utilizará el directorio actual.

        Returns:
            Un diccionario con un mensaje de éxito en la clave 'message'
            o un mensaje de error en la clave 'error'.
        """
        try:
            if destination_path is None:
                destination_path = os.path.dirname(path)
            if path.endswith(".zip"):
                with zipfile.ZipFile(path, "r") as zip_file:
                    zip_file.extractall(destination_path)
                return {
                    "message": f"File '{path}' decompressed to '{destination_path}' successfully"
                }
            elif path.endswith(".tar"):
                with tarfile.open(path, "r") as tar_file:
                    tar_file.extractall(destination_path)
                return {
                    "message": f"File '{path}' decompressed to '{destination_path}' successfully"
                }
            elif path.endswith(".gz"):
                base_name = os.path.basename(path)
                output_file = os.path.join(
                    destination_path, base_name[:-3]
                )  # Remove .gz
                with gzip.open(path, "rb") as f_in:
                    with open(output_file, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                return {
                    "message": f"File '{path}' decompressed to '{destination_path}' successfully"
                }
            else:
                return {
                    "error": "Unsupported archive format. Only .zip, .tar, and .gz are supported."
                }
        except OSError as e:
            return {"error": str(e)}

    async def tool_get_metadata(self, path: str) -> Dict[str, Union[str, int, float]]:
        """
        Obtiene metadatos de un archivo.

        Args:
            path: La ruta del archivo.

        Returns:
            Un diccionario con los metadatos del archivo
            o un mensaje de error en la clave 'error'.
        """
        try:
            return {
                "name": os.path.basename(path),
                "size": os.path.getsize(path),
                "creation_time": os.path.getctime(path),
                "modification_time": os.path.getmtime(path),
                "access_time": os.path.getatime(path),
                "is_directory": os.path.isdir(path),
                "is_file": os.path.isfile(path),
                "is_link": os.path.islink(path),
            }
        except OSError as e:
            return {"error": str(e)}

    async def tool_hash(self, path: str, algorithm: str = "sha256") -> Dict[str, str]:
        """
        Calcula el hash de un archivo.

        Args:
            path: La ruta del archivo.
            algorithm: El algoritmo de hash a utilizar ("sha256", "md5", "sha1"). Por defecto, "sha256".

        Returns:
            Un diccionario con el hash del archivo en la clave 'hash'
            o un mensaje de error en la clave 'error'.
        """
        try:
            if algorithm not in hashlib.algorithms_available:
                return {"error": f"Unsupported hash algorithm: {algorithm}"}

            hasher = hashlib.new(algorithm)
            with open(path, "rb") as file:
                while chunk := file.read(4096):
                    hasher.update(chunk)
            return {"hash": hasher.hexdigest()}
        except OSError as e:
            return {"error": str(e)}

    async def tool_convert_encoding(
        self, path: str, from_encoding: str = "auto", to_encoding: str = "utf-8"  # type: ignore
    ) -> Dict[str, str]:
        """
        Convierte un archivo de una codificación a otra.

        Args:
            path: La ruta del archivo a convertir.
            from_encoding: La codificación original del archivo. Si se especifica "auto", se intentará detectar la codificación automáticamente. Por defecto, "auto".
            to_encoding: La codificación a la que se convertirá el archivo. Por defecto, "utf-8".

        Returns:
            Un diccionario con un mensaje de éxito en la clave 'message'
            o un mensaje de error en la clave 'error'.
        """
        try:
            import chardet  # type: ignore
        except ImportError:
            return {"error": "El módulo chardet no está instalado."}
        try:
            if from_encoding == "auto":
                with open(path, "rb") as f:
                    raw_data = f.read()
                result: dict[str, Any] = chardet.detect(raw_data)  # type: ignore
                from_encoding: str | None = result["encoding"]  # type: ignore
                if from_encoding is None:
                    return {"error": "Failed to detect the encoding of the file."}
                print(f"Detected encoding: {from_encoding}")

            with open(path, "r", encoding=from_encoding, errors="ignore") as f:  # type: ignore
                content = f.read()

            # Escribir el archivo con la nueva codificación
            with open(path, "w", encoding=to_encoding) as f:
                f.write(content)

            return {
                "message": f"File '{path}' converted from '{from_encoding}' to '{to_encoding}' successfully"
            }
        except OSError as e:
            return {"error": str(e)}
        except LookupError as e:
            return {"error": f"Invalid encoding specified: {e}"}

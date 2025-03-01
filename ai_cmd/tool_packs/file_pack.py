"""FilePack"""

from time import sleep
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from rich.console import Console

from ..tool_pack import ToolPack

START_DEFAULT = 0
END_DEFAULT = -1
DEFAULT_ENCODING = "utf-8"


class FilePack(ToolPack):
    """Herramientas para manejo de archivos"""

    name = "file"

    def __init__(self, console: "Console"):
        self.console = console
        super().__init__()

    async def tool_read(
        self,
        path: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
        encoding: Optional[str] = None,
    ):
        """
        Lee el contenido del archivo
        args:
            path: La direccion del archivo
            start: Indica el numero del caracter donde se va a empezar a leer. \
                Es opcional, por defecto es el inicio del archivo
            end: Indica el numero del caracter donde se va a terminar a leer. \
                Es opcional, por defecto es el final del archivo
            encoding: La codificaion del archivo. Por defecto es utf-8
        """
        self.console.print(
            f'[yellow]Argumentos -> path=[bold]"{path}"[/bold]\
            {f"start=[bold]'{start}'[/bold]" if start else ""}\
            {f"end=[bold]'{end}'[/bold]" if end else ""}\
            {f"encoding=[bold]'{encoding}'[/bold]" if encoding else ""}[/yellow]'
        )
        sleep(2)
        with open(path, "r", encoding=encoding or DEFAULT_ENCODING) as file:
            file.seek(start or START_DEFAULT)
            content = file.read(end or END_DEFAULT)
        return {"content": content}

    async def tool_write(self, path: str, content: str, encoding: Optional[str] = None):
        """
        Escribe text en un archivo, si esta creado remplazando el conenido de este o
         creando uno nuevo
        args:
            path: La direccion del archivo
            content: El contenido que se va a escribir
            encoding: La codificaion del archivo. Por defecto es utf-8
        """
        with open(path, "w", encoding=encoding or DEFAULT_ENCODING) as file:
            file.write(content)

    async def tool_append(
        self, path: str, content: str, encoding: Optional[str] = None
    ):
        """
        Escribe text al final de un archivo
        args:
            path: La direccion del archivo
            content: El contenido que se va a escribir
            encoding: La codificaion del archivo. Por defecto es utf-8
        """
        with open(path, "a", encoding=encoding or DEFAULT_ENCODING) as file:
            file.write(content)

    async def reset(self):
        pass

### en dessarrollo ###
from typing import Any

from ..tool_pack import ToolPack


class WebPack(ToolPack):
    name = "web"

    async def tool_search(self, query: str, num_results: int = 5):
        """Hace una busqueda en goolge

        Args:
            query (str): La query a buscar
            num_results: El numbero de resultados. Por defecto es 5
        """
        try:
            from googlesearch import search  # type: ignore
        except ImportError:
            return {
                "error": "El módulo googlesearch-python no está instalado. Por favor, instálalo con 'pip install googlesearch-python'"
            }
        results: list[dict[str, Any] | str] = []
        try:
            for result in search(query, num_results=num_results, advanced=True):
                if isinstance(result, str):
                    results.append(result)
                    continue
                results.append(
                    {
                        "url": result.url,
                        "title": result.title,  # type: ignore
                        "description": result.description,  # type: ignore
                    }
                )
            return {"results": results}
        except Exception as e:
            return {"error": str(e)}

    async def tool_links(self, url: str) -> dict[str, Any]:
        """
        Extrae todos los enlaces (href) de una página web.

        Args:
            url (str): La URL de la página web.

        Returns:
            dict: Un diccionario con una lista de enlaces en la clave 'links' o un mensaje de error en la clave 'error'.
        """
        try:
            import requests
        except ImportError:
            return {"error": "El módulo requests no está instalado."}
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            return {
                "error": "El módulo bs4 no está instalado. Por favor instalalo con 'pip install bs4'"
            }
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            links: list[Any] = [
                ancor.attrs.get("href", "") for ancor in soup.find_all("a", href=True)  # type: ignore
            ]
            return {"links": links}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    async def tool_read(self, url: str):
        """
        Lee el contenido de una página web y devuelve el texto.

        Args:
            url (str): La URL de la página web.

        Returns:
            dict: Un diccionario con el contenido de la página en la clave 'content' o un mensaje de error en la clave 'error'.
        """
        try:
            import requests
        except ImportError:
            return {"error": "El módulo requests no está instalado."}
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            return {"error": "El módulo beautifulsoup4 no está instalado."}
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
            return {"content": text}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

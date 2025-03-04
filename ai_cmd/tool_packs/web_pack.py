### en dessarrollo ###
from typing import Any

import requests

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
        results: list[dict[str, Any]] = []
        try:
            for resultado in search(query, num_results=num_results, advanced=True):  # type: ignore
                results.append(
                    {
                        "url": resultado.url,  # type: ignore
                        "title": resultado.title,  # type: ignore
                        "description": resultado.description,  # type: ignore
                    }
                )
            return {"results": results}
        except Exception as e:
            return {"error": str(e)}

    async def tool_links(self, url: str):
        """
        Extrae todos los enlaces (href) de una página web.

        Args:
            url (str): La URL de la página web.

        Returns:
            dict: Un diccionario con una lista de enlaces en la clave 'links' o un mensaje de error en la clave 'error'.
        """
        try:
            from bs4 import BeautifulSoup  # type: ignore
        except ImportError:
            return {'error': 'El módulo beautifulsoup4 no está instalado.'}
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            links = [a["href"] for a in soup.find_all("a", href=True)]
            return {"links": links}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

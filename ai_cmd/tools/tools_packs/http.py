### en dessarrollo ###
from typing import Any, Dict, Optional

import requests

from ..tool_pack import ToolPack


class HttpPack(ToolPack):
    name = "http"

    async def tool_request(
        self,
        url: str,
        method: str = "get",
        data: Optional[str] = None,
        timeout: float = 5,
    ) -> Dict[str, Any]:
        """
        Args:
            url (str): La URL a la que hacer la petición.
            method (str): El método HTTP a utilizar (get, post, put, delete). Por defecto, 'get'.
            data (str): Un json de datos a enviar con la petición (para métodos post y put). Por defecto, None.
            timeout (float): Tiempo de espera
        Returns:
            dict: Un diccionario con el código de estado HTTP en la clave 'status_code' y el contenido de la respuesta en la clave 'content'.
                  Si ocurre un error, devuelve un diccionario con un mensaje de error en la clave 'error'.
        """
        try:
            method = method.lower()
            headers = {"User-Agent": "Mozilla/5.0"}

            if method == "get":
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == "post":
                response = requests.post(
                    url, headers=headers, data=data, timeout=timeout
                )
            elif method == "put":
                response = requests.put(
                    url, headers=headers, data=data, timeout=timeout
                )
            elif method == "delete":
                response = requests.delete(url, headers=headers, timeout=timeout)
            else:
                return {"error": f"Unsupported method: {method}"}

            response.raise_for_status()

            return {
                "status_code": response.status_code,
                "content": response.text,
                "headers": {k: v for (k, v) in response.headers.items()},
            }

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    async def tool_status(self, url: str):
        """Comprueba el estado de un sitio web.

        Args:
            url (str): La URL del sitio web.

        Returns:
            dict: Un diccionario con el código de estado HTTP en la clave 'status_code' o un mensaje de error en la clave 'error'.
        """
        try:
            response = requests.get(
                url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5
            )
            response.raise_for_status()
            status_code = response.status_code
            return {"status_code": status_code}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

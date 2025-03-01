### en dessarrollo ###
from typing import Any, Dict

import requests

from ..tool_pack import ToolPack


class HttpPack(ToolPack):
    name = "http"

    async def tool_request(
        self,
        url: str,
        method: str = "get",
        data: str = None,  # type: ignore
    ) -> Dict[str, Any]:
        """
        Args:
            url (str): La URL a la que hacer la petición.
            method (str): El método HTTP a utilizar (get, post, put, delete). Por defecto, 'get'.
            data (str): Un json de datos a enviar con la petición (para métodos post y put). Por defecto, None.

        Returns:
            dict: Un diccionario con el código de estado HTTP en la clave 'status_code' y el contenido de la respuesta en la clave 'content'.
                  Si ocurre un error, devuelve un diccionario con un mensaje de error en la clave 'error'.
        """
        # headers: dict[str, str] = None,  # type: ignore
        # headers (dict): Un diccionario de cabeceras HTTP a enviar con la petición. Por defecto, None.
        try:
            method = method.lower()
            # if headers is None:  # type: ignore
            #    headers = {"User-Agent": "Mozilla/5.0"}
            headers = {"User-Agent": "Mozilla/5.0"}

            if method == "get":
                response = requests.get(url, headers=headers)
            elif method == "post":
                response = requests.post(url, headers=headers, data=data)
            elif method == "put":
                response = requests.put(url, headers=headers, data=data)
            elif method == "delete":
                response = requests.delete(url, headers=headers)
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
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            status_code = response.status_code
            return {"status_code": status_code}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

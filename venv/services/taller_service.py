
from typing import Optional
import httpx
from httpx import Request
from httpx import Response
from infrastructure.constants import APITaller
from infrastructure import cookie_autoriz
from fastapi import status


async def get_taller(request: Request, id_taller: int) -> Optional[dict]:

    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/taller/{id_taller}/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    taller = response.json()
    return taller


async def get_producto_taller(id_taller: int, id_producto: int, cod_agrupador: int) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/taller/{id_taller}/producto/{id_producto}/agrupador/{cod_agrupador}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    producto = response.json()
    return producto


async def get_lista_agrupadores() -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/agrupador/lista"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    agrupadores = response.json()
    return agrupadores


async def update_producto_taller(request: Request, producto: dict) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/taller/producto/agrupador"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.put(url, json=producto, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    producto = response.json()
    return producto


async def insert_producto_taller(producto: dict) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/taller/producto/agrupador"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.post(url, json=producto, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            error_message = str(e)
            if e.response.status_code == status.HTTP_409_CONFLICT:
                return {
                    "msg_error": e.response.json()["detail"],
                    }

            raise Exception(f"Error en la llamada a la API respectiva. [{error_message}]")
        except httpx.RequestError as e:
            error_message = str(e)
            raise Exception(f"Error de conexión con la API respectiva. [{error_message}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    producto = response.json()
    return producto


async def get_taller_asignatura_lista(sigla: str) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/asignatura/{sigla}/taller/lista"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    talleres = response.json()
    return talleres

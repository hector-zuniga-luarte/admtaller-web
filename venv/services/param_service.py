
from typing import Optional
import httpx
from httpx import Request
from httpx import Response
from infrastructure.constants import APITaller


async def get_params_lista(id_usuario: int) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/param/lista"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    params = response.json()
    return params


async def get_param(request: Request, cod_param: int) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/param/{cod_param}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    param = response.json()
    return param


async def update_param(request: Request, param: dict) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/param"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.put(url, json=param, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    param = response.json()
    return param


async def get_periodo_lista(request: Request) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/param/periodo/lista"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    periodos = response.json()
    return periodos


async def get_periodo(request: Request, cod_periodo_academ: int) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/param/periodo/{cod_periodo_academ}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    periodo = response.json()
    return periodo


async def get_unidad_medida_lista(request: Request) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/unidad_medida/lista"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    unidades_medida = response.json()
    return unidades_medida


async def get_categoria_producto_lista(request: Request) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/categoria_producto/lista"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    categorias_producto = response.json()
    return categorias_producto

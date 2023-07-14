
from typing import Optional
import httpx
from httpx import Request
from httpx import Response
from infrastructure.constants import APITaller
from infrastructure import cookie_autoriz
from fastapi import status
from infrastructure.conversion import texto_fecha_formato_corto
from infrastructure.conversion import texto_fecha_formato_largo


async def get_programaciones_asignatura_lista(ano_academ: int, id_usuario: int) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/programacion/asignatura/{ano_academ}/{id_usuario}/lista"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    programaciones = response.json()
    return programaciones


async def delete_programacion_asignatura(request: Request, ano_academ: int, cod_periodo_academ: int, sigla: str, seccion: int) -> Optional[dict]:

    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)
    error_message: str = None

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/programacion/eliminar/ano_academ/{ano_academ}/cod_periodo_academ/{cod_periodo_academ}/sigla/{sigla}/seccion/{seccion}/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.delete(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            error_message = e.response.json().get("detail")
            if "409" not in str(e):
                raise Exception(f"Error en la llamada a la API respectiva. [{error_message}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    eliminacion = response.json()
    return eliminacion


async def insert_programacion_asignatura(programacion: dict) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/programacion/asignatura/ano_academ/periodo/seccion"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.post(url, json=programacion, follow_redirects=True)
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
    programacion = response.json()
    return programacion


async def get_programaciones_taller_lista(ano_academ: int, cod_periodo_academ: int, sigla: str, seccion: int) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/programacion/ano_academ/{ano_academ}/periodo/{cod_periodo_academ}/sigla/{sigla}/seccion/{seccion}/lista"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    programaciones = response.json()

    # Generamos los formatos de fecha necesarios
    for row in programaciones:
        row["fecha_formato_corto"] = texto_fecha_formato_corto(row["fecha"])
        row["fecha_formato_largo"] = texto_fecha_formato_largo(row["fecha"])

    return programaciones


async def get_programacion_taller(ano_academ, cod_periodo_academ, sigla, seccion, id_taller, fecha) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/programacion/ano_academ/{ano_academ}/periodo/{cod_periodo_academ}/sigla/{sigla}/seccion/{seccion}/taller/{id_taller}/fecha/{fecha}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    programacion = response.json()

    programacion["fecha_formato_corto"] = texto_fecha_formato_corto(programacion["fecha"])
    programacion["fecha_formato_largo"] = texto_fecha_formato_largo(programacion["fecha"])

    return programacion


async def delete_programacion_taller(request: Request, ano_academ: int, cod_periodo_academ: int, sigla: str, seccion: int, id_taller: int, fecha: str) -> Optional[dict]:

    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)
    error_message: str = None

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/programacion/eliminar/ano_academ/{ano_academ}/cod_periodo_academ/{cod_periodo_academ}/sigla/{sigla}/seccion/{seccion}/taller/{id_taller}/fecha/{fecha}/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.delete(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            error_message = e.response.json().get("detail")
            if "409" not in str(e):
                raise Exception(f"Error en la llamada a la API respectiva. [{error_message}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    eliminacion = response.json()
    return eliminacion


async def update_programacion_taller(request: Request, programacion: dict) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/programacion/ano_academ/periodo/sigla/seccion/taller/fecha"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.put(url, json=programacion, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    programacion = response.json()
    return programacion


async def insert_programacion_taller(programacion: dict) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/programacion/asignatura/ano_academ/periodo/seccion/taller/fecha"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.post(url, json=programacion, follow_redirects=True)
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
    programacion = response.json()
    return programacion

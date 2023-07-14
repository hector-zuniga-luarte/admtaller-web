
from typing import Optional
import httpx
from httpx import Response
from infrastructure.constants import APITaller
from fastapi import status
from infrastructure.conversion import texto_fecha_formato_corto


async def get_registros_asignatura_lista(ano_academ: int, id_usuario: int) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/registro/asignatura/ano_academ/{ano_academ}/docente/{id_usuario}/lista"

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


async def get_registros_taller_lista(ano_academ: int, cod_periodo_academ: int, sigla: str, seccion: int, id_usuario: int) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/registro/asignatura/ano_academ/{ano_academ}/periodo/{cod_periodo_academ}/asignatura/{sigla}/seccion/{seccion}/docente/{id_usuario}/lista"

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

    return programaciones


async def registro_taller(registro: dict) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/registro/taller"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.post(url, json=registro, follow_redirects=True)
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
    registro = response.json()
    return registro

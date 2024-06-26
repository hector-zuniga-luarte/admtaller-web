
from typing import Optional
import httpx
from httpx import Request
from httpx import Response
from infrastructure.constants import APITaller
from infrastructure import cookie_autoriz
from infrastructure.constants import Perfil
from services import usuario_service
from infrastructure.constants import Perfil
from fastapi import status


async def get_asignaturas_lista(id_usuario: int) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/asignatura/lista/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    asignaturas = response.json()

    # Determinamos el perfil del usuario conectado de manera que se elimine la información de costos para docentes
    perfil = await usuario_service.get_perfil(id_usuario)
    cod_perfil = int(perfil["cod_perfil"])
    if cod_perfil == Perfil.K_DOCENTE.value:
        # Eliminamos las columnas con datos sensibles para ese perfil de usuario
        asignaturas = [{sel: item for sel, item in a.items() if sel != "costo_total"} for a in asignaturas]

    return asignaturas


async def delete_asignatura(request: Request, sigla: str) -> Optional[dict]:

    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)
    error_message: str = None

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/asignatura/eliminar/{sigla}/{id_usuario}"

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


async def get_asignatura(request: Request, sigla: str) -> Optional[dict]:

    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/asignatura/{sigla}/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    asignatura = response.json()

    return asignatura


async def update_asignatura(request: Request, asignatura: dict) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/asignatura"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.put(url, json=asignatura, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    asignatura = response.json()
    return asignatura


async def insert_asignatura(asignatura: dict) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/asignatura"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.post(url, json=asignatura, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:

            if e.response.status_code == status.HTTP_409_CONFLICT:
                return {
                    "msg_error": e.response.json()["detail"],
                    }

            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    asignatura = response.json()
    return asignatura


async def get_talleres_lista(sigla: str, id_usuario: int) -> Optional[dict]:
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

    # Determinamos el perfil del usuario conectado de manera que se elimine la información de costos para docentes
    perfil = await usuario_service.get_perfil(id_usuario)
    cod_perfil = int(perfil["cod_perfil"])
    if cod_perfil == Perfil.K_DOCENTE.value:
        # Eliminamos las columnas con datos sensibles para ese perfil de usuario
        talleres = [{sel: item for sel, item in a.items() if sel != "costo_total"} for a in talleres]

    return talleres


async def get_nom_asignatura(sigla: str, id_usuario: int) -> Optional[str]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/asignatura/{sigla}/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    nom_asignatura = response.json()["nom_asignatura"]
    return nom_asignatura


async def delete_taller(request: Request, sigla: str, id_taller: int) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/taller/eliminar/{id_taller}"

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


async def get_taller(id_taller: int, id_usuario: int) -> Optional[dict]:
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
    asignaturas = response.json()
    return asignaturas


async def update_taller(request: Request, taller: dict) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/taller"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.put(url, json=taller, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    taller = response.json()
    return taller


async def insert_taller(taller: dict) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/taller"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.post(url, json=taller, follow_redirects=True)
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
    taller = response.json()
    return taller


async def get_productos_lista(sigla: str, id_taller: int, id_usuario: int) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/taller/{id_taller}/producto/lista"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    productos = response.json()

    # Determinamos el perfil del usuario conectado de manera que se elimine la información de costos para docentes
    perfil = await usuario_service.get_perfil(id_usuario)
    cod_perfil = int(perfil["cod_perfil"])
    if cod_perfil == Perfil.K_DOCENTE.value:
        # Eliminamos las columnas con datos sensibles para ese perfil de usuario
        productos = [{sel: item for sel, item in p.items() if sel not in ["precio", "total"]} for p in productos]

    return productos


async def delete_producto_taller(request: Request, sigla: str, id_taller: int, id_producto: int, cod_agrupador: int) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/taller/eliminar/{id_taller}/producto/{id_producto}/agrupador/{cod_agrupador}"

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

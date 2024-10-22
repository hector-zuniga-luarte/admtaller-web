
from typing import Optional
import httpx
from httpx import Request
from httpx import Response
from infrastructure.constants import APITaller
from infrastructure import cookie_autoriz
from infrastructure.hash import hash_text


async def get_id_usuario_by_login(login: str) -> Optional[int]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/usuario/id_usuario/{login}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    id_usuario: int = response.json()["id_usuario"]
    return id_usuario


async def autenticacion(login: str, password: str) -> Optional[dict]:
    autenticacion = {
        "login": login,
        "hash_password": password,
        "autenticado": False,
    }

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/autenticacion"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.post(url, json=autenticacion, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    autenticacion = response.json()
    return autenticacion


async def get_perfil(id_usuario: int) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/perfil/usuario/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    perfil = response.json()
    return perfil


async def get_ano_academ() -> Optional[int]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/param/ano_academ/valor"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    ano_academ: int = response.json()["ano_academ"]
    return ano_academ


async def get_nom_carrera(id_usuario: int) -> Optional[str]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/perfil/nom_carrera/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    nom_carrera: str = response.json()["nom_carrera"]
    if not nom_carrera:
        return ""
    return nom_carrera.strip()


async def get_cod_carrera(id_usuario: int) -> Optional[int]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/perfil/cod_carrera/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    cod_carrera: int = response.json()["cod_carrera"]
    return cod_carrera


async def get_usuarios_lista(id_usuario: int) -> Optional[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/usuario/lista/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    usuarios = response.json()
    return usuarios


async def delete_usuario(request: Request, id_usuario_eliminar: int) -> Optional[dict]:

    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)
    error_message: str = None

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/usuario/eliminar/{id_usuario_eliminar}/{id_usuario}"

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


async def get_usuario(request: Request, id_usuario_get: int) -> Optional[dict]:

    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/usuario/{id_usuario_get}/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    usuario = response.json()
    return usuario


async def update_usuario(request: Request, usuario: dict) -> Optional[dict]:

    print("Hola")


    # Recuperamos el usuario conectado desde la cookie para pasarlo a los servicios como parámetro para segmentar datos
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/usuario/{id_usuario}"

    print(url)

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.put(url, json=usuario, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    usuario = response.json()
    return usuario


async def insert_usuario(usuario: dict) -> Optional[dict]:

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/usuario"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.post(url, json=usuario, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    usuario = response.json()
    return usuario


async def cambio_password(request: Request, nueva_password: str, confirmacion_nueva_password: str) -> bool:
    # Recuperamos el usuario conectado desde la cookie para pasarlo al servicio de cambio de contraseña
    id_usuario = cookie_autoriz.get_id_usuario_cookie(request)

    cambio_password: dict = {
        "id_usuario": id_usuario,
        "nueva_password": hash_text(nueva_password),
        "confirmacion_password": hash_text(confirmacion_nueva_password),
        "modificada": False,
    }

    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/autenticacion/password"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.put(url, json=cambio_password, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    cambio_password = response.json()
    return cambio_password["modificada"]

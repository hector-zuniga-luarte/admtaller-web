
from typing import List
from infrastructure.constants import APITaller
import httpx
from httpx import Response


async def get_dashboard(id_usuario: int) -> List[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/principal/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    dashboard = response.json()
    return dashboard

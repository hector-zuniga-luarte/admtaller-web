
from typing import List
from infrastructure.constants import APITaller
import httpx
from httpx import Response
from datetime import date


async def get_reporte_valorizacion_taller(cod_reporte: int, id_usuario: int) -> List[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/consulta/{cod_reporte}/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    reporte = response.json()
    return reporte


async def get_reporte_presupuesto_estimado_asignatura(cod_reporte: int, ano_academ: int, id_usuario: int) -> List[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/consulta/{cod_reporte}/ano_academ/{ano_academ}/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    # Si todo está correcto, Retornamos la respuesta de la API
    reporte = response.json()
    return reporte


async def get_reporte_asignacion_registro_docentes(cod_reporte: int, ano_academ: int, id_usuario: int) -> List[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/consulta/{cod_reporte}/ano_academ/{ano_academ}/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    reporte = response.json()

    # Calculamos porcentaje de avance en el registro
    for row in reporte:
        row["porcentaje_registro"] = None if row["total_taller_asignado"] == 0 else round(row["total_taller_registrado"] / row["total_taller_asignado"], 2)

    # Si todo está correcto, Retornamos la respuesta de la API
    return reporte


async def get_reporte_resumen_producto_rango_fechas(cod_reporte: int, ano_academ: int, fecha_inicio: date, fecha_termino: date, id_usuario: int) -> List[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/consulta/{cod_reporte}/ano_academ/{ano_academ}/fecha_inicio/{fecha_inicio}/fecha_termino/{fecha_termino}/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    reporte = response.json()
    return reporte


async def get_reporte_detalle_producto_taller_rango_fechas(cod_reporte: int, ano_academ: int, fecha_inicio: date, fecha_termino: date, id_usuario: int) -> List[dict]:
    # Armamos la URL de la API respectiva
    url = f"{APITaller.URL_BASE.value}/consulta/{cod_reporte}/ano_academ/{ano_academ}/fecha_inicio/{fecha_inicio}/fecha_termino/{fecha_termino}/{id_usuario}"

    async with httpx.AsyncClient() as client:
        try:
            response: Response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error en la llamada a la API respectiva. [{str(e)}]")
        except httpx.RequestError as e:
            raise Exception(f"Error de conexión con la API respectiva. [{str(e)}]")

    reporte = response.json()
    return reporte

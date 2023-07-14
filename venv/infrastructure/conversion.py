
from datetime import datetime


# Rutina que convierte un texto a número manejando la excepción en caso de no poder convertirlo
def convierte_entero(text) -> int:
    try:
        return int(text)
    except ValueError:
        return 0


# Transforma un string de fecha en formato "yyyy-mm-dd" en formato corto "lun 16.01.1967"
def texto_fecha_formato_corto(fecha_str) -> str:
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    except ValueError:
        return "fecha inválida"

    # Diccionario para mapear los valores numéricos de los días de la semana a los nombres abreviados en español
    dias_semana_formato = {
        0: "lun",
        1: "mar",
        2: "mié",
        3: "jue",
        4: "vie",
        5: "sáb",
        6: "dom"
    }

    # Obtener el número del día de la semana (0: lunes, 1: martes, ..., 6: domingo)
    numero_dia_semana = fecha.weekday()

    # Obtener el nombre abreviado del día de la semana en español a partir del diccionario
    nombre_dia_semana_formato_corto = dias_semana_formato.get(numero_dia_semana)

    # Obtener el día del mes con ceros a la izquierda
    dia = fecha.strftime("%d")

    # Obtener el mes con ceros a la izquierda
    mes = fecha.strftime("%m")

    # Obtener el año
    ano = fecha.strftime("%Y")

    # Construir la cadena de formato deseada
    return f"{nombre_dia_semana_formato_corto} {dia}.{mes}.{ano}"


# Transforma un string de fecha en formato "yyyy-mm-dd" en formato largo "lunes 16 de enero de 1967"
def texto_fecha_formato_largo(fecha_str) -> str:
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    except ValueError:
        return "fecha inválida"

    # Diccionario para mapear los valores numéricos de los días de la semana a los nombres abreviados en español
    dias_semana_formato = {
        0: "lunes",
        1: "martes",
        2: "miércoles",
        3: "jueves",
        4: "viernes",
        5: "sábado",
        6: "domingo"
    }
    meses_formato = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "septiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre",
    }

    fecha = datetime.strptime(fecha_str, "%Y-%m-%d") 

    # Obtener el número del día de la semana (0: lunes, 1: martes, ..., 6: domingo)
    numero_dia_semana = fecha.weekday()
    numero_mes = fecha.month

    # Obtener el nombre abreviado del día de la semana en español a partir del diccionario
    nombre_dia_semana_formato_largo = dias_semana_formato.get(numero_dia_semana)
    nombre_mes_formato_largo = meses_formato.get(numero_mes)

    # Obtener el día
    dia = fecha.strftime("%d").lstrip("0")

    # Obtener el año
    ano = fecha.strftime("%Y")

    # Construir la cadena de formato deseada
    return f"{nombre_dia_semana_formato_largo} {dia} de {nombre_mes_formato_largo} de {ano}"


from enum import Enum


class APITaller(str, Enum):
    URL_BASE = "http://localhost:8001/api"


class Mensajes(str, Enum):
    ERR_NO_AUTENTICADO = "El usuario no está correctamente autenticado"

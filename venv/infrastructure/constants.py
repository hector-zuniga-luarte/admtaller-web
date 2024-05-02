
from enum import Enum


class APITaller(str, Enum):
    URL_BASE = "http://localhost:8001/api"


class Mensajes(str, Enum):
    ERR_NO_AUTENTICADO = "El usuario no está correctamente autenticado"

class Perfil(int, Enum):
    K_ADMINISTRADOR_TI = 0
    K_ADMINISTRADOR_CARRERA = 1
    K_DOCENTE = 2
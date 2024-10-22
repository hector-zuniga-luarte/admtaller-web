
from typing import Optional
from starlette.requests import Request

from infrastructure import cookie_autoriz


# Se genera el viemodel base que permite recuperar sus datos e información del error con un simple to_dict()
class ViewModelBase:
    def __init__(self, request: Request):

        # Se aprovecha que al setear el request, FastAPI transforma todo a un diccionario JSON
        self.request: Request = request

        # Para retornar errores y mensajes de éxito
        self.msg_error: Optional[str] = None
        self.msg_exito: Optional[str] = None

        # Indicador de si está o no con una sesión activa en el sistema
        # Se obtendrá de las cookies
        self.esta_conectado: bool = (False if cookie_autoriz.get_id_usuario_cookie(self.request) is None else True)

        # Identificadores del usuario que usa el viewmodel
        self.id_usuario_conectado: Optional[int] = cookie_autoriz.get_id_usuario_cookie(request)
        self.login_conectado: Optional[str] = cookie_autoriz.get_login_cookie(request)

        # El perfil del usuario conectado
        self.cod_perfil_conectado: Optional[int] = cookie_autoriz.get_cod_perfil_cookie(request)

        # El año académico en curso
        self.ano_academ: Optional[int] = cookie_autoriz.get_ano_academ_cookie(request)

        # El nombre de la carrera a la que pertenece el usuario
        self.nom_carrera: Optional[str] = cookie_autoriz.get_nom_carrera_cookie(request)

        # El código de la carrera a la que pertenece el usuario
        self.cod_carrera: Optional[int] = cookie_autoriz.get_cod_carrera_cookie(request)

        # Método del request. ütil para saber cuándo mostrar mensajes de grabación exitosos
        self.method = request.method

    # Salida en formato diccionario (JSON)
    def to_dict(self) -> dict:
        return self.__dict__

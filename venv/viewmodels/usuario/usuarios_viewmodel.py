
from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import usuario_service
from infrastructure.constants import Mensajes


class UsuariosViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.usuarios: List[dict] = []

    # Función que carga datos y verifica si está conectado al sistema
    async def load(self):
        if self.esta_conectado:
            self.usuarios = await usuario_service.get_usuarios_lista(self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

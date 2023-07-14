
from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import principal_service
from infrastructure.constants import Mensajes


class PrincipalViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.dashboard: List[dict] = []

    # Función que carga datos que verifica si está conectado al sistema
    async def load(self):
        if self.esta_conectado:
            self.dashboard = await principal_service.get_dashboard(self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value


from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import param_service
from infrastructure.constants import Mensajes


class ParamsViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.params: List[dict] = []

    # Función que carga datos y verifica si está conectado al sistema
    async def load(self):
        if self.esta_conectado:
            self.params = await param_service.get_params_lista(self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

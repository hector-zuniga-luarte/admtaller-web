
from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import asignatura_service
from infrastructure.constants import Mensajes


class AsignaturasViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.asignaturas: List[dict] = []

    # Función que carga datos y verifica si está conectado al sistema
    async def load(self):
        if self.esta_conectado:
            self.asignaturas = await asignatura_service.get_asignaturas_lista(self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

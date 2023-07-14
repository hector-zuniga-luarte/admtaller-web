
from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import registro_service
from infrastructure.constants import Mensajes


class RegistrosAsignaturaViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.registros_asignatura: List[dict] = []

    # Función que carga datos y verifica si está conectado al sistema
    async def load(self):
        if self.esta_conectado:
            self.registros_asignatura = await registro_service.get_registros_asignatura_lista(self.ano_academ, self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

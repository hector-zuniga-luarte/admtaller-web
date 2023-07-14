
from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import programacion_service
from infrastructure.constants import Mensajes


class ProgramacionesAsignaturaViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.programaciones_asignatura: List[dict] = []

    # Función que carga datos y verifica si está conectado al sistema
    async def load(self):
        if self.esta_conectado:
            self.programaciones_asignatura = await programacion_service.get_programaciones_asignatura_lista(self.ano_academ, self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

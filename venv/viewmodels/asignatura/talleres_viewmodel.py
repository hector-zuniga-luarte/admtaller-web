
from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import asignatura_service
from infrastructure.constants import Mensajes


class TalleresViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.sigla: str = None
        self.nom_asignatura: str = None
        self.talleres: List[dict] = []

    # Función que carga datos y verifica si está conectado al sistema
    async def load(self, sigla):
        if self.esta_conectado:
            self.sigla = sigla
            self.nom_asignatura = await asignatura_service.get_nom_asignatura(self.sigla, self.id_usuario_conectado)
            self.talleres = await asignatura_service.get_talleres_lista(self.sigla)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

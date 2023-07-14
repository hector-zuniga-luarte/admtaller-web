
from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import programacion_service
from services import param_service
from services import asignatura_service
from infrastructure.constants import Mensajes


class ProgramacionesTallerViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.cod_periodo_academ: int
        self.sigla: str
        self.seccion: int
        self.nom_periodo_academ: int
        self.nom_asignatura: str
        self.programaciones_taller: List[dict] = []

    # Función que carga datos y verifica si está conectado al sistema
    async def load(self, cod_periodo_academ, sigla, seccion):
        if self.esta_conectado:
            self.cod_periodo_academ = cod_periodo_academ
            self.sigla = sigla
            self.seccion = seccion

            periodo_academ = await param_service.get_periodo(self.request, self.cod_periodo_academ)
            self.nom_periodo_academ = periodo_academ["nom_periodo_academ"]
            self.nom_asignatura = await asignatura_service.get_nom_asignatura(self.sigla, self.id_usuario_conectado)
            self.programaciones_taller = await programacion_service.get_programaciones_taller_lista(self.ano_academ, cod_periodo_academ, sigla, seccion)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value


from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import asignatura_service
from services import registro_service
from services import param_service
from infrastructure.constants import Mensajes


class RegistrosTallerViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.cod_periodo_academ: int
        self.sigla: str
        self.seccion: int
        self.nom_periodo_academ: str
        self.nom_asignatura: str

        self.registros_taller: List[dict] = []

    # Función que carga datos y verifica si está conectado al sistema
    async def load(self, cod_periodo_academ, sigla, seccion):
        if self.esta_conectado:
            self.cod_periodo_academ = cod_periodo_academ
            self.sigla = sigla
            self.seccion = seccion

            asignatura = await asignatura_service.get_asignatura(self.request, self.sigla)
            self.nom_asignatura = asignatura["nom_asignatura"]
            param = await param_service.get_periodo(self.request, self.cod_periodo_academ)
            self.nom_periodo_academ = param["nom_periodo_academ"]

            self.registros_taller = await registro_service.get_registros_taller_lista(self.ano_academ, cod_periodo_academ, sigla, seccion, self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

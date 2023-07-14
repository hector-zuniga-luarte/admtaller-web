
from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import reporte_service
from infrastructure.constants import Mensajes


class ReporteValorizacionTaller(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.registros: List[dict] = []

    # Función que carga datos y verifica si está conectado al sistema
    async def load(self):
        K_COD_REPORTE = 1
        if self.esta_conectado:
            self.registros = await reporte_service.get_reporte_valorizacion_taller(K_COD_REPORTE, self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

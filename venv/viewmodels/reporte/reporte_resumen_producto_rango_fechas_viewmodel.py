
from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import reporte_service
from infrastructure.constants import Mensajes
from infrastructure.conversion import texto_fecha_formato_largo

from datetime import date
from datetime import datetime
from datetime import timedelta


class ReporteResumenProductoRangoFechas(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.fecha_inicio: date
        self.fecha_termino: date
        self.fecha_inicio_formato_largo: str
        self.fecha_termino_formato_largo: str
        self.total: int

        self.registros: List[dict] = []

    # Función de carga del formulario para hacer la primera consulta
    async def load_empty(self):
        hoy = datetime.today().date()
        self.fecha_inicio = hoy + timedelta(days=(7 - hoy.weekday()))
        self.fecha_termino = hoy + timedelta(days=(13 - hoy.weekday()))
        self.fecha_inicio_formato_largo = texto_fecha_formato_largo(self.fecha_inicio.strftime("%Y-%m-%d"))
        self.fecha_termino_formato_largo = texto_fecha_formato_largo(self.fecha_termino.strftime("%Y-%m-%d"))
        self.total = 0


    # Función que carga datos y verifica si está conectado al sistema
    async def load(self, fecha_inicio, fecha_termino):
        K_COD_REPORTE = 4
        self.fecha_inicio = fecha_inicio
        self.fecha_termino = fecha_termino
        self.fecha_inicio_formato_largo = texto_fecha_formato_largo(self.fecha_inicio.strftime("%Y-%m-%d"))
        self.fecha_termino_formato_largo = texto_fecha_formato_largo(self.fecha_termino.strftime("%Y-%m-%d"))
        if self.esta_conectado:
            self.registros = await reporte_service.get_reporte_resumen_producto_rango_fechas(K_COD_REPORTE, self.ano_academ, self.fecha_inicio, self.fecha_termino, self.id_usuario_conectado)
            self.total = sum(r["precio_total_productos"] for r in self.registros)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

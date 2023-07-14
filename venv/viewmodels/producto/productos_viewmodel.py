
from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import programacion_service
from services import param_service
from services import asignatura_service
from services import producto_service
from infrastructure.constants import Mensajes


class ProductosViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.productos: List[dict] = []

    # Función que carga datos y verifica si está conectado al sistema
    async def load(self):
        if self.esta_conectado:
            self.productos = await producto_service.get_lista_productos(self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value


from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import param_service
from infrastructure.constants import Mensajes
from infrastructure.conversion import convierte_entero


class ParamViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.cod_param: int
        self.nom_param: str
        self.valor: str

        self.param: dict

    async def validate(self) -> bool:
        # Verificar si el parámetro 1 es un año válido
        if convierte_entero(self.valor) == 0 and self.cod_param == 1:
            self.msg_error = "El parámetro debe ser un valor entero"
            return False

        if convierte_entero(self.valor) < 2023 and self.cod_param == 1:
            self.msg_error = "El parámetro debe ser un año mayor o igual a 2023"
            return False

        return True

    # Función que carga datos y verifica si está conectado al sistema
    async def update(self):
        # Recuperamos los datos desde el formulario
        form = await self.request.form()
        self.cod_param = int(form.get("cod-param", "").strip())
        self.nom_param = form.get("nom-param", "")
        self.valor = form.get("valor", "").strip()

        self.param = {
            "cod_param": self.cod_param,
            "nom_param": self.nom_param,
            "valor": self.valor,
        }

        if await self.validate():
            self.param = await param_service.update_param(self.request, self.param)

            if not self.param:
                self.msg_error = "Error al modificar el parámetro"
            else:
                self.msg_exito = "Se ha modificado correctamente el parámetro"

    async def load(self, cod_param):
        if self.esta_conectado:
            self.param = await param_service.get_param(self.request, cod_param)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

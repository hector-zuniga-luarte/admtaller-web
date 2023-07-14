
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import asignatura_service
from infrastructure.constants import Mensajes


class TallerViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.taller: dict
        self.id_taller: int
        self.titulo_preparacion: str
        self.detalle_preparacion: str
        self.sigla: str
        self.nom_asignatura: str

    async def validate(self) -> bool:
        result: bool = True

        return result

    # Función que permite visualizar un formulario para registros nuevos en el sistema
    async def load_empty(self, sigla):
        K_NUEVOREGISTRO: int = 0
        if self.esta_conectado:
            self.sigla = sigla
            self.nom_asignatura = await asignatura_service.get_nom_asignatura(self.sigla, self.id_usuario_conectado)
            self.taller = await asignatura_service.get_taller(K_NUEVOREGISTRO, self.id_usuario_conectado)
            self.taller["sigla"] = sigla
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

    # Función que carga datos y verifica si está conectado al sistema
    async def update(self):
        # Recuperamos los datos desde el formulario
        form = await self.request.form()
        self.id_taller = int(form.get("id-taller", "").strip())
        self.sigla = form.get("sigla", "").strip()
        self.titulo_preparacion = form.get("titulo-preparacion", "").strip()
        self.detalle_preparacion = form.get("detalle-preparacion", "").strip()
        self.semana = int(form.get("semana", "").strip())

        self.taller = {
            "id_taller": self.id_taller,
            "titulo_preparacion": self.titulo_preparacion,
            "detalle_preparacion": self.detalle_preparacion,
            "semana": self.semana,
            "sigla": self.sigla,
        }

        if await self.validate():
            self.taller = await asignatura_service.update_taller(self.request, self.taller)

            if not self.taller:
                self.msg_error = "Error al modificar el taller"
            else:
                self.msg_exito = "Se ha modificado correctamente el taller"

    # Función que carga datos y verifica si está conectado al sistema
    async def insert(self):
        # Recuperamos los datos desde el formulario
        form = await self.request.form()
        self.id_taller = int(form.get("id-taller", "").strip())
        self.sigla = form.get("sigla", "").strip()
        self.titulo_preparacion = form.get("titulo-preparacion", "").strip()
        self.detalle_preparacion = form.get("detalle-preparacion", "").strip()
        self.semana = int(form.get("semana", "").strip())

        self.taller = {
            "id_taller": self.id_taller,
            "titulo_preparacion": self.titulo_preparacion,
            "detalle_preparacion": self.detalle_preparacion,
            "semana": self.semana,
            "sigla": self.sigla,
        }

        if await self.validate():
            taller = await asignatura_service.insert_taller(self.taller)
            if "msg_error" in taller:
                self.msg_error = taller["msg_error"]
            else:
                self.taller = taller

            if not self.taller:
                self.msg_error = "Error al agregar el taller"
            else:
                self.id_taller = self.taller["id_taller"]
                self.msg_exito = "Se ha agregado correctamente el taller"

    async def load(self, sigla, id_taller):
        if self.esta_conectado:
            self.sigla = sigla
            self.taller = await asignatura_service.get_taller(id_taller, self.id_usuario_conectado)
            self.nom_asignatura = await asignatura_service.get_nom_asignatura(self.sigla, self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value


from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import asignatura_service
from services import carrera_service
from infrastructure.constants import Mensajes


class AsignaturaViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.asignatura: dict
        self.sigla: str
        self.nom_asignatura: str
        self.nom_asignatura_abrev: str
        self.cod_carrera: int
        self.lista_carrera: List[dict]

    async def validate(self) -> bool:
        result: bool = True

        return result

    # Función que permite visualizar un formulario para registros nuevos en el sistema
    async def load_empty(self):
        K_NUEVOREGISTRO: str = "None"
        if self.esta_conectado:
            self.asignatura = await asignatura_service.get_asignatura(self.request, K_NUEVOREGISTRO)
            self.lista_carrera = await carrera_service.get_carrera_lista(self.request, self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

    # Función que carga datos y verifica si está conectado al sistema
    async def update(self):
        # Recuperamos los datos desde el formulario
        form = await self.request.form()
        self.sigla = form.get("sigla", "").strip()
        self.nom_asignatura = form.get("nom-asignatura", "").strip()
        self.nom_asignatura_abrev = form.get("nom-asignatura-abrev", "").strip()
        self.cod_carrera = int(form.get("cod-carrera", "").strip())

        self.asignatura = {
            "sigla": self.sigla,
            "nom_asignatura": self.nom_asignatura,
            "nom_asignatura_abrev": self.nom_asignatura_abrev,
            "cod_carrera": self.cod_carrera,
        }
        self.lista_carrera = await carrera_service.get_carrera_lista(self.request, self.id_usuario_conectado)

        if await self.validate():
            # Encriptamos la password antes de pasarla al servicio

            self.asignatura = await asignatura_service.update_asignatura(self.request, self.asignatura)

            if not self.asignatura:
                self.msg_error = "Error al modificar la asignatura"
            else:
                self.msg_exito = "Se ha modificado correctamente la asignatura"

    # Función que carga datos y verifica si está conectado al sistema
    async def insert(self):
        # Recuperamos los datos desde el formulario
        form = await self.request.form()
        self.sigla = form.get("sigla", "").strip()
        self.nom_asignatura = form.get("nom-asignatura", "").strip()
        self.nom_asignatura_abrev = form.get("nom-asignatura-abrev", "").strip()
        self.cod_carrera = int(form.get("cod-carrera", "").strip())

        self.asignatura = {
            "sigla": self.sigla,
            "nom_asignatura": self.nom_asignatura,
            "nom_asignatura_abrev": self.nom_asignatura_abrev,
            "cod_carrera": self.cod_carrera,
        }
        self.lista_carrera = await carrera_service.get_carrera_lista(self.request, self.id_usuario_conectado)

        if await self.validate():
            asignatura = await asignatura_service.insert_asignatura(self.asignatura)
            if "msg_error" in asignatura:
                self.msg_error = asignatura["msg_error"]
            else:
                self.asignatura = asignatura

            if not self.asignatura:
                self.msg_error = "Error al agregar la asignatura"
            else:
                self.sigla = self.asignatura["sigla"]
                self.msg_exito = "Se ha agregado correctamente la asignatura"

    async def load(self, sigla):
        if self.esta_conectado:
            self.asignatura = await asignatura_service.get_asignatura(self.request, sigla)
            self.lista_carrera = await carrera_service.get_carrera_lista(self.request, self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value


from typing import List

from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import asignatura_service
from services import param_service
from services import programacion_service
from infrastructure.constants import Mensajes
from infrastructure.cookie_autoriz import get_ano_academ_cookie


class ProgramacionAsignaturaViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.ano_academ: int
        self.cod_periodo_academ: int
        self.sigla: str
        self.seccion: int
        self.nom_periodo_academ: str
        self.nom_asignatura: str

        self.lista_periodos: List[dict]
        self.lista_asignaturas: List[dict]

    async def validate(self) -> bool:
        result: bool = True

        return result

    # Función que permite visualizar un formulario para registros nuevos en el sistema
    async def load_empty(self):
        K_PERIODO_DEFAULT: int = 1
        if self.esta_conectado:
            self.ano_academ = get_ano_academ_cookie(self.request)
            self.cod_periodo_academ = K_PERIODO_DEFAULT
            self.sigla = None
            self.seccion = None
            self.nom_periodo_academ = None
            self.nom_asignatura = None

            self.lista_periodos = await param_service.get_periodo_lista(self.request)
            self.lista_asignaturas = await asignatura_service.get_asignaturas_lista(self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

    # Función que carga datos y verifica si está conectado al sistema
    async def insert(self):
        # Recuperamos los datos desde el formulario
        form = await self.request.form()
        self.ano_academ = get_ano_academ_cookie(self.request)
        self.cod_periodo_academ = int(form.get("cod-periodo-academ", "").strip())
        self.sigla = form.get("sigla", "").strip()
        self.seccion = int(form.get("seccion", "").strip())

        periodo_academ = await param_service.get_periodo(self.request, self.cod_periodo_academ)
        self.nom_periodo_academ = periodo_academ["nom_periodo_academ"]
        self.nom_asignatura = await asignatura_service.get_nom_asignatura(self.sigla, self.id_usuario_conectado)
        self.programacion = {
            "ano_academ": self.ano_academ,
            "cod_periodo_academ": self.cod_periodo_academ,
            "sigla": self.sigla,
            "seccion": self.seccion,
            "nom_periodo_academ": self.nom_periodo_academ,
            "nom_asignatura": self.nom_asignatura,
        }

        if await self.validate():
            programacion = await programacion_service.insert_programacion_asignatura(self.programacion)
            if "msg_error" in programacion:
                self.msg_error = programacion["msg_error"]
            else:
                self.programacion = programacion

            if not self.programacion:
                self.msg_error = "Error al agregar la programación de la sección de la asignatura"
            else:
                self.lista_periodos = await param_service.get_periodo_lista(self.request)
                self.lista_asignaturas = await asignatura_service.get_asignaturas_lista(self.id_usuario_conectado)
                self.msg_exito = "Se ha agregado correctamente la programación de la sección de la asignatura"

    async def load(self, ano_academ, cod_periodo_academ, sigla, seccion):
        if self.esta_conectado:
            self.ano_academ = ano_academ
            self.cod_periodo_academ = cod_periodo_academ
            self.sigla = sigla
            self.seccion = seccion

            periodo_academ = await param_service.get_periodo(self.request, self.cod_periodo_academ)
            self.nom_periodo_academ = periodo_academ["nom_periodo_academ"]
            self.nom_asignatura = await asignatura_service.get_nom_asignatura(self.sigla, self.id_usuario_conectado)

            self.lista_periodos = await param_service.get_periodo_lista(self.request)
            self.lista_asignaturas = await asignatura_service.get_asignaturas_lista(self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

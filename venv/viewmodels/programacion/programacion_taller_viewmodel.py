
from typing import List
from typing import Optional
from datetime import date

from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import asignatura_service
from services import param_service
from services import programacion_service
from services import usuario_service
from services import taller_service
from infrastructure.constants import Mensajes
from infrastructure.cookie_autoriz import get_ano_academ_cookie


class ProgramacionTallerViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.fecha: str
        self.ano_academ: int
        self.cod_periodo_academ: int
        self.sigla: str
        self.seccion: int
        self.id_taller: int
        self.id_usuario: int
        
        self.nom_periodo_academ: Optional[str]
        self.nom_asignatura: Optional[str]

        self.lista_talleres: List[dict]
        self.lista_usuarios: List[dict]

    async def validate(self) -> bool:
        result: bool = True

        return result

    # Función que permite visualizar un formulario para registros nuevos en el sistema
    async def load_empty(self, sigla, cod_periodo_academ, seccion):
        if self.esta_conectado:
            self.ano_academ = get_ano_academ_cookie(self.request)
            self.cod_periodo_academ = cod_periodo_academ
            self.sigla = sigla
            self.seccion = seccion
            self.nom_periodo_academ = None
            self.nom_asignatura = None
            self.id_usuario = 0

            fecha_actual = date.today()
            self.fecha = fecha_actual.strftime("%Y-%m-%d")

            self.programacion = dict

            periodo_academ = await param_service.get_periodo(self.request, self.cod_periodo_academ)
            self.nom_periodo_academ = periodo_academ["nom_periodo_academ"]
            self.nom_asignatura = await asignatura_service.get_nom_asignatura(self.sigla, self.id_usuario_conectado)

            self.lista_usuarios = await usuario_service.get_usuarios_lista(self.id_usuario_conectado)
            self.lista_talleres = await taller_service.get_taller_asignatura_lista(self.sigla)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

    # Función que carga datos y verifica si está conectado al sistema
    async def insert(self, sigla, cod_periodo_academ, seccion):
        # Recuperamos los datos desde el formulario
        form = await self.request.form()
        self.ano_academ = get_ano_academ_cookie(self.request)
        self.sigla = sigla
        self.cod_periodo_academ = cod_periodo_academ
        self.seccion = seccion

        self.fecha = form.get("fecha", "").strip()
        self.id_taller = int(form.get("id-taller", "").strip())
        self.id_usuario = int(form.get("id-usuario", "").strip())

        self.programacion = {
            "fecha": self.fecha,
            "ano_academ": self.ano_academ,
            "cod_periodo_academ": self.cod_periodo_academ,
            "sigla": self.sigla,
            "seccion": self.seccion,
            "id_taller": self.id_taller,
            "id_usuario": self.id_usuario,
            "nom_periodo_academ": "",
            "nom_asignatura": "",
            "titulo_preparacion": "",
            "semana": 0,
            "login": "",
            "nom_preferido": "",
            "primer_apellido": "",
            "segundo_apellido": ""            
        }

        if await self.validate():
            programacion = await programacion_service.insert_programacion_taller(self.programacion)
            if "msg_error" in programacion:
                self.lista_usuarios = await usuario_service.get_usuarios_lista(self.id_usuario_conectado)
                self.lista_talleres = await taller_service.get_taller_asignatura_lista(self.sigla)
                self.msg_error = programacion["msg_error"]
            else:
                self.programacion = programacion

            if not self.programacion:
                self.msg_error = "Error al agregar la programación del taller de la asignatura"
            else:
                self.id_usuario = self.programacion["id_usuario"]
                periodo_academ = await param_service.get_periodo(self.request, self.cod_periodo_academ)
                self.nom_periodo_academ = periodo_academ["nom_periodo_academ"]
                self.nom_asignatura = await asignatura_service.get_nom_asignatura(self.sigla, self.id_usuario_conectado)

                self.lista_usuarios = await usuario_service.get_usuarios_lista(self.id_usuario_conectado)
                self.msg_exito = "Se ha agregado correctamente la programación del taller de la asignatura"

    async def load(self, sigla, cod_periodo_academ, seccion, id_taller, fecha):
        if self.esta_conectado:
            self.ano_academ = get_ano_academ_cookie(self.request)
            self.cod_periodo_academ = cod_periodo_academ
            self.sigla = sigla
            self.seccion = seccion
            self.id_taller = id_taller
            self.fecha = fecha

            self.programacion = await programacion_service.get_programacion_taller(self.ano_academ, self.cod_periodo_academ, self.sigla, self.seccion, self.id_taller, self.fecha)

            self.id_usuario = self.programacion["id_usuario"]
            periodo_academ = await param_service.get_periodo(self.request, self.cod_periodo_academ)
            self.nom_periodo_academ = periodo_academ["nom_periodo_academ"]
            self.nom_asignatura = await asignatura_service.get_nom_asignatura(self.sigla, self.id_usuario_conectado)

            self.lista_usuarios = await usuario_service.get_usuarios_lista(self.id_usuario_conectado)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

    # Función que carga datos y verifica si está conectado al sistema
    async def update(self, sigla, cod_periodo_academ, seccion, id_taller, fecha):
        # Recuperamos los datos desde el formulario
        form = await self.request.form()

        self.ano_academ = get_ano_academ_cookie(self.request)
        self.cod_periodo_academ = cod_periodo_academ
        self.sigla = sigla
        self.seccion = seccion
        self.id_taller = id_taller
        self.fecha = fecha

        self.id_usuario = int(form.get("id-usuario", "").strip())

        self.programacion = {
            "fecha": self.fecha,
            "ano_academ": self.ano_academ,
            "cod_periodo_academ": self.cod_periodo_academ,
            "sigla": self.sigla,
            "seccion": self.seccion,
            "id_taller": self.id_taller,
            "id_usuario": self.id_usuario,
            "nom_periodo_academ": "",
            "nom_asignatura": "",
            "titulo_preparacion": "",
            "semana": 0,
            "login": "",
            "nom_preferido": "",
            "primer_apellido": "",
            "segundo_apellido": ""            
        }

        if await self.validate():
            self.taller = await programacion_service.update_programacion_taller(self.request, self.programacion)

            if not self.taller:
                self.msg_error = "Error al modificar la programación del taller"
            else:
                self.msg_exito = "Se ha modificado correctamente la programación del taller"

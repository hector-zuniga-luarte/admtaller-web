
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import asignatura_service
from services import param_service
from services import programacion_service
from services import usuario_service
from services import taller_service
from services import registro_service
from infrastructure.constants import Mensajes
from infrastructure.cookie_autoriz import get_ano_academ_cookie
from infrastructure.conversion import texto_fecha_formato_largo


class RegistroTallerViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.fecha: str
        self.ano_academ: int
        self.cod_periodo_academ: int
        self.sigla: str
        self.seccion: int
        self.id_taller: int
        self.id_usuario: int
        self.obs: str

        self.nom_periodo_academ: str
        self.nom_asignatura: str
        self.semana: int
        self.titulo_preparacion: int
        self.fecha_formato_largo: str
        self.nom_preferido: str
        self.primer_apellido: str
        self.segundo_apellido: str

        self.registro: dict

    async def validate(self) -> bool:
        result: bool = True

        return result

    # Función que permite visualizar un formulario para registros nuevos en el sistema
    async def load_empty(self, sigla, cod_periodo_academ, seccion, id_taller, fecha, id_usuario, obs):
        if self.esta_conectado:
            self.fecha = fecha
            self.cod_periodo_academ = cod_periodo_academ
            self.sigla = sigla
            self.seccion = seccion
            self.id_taller = id_taller
            self.id_usuario = id_usuario
            self.obs = obs

            periodo = await param_service.get_periodo(self.request, self.cod_periodo_academ)
            self.nom_periodo_academ = periodo["nom_periodo_academ"]
            asignatura = await asignatura_service.get_asignatura(self.request, sigla)
            self.nom_asignatura = asignatura["nom_asignatura"]
            taller = await taller_service.get_taller(self.request, self.id_taller)
            self.semana = taller["semana"]
            self.titulo_preparacion = taller["titulo_preparacion"]
            usuario = await usuario_service.get_usuario(self.request, self.id_usuario)
            self.nom_preferido = usuario["nom_preferido"]
            self.primer_apellido = usuario["primer_apellido"]
            self.segundo_apellido = usuario["segundo_apellido"]

            self.fecha_formato_largo = texto_fecha_formato_largo(self.fecha)

        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

    # Función que carga datos y verifica si está conectado al sistema
    async def register(self, sigla, cod_periodo_academ, seccion, id_taller, fecha, id_usuario):
        # Recuperamos los datos desde el formulario
        form = await self.request.form()
        self.ano_academ = get_ano_academ_cookie(self.request)
        self.fecha = fecha
        self.cod_periodo_academ = cod_periodo_academ
        self.sigla = sigla
        self.seccion = seccion
        self.id_taller = id_taller
        self.id_usuario = id_usuario

        periodo = await param_service.get_periodo(self.request, self.cod_periodo_academ)
        self.nom_periodo_academ = periodo["nom_periodo_academ"]
        asignatura = await asignatura_service.get_asignatura(self.request, sigla)
        self.nom_asignatura = asignatura["nom_asignatura"]
        taller = await taller_service.get_taller(self.request, self.id_taller)
        self.semana = taller["semana"]
        self.titulo_preparacion = taller["titulo_preparacion"]
        usuario = await usuario_service.get_usuario(self.request, self.id_usuario)
        self.nom_preferido = usuario["nom_preferido"]
        self.primer_apellido = usuario["primer_apellido"]
        self.segundo_apellido = usuario["segundo_apellido"]

        self.fecha_formato_largo = texto_fecha_formato_largo(self.fecha)

        self.obs = form.get("obs", "").strip()

        self.registro = {
            "fecha": self.fecha,
            "ano_academ": self.ano_academ,
            "cod_periodo_academ": self.cod_periodo_academ,
            "sigla": self.sigla,
            "seccion": self.seccion,
            "id_taller": self.id_taller,
            "id_usuario": self.id_usuario,
            "obs": self.obs
        }

        if await self.validate():
            registro = await registro_service.registro_taller(self.registro)
            if "msg_error" in registro:
                self.msg_error = registro["msg_error"]
            else:
                self.registro = registro

            if not self.registro:
                self.msg_error = "Error al registrar el taller"
            else:
                self.msg_exito = "Se ha registrado correctamente el taller"

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

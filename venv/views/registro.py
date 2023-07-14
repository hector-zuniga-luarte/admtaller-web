
import fastapi
from fastapi_chameleon import template
from viewmodels.registro.registros_asignatura_viewmodel import RegistrosAsignaturaViewModel
from viewmodels.registro.registros_taller_viewmodel import RegistrosTallerViewModel
from viewmodels.registro.registro_taller_viewmodel import RegistroTallerViewModel
from starlette.requests import Request

router = fastapi.APIRouter()


@router.get("/registro/asignatura/lista")
@template(template_file="registro/registro_asignatura_lista.pt")
async def registro_asignatura_lista(request: Request):
    vm = RegistrosAsignaturaViewModel(request)
    await vm.load()

    return vm.to_dict()


@router.get("/registro/asignatura/{sigla}/periodo/{cod_periodo_academ}/seccion/{seccion}/lista")
@template(template_file="registro/registro_taller_lista.pt")
async def registro_taller_lista(request: Request, cod_periodo_academ: int, sigla: str, seccion: int):
    vm = RegistrosTallerViewModel(request)
    await vm.load(cod_periodo_academ, sigla, seccion)

    return vm.to_dict()


@router.get("/registro/asignatura/{sigla}/periodo/{cod_periodo_academ}/seccion/{seccion}/taller/{id_taller}/fecha/{fecha}/docente/{id_usuario}")
@template(template_file="registro/registro_taller.pt")
async def registro_taller_get_empty(request: Request, sigla: str, cod_periodo_academ: int, seccion: int, id_taller: int, fecha: str, id_usuario: int):
    vm = RegistroTallerViewModel(request)
    await vm.load_empty(sigla=sigla, cod_periodo_academ=cod_periodo_academ, seccion=seccion, id_taller=id_taller, fecha=fecha, id_usuario=id_usuario, obs="")
    return vm.to_dict()


@router.post("/registro/asignatura/{sigla}/periodo/{cod_periodo_academ}/seccion/{seccion}/taller/{id_taller}/fecha/{fecha}/docente/{id_usuario}")
@template(template_file="registro/registro_taller.pt")
async def registro_taller_asignatura_post(request: Request, sigla: str, cod_periodo_academ: int, seccion: int, id_taller: int, fecha: str, id_usuario: int):
    # Cargamos el view model el cual recupera los datos del formulario respectivo y realiza validaciones
    vm = RegistroTallerViewModel(request)
    await vm.register(sigla, cod_periodo_academ, seccion, id_taller, fecha, id_usuario)

    # Si hay errores, recarga el mismo formulario con los datos ingresados
    if vm.msg_error:
        return vm.to_dict()

    # Se carga el formulario con los datos
    await vm.load_empty(sigla=sigla, cod_periodo_academ=cod_periodo_academ, seccion=seccion, id_taller=id_taller, fecha=fecha, id_usuario=id_usuario, obs=vm.obs)

    # Se retorna el diccionario entregado por el redirect hacia la página principal
    return vm.to_dict()


import fastapi
from typing import Optional
from fastapi_chameleon import template
from starlette.requests import Request
from starlette import status
from services import programacion_service

from viewmodels.programacion.programaciones_asignatura_viewmodel import ProgramacionesAsignaturaViewModel
from viewmodels.programacion.programacion_asignatura_viewmodel import ProgramacionAsignaturaViewModel
from viewmodels.programacion.programaciones_taller_viewmodel import ProgramacionesTallerViewModel
from viewmodels.programacion.programacion_taller_viewmodel import ProgramacionTallerViewModel

router = fastapi.APIRouter()


@router.get("/programacion/asignatura/lista")
@template(template_file="programacion/programacion_asignatura_lista.pt")
async def programaciones_asignatura_lista(request: Request):
    vm = ProgramacionesAsignaturaViewModel(request)
    await vm.load()

    return vm.to_dict()


@router.get("/programacion/eliminar/ano_academ/{ano_academ}/periodo/{cod_periodo_academ}/sigla/{sigla}/seccion/{seccion}")
@template(template_file="programacion/programacion_asignatura_lista.pt")
async def eliminar_asignatura(request: Request, ano_academ: int, cod_periodo_academ: int, sigla: str, seccion: int):
    eliminacion = await programacion_service.delete_programacion_asignatura(request, ano_academ, cod_periodo_academ, sigla, seccion)

    if not eliminacion["eliminado"]:
        vm = ProgramacionesAsignaturaViewModel(request)
        await vm.load()
        vm.msg_error = eliminacion["msg_error"]
        return vm.to_dict()

    # Si no hay errores, se redirecciona a la página principal
    response = fastapi.responses.RedirectResponse("/programacion/asignatura/lista", status_code=status.HTTP_302_FOUND)
    return response


@router.get("/programacion/asignatura/periodo/seccion")
@template(template_file="programacion/programacion_asignatura.pt")
async def programacion_asignatura_get_empty(request: Request):
    vm = ProgramacionAsignaturaViewModel(request)
    await vm.load_empty()
    return vm.to_dict()


@router.post("/programacion/asignatura/periodo/seccion")
@template(template_file="programacion/programacion_asignatura.pt")
async def programacion_asignatura_post(request: Request):
    # Cargamos el view model el cual recupera los datos del formulario respectivo y realiza validaciones
    vm = ProgramacionAsignaturaViewModel(request)
    await vm.insert()

    # Si hay errores, recarga el mismo formulario con los datos ingresados
    if vm.msg_error:
        return vm.to_dict()

    # Se carga el formulario con los datos
    await vm.load(ano_academ=vm.ano_academ, cod_periodo_academ=vm.cod_periodo_academ, sigla=vm.sigla, seccion=vm.seccion)

    # Se retorna el diccionario entregado por el redirect hacia la página principal
    return vm.to_dict()


@router.get("/programacion/asignatura/{sigla}/periodo/{cod_periodo_academ}/seccion/{seccion}/lista")
@template(template_file="programacion/programacion_taller_lista.pt")
async def programaciones_taller_lista(request: Request, sigla: str, cod_periodo_academ: int, seccion: int):
    vm = ProgramacionesTallerViewModel(request)
    await vm.load(cod_periodo_academ, sigla, seccion)

    return vm.to_dict()


@router.get("/programacion/asignatura/{sigla}/periodo/{cod_periodo_academ}/seccion/{seccion}/taller/{id_taller}/fecha/{fecha}")
@template(template_file="programacion/programacion_taller.pt")
async def programacion_taller(request: Request, sigla: str, cod_periodo_academ: int, seccion: int, id_taller: int, fecha: str):
    vm = ProgramacionTallerViewModel(request)
    await vm.load(sigla=sigla, cod_periodo_academ=cod_periodo_academ, seccion=seccion, id_taller=id_taller, fecha=fecha)

    return vm.to_dict()


@router.get("/programacion/eliminar/ano_academ/{ano_academ}/periodo/{cod_periodo_academ}/sigla/{sigla}/seccion/{seccion}/taller/{id_taller}/fecha/{fecha}")
@template(template_file="programacion/programacion_taller_lista.pt")
async def eliminar_taller(request: Request, ano_academ: int, cod_periodo_academ: int, sigla: str, seccion: int, id_taller: int, fecha: str):
    eliminacion = await programacion_service.delete_programacion_taller(request, ano_academ, cod_periodo_academ, sigla, seccion, id_taller, fecha)

    if not eliminacion["eliminado"]:
        vm = ProgramacionesTallerViewModel(request)
        await vm.load(sigla=sigla, cod_periodo_academ=cod_periodo_academ, seccion=seccion)
        vm.msg_error = eliminacion["msg_error"]
        return vm.to_dict()

    # Si no hay errores, se redirecciona a la página principal
    response = fastapi.responses.RedirectResponse(f"/programacion/asignatura/{sigla}/periodo/{cod_periodo_academ}/seccion/{seccion}/lista", status_code=status.HTTP_302_FOUND)
    return response


@router.get("/programacion/asignatura/{sigla}/periodo/{cod_periodo_academ}/seccion/{seccion}")
@template(template_file="programacion/programacion_taller.pt")
async def producto_taller_get_empty(request: Request, sigla: str, cod_periodo_academ: int, seccion: int):
    vm = ProgramacionTallerViewModel(request)
    await vm.load_empty(sigla=sigla, cod_periodo_academ=cod_periodo_academ, seccion=seccion)

    return vm.to_dict()


@router.post("/programacion/asignatura/{sigla}/periodo/{cod_periodo_academ}/seccion/{seccion}/taller/{id_taller}/fecha/{fecha}")
@template(template_file="programacion/programacion_taller.pt")
async def programacion_taller_put(request: Request, sigla: str, cod_periodo_academ: int, seccion: int, id_taller: int, fecha: str):
    # Cargamos el view model el cual recupera los datos del formulario respectivo y realiza validaciones
    vm = ProgramacionTallerViewModel(request)
    await vm.update(sigla, cod_periodo_academ, seccion, id_taller, fecha)

    # Si hay errores, recarga el mismo formulario con los datos ingresados
    if vm.msg_error:
        return vm.to_dict()

    # Se carga el formulario con los datos
    await vm.load(sigla=sigla, cod_periodo_academ=cod_periodo_academ, seccion=seccion, id_taller=id_taller, fecha=fecha)

    # Se retorna el diccionario entregado por el redirect hacia la página principal
    return vm.to_dict()


@router.post("/programacion/asignatura/{sigla}/periodo/{cod_periodo_academ}/seccion/{seccion}/taller/fecha")
@template(template_file="programacion/programacion_taller.pt")
async def programacion_taller_post(request: Request, sigla: str, cod_periodo_academ: int, seccion: int):
    # Cargamos el view model el cual recupera los datos del formulario respectivo y realiza validaciones
    vm = ProgramacionTallerViewModel(request)
    await vm.insert(sigla, cod_periodo_academ, seccion)

    # Si hay errores, recarga el mismo formulario con los datos ingresados
    if vm.msg_error:
        return vm.to_dict()

    # Se carga el formulario con los datos
    await vm.load(sigla=sigla, cod_periodo_academ=cod_periodo_academ, seccion=seccion, id_taller=vm.id_taller, fecha=vm.fecha)

    # Se retorna el diccionario entregado por el redirect hacia la página principal
    return vm.to_dict()

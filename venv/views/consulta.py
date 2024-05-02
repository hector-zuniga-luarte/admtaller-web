
import fastapi
from fastapi_chameleon import template
from viewmodels.asignatura.asignaturas_viewmodel import AsignaturasViewModel
from viewmodels.asignatura.talleres_viewmodel import TalleresViewModel
from viewmodels.consulta.taller_viewmodel import ConsultaTallerViewModel
from starlette.requests import Request
from starlette.responses import Response

from infrastructure.fileexport import generar_excel

router = fastapi.APIRouter()


@router.get("/consulta/asignatura/lista")
@template(template_file="consulta/asignatura_lista.pt")
async def asignatura_lista(request: Request):
    vm = AsignaturasViewModel(request)
    await vm.load()

    return vm.to_dict()


@router.get("/consulta/asignatura/{sigla}/taller/lista")
@template(template_file="consulta/taller_lista.pt")
async def taller_lista(request: Request, sigla: str):
    vm = TalleresViewModel(request)
    await vm.load(sigla)

    return vm.to_dict()


@router.get("/consulta/asignatura/{sigla}/taller/{id_taller}")
@template(template_file="consulta/taller.pt")
async def taller(request: Request, sigla: str, id_taller: int):
    vm = ConsultaTallerViewModel(request)
    await vm.load(sigla=sigla, id_taller=id_taller)
    return vm.to_dict()


@router.get("/consulta/asignatura/lista/excel")
async def consulta_asignatura_lista_excel(request: Request):
    vm = AsignaturasViewModel(request)
    await vm.load()

    # Generar el archivo Excel
    excel_content = await generar_excel(vm.asignaturas)

    # Devolver el Excel como una respuesta
    filename = "Consulta asignaturas"
    return Response(content=excel_content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=" + filename + ".xlsx"})


@router.get("/consulta/asignatura/{sigla}/taller/lista/excel")
async def taller_lista_excel(request: Request, sigla: str):
    vm = TalleresViewModel(request)
    await vm.load(sigla)

    # Generar el archivo Excel
    excel_content = await generar_excel(vm.talleres)

    # Devolver el Excel como una respuesta
    filename = f"Consulta talleres {sigla}"
    return Response(content=excel_content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=" + filename + ".xlsx"})


@router.get("/consulta/asignatura/{sigla}/taller/{id_taller}/excel")
async def taller(request: Request, sigla: str, id_taller: int):
    vm = ConsultaTallerViewModel(request)
    await vm.load(sigla=sigla, id_taller=id_taller)

    # Generar el archivo Excel
    excel_content = await generar_excel(vm.productos)

    # Devolver el Excel como una respuesta
    filename = f"Consulta taller {sigla} semana {vm.semana}"
    return Response(content=excel_content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=" + filename + ".xlsx"})



import fastapi
from fastapi_chameleon import template
from viewmodels.asignatura.asignaturas_viewmodel import AsignaturasViewModel
from viewmodels.asignatura.talleres_viewmodel import TalleresViewModel
from viewmodels.consulta.taller_viewmodel import ConsultaTallerViewModel
from starlette.requests import Request

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

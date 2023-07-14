
import fastapi
from fastapi_chameleon import template
from viewmodels.param.params_viewmodel import ParamsViewModel
from viewmodels.param.param_viewmodel import ParamViewModel
from starlette.requests import Request

router = fastapi.APIRouter()


@router.get("/param/lista")
@template(template_file="param/param_lista.pt")
async def usuario_lista(request: Request):
    vm = ParamsViewModel(request)
    await vm.load()

    return vm.to_dict()


@router.get("/param/{cod_param}")
@template(template_file="param/param.pt")
async def usuario(request: Request, cod_param: int):
    vm = ParamViewModel(request)
    await vm.load(cod_param=cod_param)
    return vm.to_dict()


@router.post("/param/{cod_param}")
@template(template_file="param/param.pt")
async def usuario_put(request: Request, cod_param: int):
    # Cargamos el view model el cual recupera los datos del formulario respectivo y realiza validaciones
    vm = ParamViewModel(request)
    await vm.update()

    # Si hay errores, recarga el mismo formulario con los datos ingresados
    if vm.msg_error:
        return vm.to_dict()

    # Se carga el formulario con los datos
    await vm.load(cod_param=cod_param)

    # Se retorna el diccionario entregado por el redirect hacia la página principal
    return vm.to_dict()

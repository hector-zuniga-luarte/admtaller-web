
import fastapi
from fastapi_chameleon import template
from viewmodels.usuario.usuarios_viewmodel import UsuariosViewModel
from viewmodels.usuario.usuario_viewmodel import UsuarioViewModel
from starlette.requests import Request
from starlette import status
from services import usuario_service

router = fastapi.APIRouter()


@router.get("/usuario/lista")
@template(template_file="usuario/usuario_lista.pt")
async def usuario_lista(request: Request):
    vm = UsuariosViewModel(request)
    await vm.load()

    return vm.to_dict()


@router.get("/usuario/eliminar/{id_usuario}")
@template(template_file="usuario/usuario_lista.pt")
async def eliminar_usuario(request: Request, id_usuario: int):
    eliminacion = await usuario_service.delete_usuario(request, id_usuario)

    if not eliminacion["eliminado"]:
        vm = UsuariosViewModel(request)
        await vm.load()
        vm.msg_error = eliminacion["msg_error"]

        return vm.to_dict()

    # Si no hay errores, se redirecciona a la página principal
    response = fastapi.responses.RedirectResponse("/usuario/lista", status_code=status.HTTP_302_FOUND)
    return response


@router.get("/usuario")
@template(template_file="usuario/usuario.pt")
async def usuario_new(request: Request):
    vm = UsuarioViewModel(request)
    await vm.load_empty()
    return vm.to_dict()


@router.get("/usuario/{id_usuario}")
@template(template_file="usuario/usuario.pt")
async def usuario(request: Request, id_usuario: int):
    vm = UsuarioViewModel(request)
    await vm.load(id_usuario=id_usuario)
    return vm.to_dict()


@router.post("/usuario/{id_usuario}")
@template(template_file="usuario/usuario.pt")
async def usuario_put(request: Request, id_usuario: int):
    # Cargamos el view model el cual recupera los datos del formulario respectivo y realiza validaciones
    vm = UsuarioViewModel(request)
    await vm.update()

    # Si hay errores, recarga el mismo formulario con los datos ingresados
    if vm.msg_error:
        return vm.to_dict()

    # Se carga el formulario con los datos
    await vm.load(id_usuario=id_usuario)

    # Se retorna el diccionario entregado por el redirect hacia la página principal
    return vm.to_dict()


@router.post("/usuario")
@template(template_file="usuario/usuario.pt")
async def usuario_post(request: Request):
    # Cargamos el view model el cual recupera los datos del formulario respectivo y realiza validaciones
    vm = UsuarioViewModel(request)
    await vm.insert()

    # Si hay errores, recarga el mismo formulario con los datos ingresados
    if vm.msg_error:
        return vm.to_dict()

    # Se carga el formulario con los datos
    await vm.load(id_usuario=vm.id_usuario)

    # Se retorna el diccionario entregado por el redirect hacia la página principal
    return vm.to_dict()

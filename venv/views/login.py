
import fastapi
from fastapi_chameleon import template
from starlette.requests import Request
from starlette import status

from viewmodels.login.login_viewmodel import LoginViewModel
from viewmodels.login.password_viewmodel import PasswordViewModel
from infrastructure import cookie_autoriz

router = fastapi.APIRouter()


@router.get("/login")
@template(template_file="login/login.pt")
async def login_get(request: Request):
    vm = LoginViewModel(request)

    # Si hay errores, recarga el mismo formulario con los datos ingresados
    if vm.msg_error:
        return vm.to_dict()

    return vm.to_dict()


@router.post("/login")
@template(template_file="login/login.pt")
async def login_post(request: Request):
    # Cargamos el view model el cual recupera los datos del formulario respectivo y realiza validaciones
    vm = LoginViewModel(request)
    await vm.load()

    # Si hay errores, recarga el mismo formulario con los datos ingresados
    if vm.msg_error:
        return vm.to_dict()

    # Si no hay errores, se redirecciona a la página principal
    response = fastapi.responses.RedirectResponse("/principal", status_code=status.HTTP_302_FOUND)

    # Luego seteamos la cookie con los datos relevantes del usuario
    cookie_autoriz.set_autoriz_cookie(response, vm.id_usuario, vm.login, vm.cod_perfil, vm.ano_academ, vm.nom_carrera, vm.cod_carrera)
    # Se retorna el diccionario entregado por el redirect hacia la página principal
    return response


@router.get("/logout")
def logout(request: Request):
    response = fastapi.responses.RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    cookie_autoriz.logout(response)

    return response


@router.get("/password")
@template(template_file="login/password.pt")
async def password_get(request: Request):
    vm = PasswordViewModel(request)
    await vm.load()

    # Si hay errores, recarga el mismo formulario con los datos ingresados
    if vm.msg_error:
        return vm.to_dict()

    return vm.to_dict()


@router.post("/password")
@template(template_file="login/password.pt")
async def password_put(request: Request):
    # Cargamos el view model el cual recupera los datos del formulario respectivo y realiza validaciones
    vm = PasswordViewModel(request)
    await vm.update()

    return vm.to_dict()

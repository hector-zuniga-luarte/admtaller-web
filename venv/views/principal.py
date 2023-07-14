
import fastapi
from fastapi_chameleon import template
from viewmodels.principal.principal_viewmodel import PrincipalViewModel
from starlette.requests import Request

router = fastapi.APIRouter()


@router.get("/principal")
@template()
async def principal(request: Request):
    vm = PrincipalViewModel(request)
    await vm.load()

    return vm.to_dict()

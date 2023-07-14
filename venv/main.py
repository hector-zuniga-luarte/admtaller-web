
import fastapi
import fastapi_chameleon
from starlette.staticfiles import StaticFiles

from views import index
from views import login
from views import principal
from views import usuario
from views import param
from views import asignatura
from views import programacion
from views import producto
from views import registro
from views import consulta
from views import reporte

app = fastapi.FastAPI()


# Método de configuración de routers
def configura_routers():
    # Cargamos la ruta de los archivos estáticos
    app.mount("/static", StaticFiles(directory="static"), name="static")
    # Cargamos los routers
    app.include_router(index.router)
    app.include_router(login.router)
    app.include_router(principal.router)
    app.include_router(usuario.router)
    app.include_router(param.router)
    app.include_router(asignatura.router)
    app.include_router(programacion.router)
    app.include_router(producto.router)
    app.include_router(registro.router)
    app.include_router(consulta.router)
    app.include_router(reporte.router)


# Método de configuración de templates
def configura_templates():
    fastapi_chameleon.global_init("templates")


# Método de configuración general, que llama a los otros sub-métodos de configuración
def configura():
    configura_routers()
    configura_templates()


# Se configura la aplicación previo a su despliegue
configura()

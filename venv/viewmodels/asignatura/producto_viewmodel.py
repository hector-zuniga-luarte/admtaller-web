
from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import asignatura_service
from services import taller_service
from services import producto_service
from infrastructure.constants import Mensajes


class ProductoTallerViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.id_producto: int
        self.cantidad: int
        self.cod_agrupador: str
        self.sigla: str
        self.nom_asignatura: str
        self.semana: int
        self.titulo_preparacion: str
        self.id_taller: int
        self.nom_producto: int
        self.nom_agrupador: str
        self.nom_unidad_medida: str
        self.precio: int

        self.producto: dict
        self.taller: dict
        self.lista_productos: List[dict]
        self.lista_agrupadores: List[dict]

    async def validate(self) -> bool:
        result: bool = True

        return result

    # Función que permite visualizar un formulario para registros nuevos en el sistema
    async def load_empty(self, sigla, id_taller):
        K_NUEVOREGISTRO: int = 0
        if self.esta_conectado:
            self.sigla = sigla
            self.id_taller = id_taller
            self.id_producto = K_NUEVOREGISTRO
            self.cod_agrupador = K_NUEVOREGISTRO
            self.nom_asignatura = await asignatura_service.get_nom_asignatura(sigla, self.id_usuario_conectado)
            taller = await taller_service.get_taller(self.request, self.id_taller)
            self.semana = taller["semana"]
            self.titulo_preparacion = taller["titulo_preparacion"]
            self.producto = await taller_service.get_producto_taller(id_taller, K_NUEVOREGISTRO, K_NUEVOREGISTRO)
            self.nom_producto = self.producto["nom_producto"]
            self.nom_agrupador = self.producto["nom_agrupador"]
            self.nom_unidad_medida = self.producto["nom_unidad_medida"]
            self.cantidad = self.producto["cantidad"]
            self.precio = self.producto["precio"]
            self.lista_productos = await producto_service.get_lista_productos(self.id_usuario_conectado)
            self.lista_agrupadores = await taller_service.get_lista_agrupadores()
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

    # Función que carga datos y verifica si está conectado al sistema
    async def update(self):
        # Recuperamos los datos desde el formulario
        form = await self.request.form()
        self.sigla = form.get("sigla", "").strip()
        self.id_taller = int(form.get("id-taller", "").strip())
        self.id_producto = int(form.get("id-producto", "").strip())
        self.cod_agrupador = int(form.get("cod-agrupador", "").strip())
        self.cantidad = float(form.get("cantidad", "").strip())

        self.producto = {
            "sigla": self.sigla,
            "id_taller": self.id_taller,
            "id_producto": self.id_producto,
            "cod_agrupador": self.cod_agrupador,
            "cantidad": self.cantidad,
        }

        if await self.validate():
            self.producto = await taller_service.update_producto_taller(self.request, self.producto)

            if not self.producto:
                self.msg_error = "Error al modificar los datos del producto del taller respectivo"
            else:
                self.msg_exito = "Se ha modificado correctamente el producto del taller respectivo"

    # Función que carga datos y verifica si está conectado al sistema
    async def insert(self):
        # Recuperamos los datos desde el formulario
        # Recuperamos los datos desde el formulario
        form = await self.request.form()
        self.sigla = form.get("sigla", "").strip()
        self.id_taller = int(form.get("id-taller", "").strip())
        self.id_producto = int(form.get("id-producto", "").strip())
        self.cod_agrupador = int(form.get("cod-agrupador", "").strip())
        self.cantidad = float(form.get("cantidad", "").strip())

        self.producto = {
            "sigla": self.sigla,
            "id_taller": self.id_taller,
            "id_producto": self.id_producto,
            "cod_agrupador": self.cod_agrupador,
            "cantidad": self.cantidad,
        }

        if await self.validate():
            self.producto = await taller_service.insert_producto_taller(self.producto)

            if not self.producto:
                self.msg_error = "Error al ingresar los datos del producto del taller respectivo"
            else:
                self.msg_exito = "Se ha ingresado correctamente el producto del taller respectivo"

    async def load(self, sigla, id_taller, id_producto, cod_agrupador):
        if self.esta_conectado:
            self.sigla = sigla
            self.id_taller = id_taller
            self.id_producto = id_producto
            self.cod_agrupador = cod_agrupador
            self.nom_asignatura = await asignatura_service.get_nom_asignatura(sigla, self.id_usuario_conectado)
            taller = await taller_service.get_taller(self.request, self.id_taller)
            self.semana = taller["semana"]
            self.titulo_preparacion = taller["titulo_preparacion"]
            self.producto = await taller_service.get_producto_taller(id_taller, id_producto, cod_agrupador)
            self.nom_producto = self.producto["nom_producto"]
            self.nom_agrupador = self.producto["nom_agrupador"]
            self.cantidad = self.producto["cantidad"]
            self.precio = self.producto["precio"]
            self.nom_unidad_medida = self.producto["nom_unidad_medida"]
            self.lista_productos = await producto_service.get_lista_productos(self.id_usuario_conectado)
            self.lista_agrupadores = await taller_service.get_lista_agrupadores()
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

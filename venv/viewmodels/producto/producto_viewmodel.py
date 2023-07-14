
from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import param_service
from services import producto_service
from infrastructure.constants import Mensajes


class ProductoViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.id_producto: int
        self.nom_producto: int
        self.precio: int
        self.cod_unidad_medida: int
        self.cod_categ_producto: int

        self.producto: dict
        self.lista_unidad_medida: List[dict]
        self.lista_categoria_producto: List[dict]

    async def validate(self) -> bool:
        result: bool = True

        # Verificar que se ingrese el nombre del producto
        if len(self.producto["nom_producto"].strip()) == 0:
            self.msg_error = "Debe ingresar el nombre del producto"
            result = False

        # Verificar que se ingrese un precio al producto
        if self.producto["precio"] <= 0:
            self.msg_error = "Debe ingresar un precio al producto"
            result = False

        # Verificar que se ingrese una unidad de medida
        if self.producto["cod_unidad_medida"] == 0:
            self.msg_error = "Debe ingresar una unidad de medida al producto"
            result = False

        return result

    # Función que permite visualizar un formulario para registros nuevos en el sistema
    async def load_empty(self):
        K_NUEVO: int = 0
        if self.esta_conectado:
            self.producto = await producto_service.get_producto(self.request, K_NUEVO)
            self.lista_unidad_medida = await param_service.get_unidad_medida_lista(self.request)
            self.lista_categoria_producto = await param_service.get_categoria_producto_lista(self.request)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

    # Función que carga datos y verifica si está conectado al sistema
    async def update(self):
        # Recuperamos los datos desde el formulario
        form = await self.request.form()
        self.id_producto = int(form.get("id-producto", "").strip())
        self.nom_producto = form.get("nom-producto", "")
        self.precio = int(form.get("precio", "").lower().strip())
        self.cod_unidad_medida = form.get("cod-unidad-medida", "").strip()
        self.cod_categ_producto = form.get("cod-categ-producto", "").strip()

        self.producto = {
            "id_producto": self.id_producto,
            "nom_producto": self.nom_producto,
            "precio": self.precio,
            "cod_unidad_medida": self.cod_unidad_medida,
            "cod_categ_producto": self.cod_categ_producto,
        }
        self.lista_unidad_medida = await param_service.get_unidad_medida_lista(self.request)
        self.lista_categoria_producto = await param_service.get_categoria_producto_lista(self.request)

        if await self.validate():
            self.producto = await producto_service.update_producto(self.request, self.producto)

            if not self.producto:
                self.msg_error = "Error al modificar el producto"
            else:
                self.msg_exito = "Se ha modificado correctamente el producto"

    # Función que carga datos y verifica si está conectado al sistema
    async def insert(self):
        # Recuperamos los datos desde el formulario
        form = await self.request.form()
        self.id_producto = int(form.get("id-producto", "").strip())
        self.nom_producto = form.get("nom-producto", "")
        self.precio = int(form.get("precio", "").lower().strip())
        self.cod_unidad_medida = form.get("cod-unidad-medida", "").strip()
        self.cod_categ_producto = form.get("cod-categ-producto", "").strip()

        self.producto = {
            "id_producto": 0,
            "nom_producto": self.nom_producto,
            "precio": self.precio,
            "cod_unidad_medida": self.cod_unidad_medida,
            "cod_categ_producto": self.cod_categ_producto,
        }
        self.lista_unidad_medida = await param_service.get_unidad_medida_lista(self.request)
        self.lista_categoria_producto = await param_service.get_categoria_producto_lista(self.request)

        if await self.validate():
            self.usuario = await producto_service.insert_producto(self.producto)

            if not self.usuario:
                self.msg_error = "Error al agregar el producto"
            else:
                self.id_producto = self.usuario["id_producto"]
                self.msg_exito = "Se ha agregado correctamente el producto"

    async def load(self, id_producto):
        if self.esta_conectado:
            self.producto = await producto_service.get_producto(self.request, id_producto)
            self.lista_unidad_medida = await param_service.get_unidad_medida_lista(self.request)
            self.lista_categoria_producto = await param_service.get_categoria_producto_lista(self.request)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

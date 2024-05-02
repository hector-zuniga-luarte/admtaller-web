
from typing import List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import asignatura_service
from infrastructure.constants import Mensajes


class TalleresViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.sigla: str = None
        self.nom_asignatura: str = None
        self.talleres: List[dict] = []
        self.total: int

    # Función que carga datos y verifica si está conectado al sistema
    async def load(self, sigla):
        if self.esta_conectado:
            self.sigla = sigla
            self.nom_asignatura = await asignatura_service.get_nom_asignatura(self.sigla, self.id_usuario_conectado)
            self.talleres = await asignatura_service.get_talleres_lista(self.sigla, self.id_usuario_conectado)
            self.total = 0

            # Anulamos lo que no están configurados para que no tengan problemas con el costo_total None de los talleres que aún no han sido configurados
            self.talleres = [{**d, "costo_total": 0} if d.get("costo_total") is None else d for d in self.talleres]

            # Si la columna de costo viene en la lista de talleres (al menos en el primer elemento) podemos sumar el total
            if self.talleres and "costo_total" in self.talleres[0]:
                self.total = sum(t["costo_total"] for t in self.talleres if t["costo_total"] is not None)
        else:
            self.msg_error = Mensajes.ERR_NO_AUTENTICADO.value

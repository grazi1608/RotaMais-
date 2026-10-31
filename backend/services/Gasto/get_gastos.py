from repositories import GastoRepository
from utils.datas import para_datetime


class ListarGastosDoMotorista:
    """Caso de uso: listar os gastos de um motorista, do mais recente para o mais antigo."""

    def __init__(self):
        self.repositorio = GastoRepository()

    def executar(self, motorista_id):
        gastos = self.repositorio.listar_por_motorista(motorista_id)

        for gasto in gastos:
            data = para_datetime(gasto["data"])
            gasto["data"] = data.strftime("%Y-%m-%dT%H:%M:%S") if data else None

        return gastos

from models.veiculo import Veiculo
from services.excecoes import RecursoNaoEncontrado


class BuscarVeiculo:
    """Caso de uso: buscar um veículo pelo id."""

    def executar(self, id):
        veiculo = Veiculo.buscar_por_id(id)

        if veiculo is None:
            raise RecursoNaoEncontrado("Veículo não encontrado.")

        return veiculo.to_dict()

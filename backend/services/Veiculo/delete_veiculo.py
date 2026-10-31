from models.veiculo import Veiculo
from services.excecoes import RecursoNaoEncontrado


class ExcluirVeiculo:
    """Caso de uso: excluir um veículo existente (as corridas dele saem junto;
    os gastos ficam sem veículo)."""

    def executar(self, id):
        veiculo = Veiculo.buscar_por_id(id)

        if veiculo is None:
            raise RecursoNaoEncontrado("Veículo não encontrado.")

        veiculo.deletar()

        return {"mensagem": "Veículo excluído com sucesso."}

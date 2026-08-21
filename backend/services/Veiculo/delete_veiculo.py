from models.veiculo import Veiculo


class ExcluirVeiculo:
    """Caso de uso: excluir um veículo existente."""

    def executar(self, id):
        veiculo = Veiculo.buscar_por_id(id)

        if veiculo is None:
            raise ValueError("Veículo não encontrado.")

        veiculo.deletar()

        return {"mensagem": "Veículo excluído com sucesso."}

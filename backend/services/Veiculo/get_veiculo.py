from models.veiculo import Veiculo


class BuscarVeiculo:
    """Caso de uso: buscar um veículo pelo id."""

    def executar(self, id):
        veiculo = Veiculo.buscar_por_id(id)

        if veiculo is None:
            raise ValueError("Veículo não encontrado.")

        return veiculo.to_dict()

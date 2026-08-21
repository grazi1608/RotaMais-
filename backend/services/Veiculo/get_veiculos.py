from models.veiculo import Veiculo


class ListarVeiculos:
    """Caso de uso: listar todos os veículos cadastrados."""

    def executar(self):
        veiculos = Veiculo.listar_todos()
        return [veiculo.to_dict() for veiculo in veiculos]

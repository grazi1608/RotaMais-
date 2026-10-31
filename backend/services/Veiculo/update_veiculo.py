from models.veiculo import Veiculo
from models.motorista import Motorista
from repositories import VeiculoRepository
from services.excecoes import RecursoNaoEncontrado
from services.validacoes import exigir_texto, exigir_numero_positivo


class AtualizarVeiculo:
    """Caso de uso: atualizar os dados de um veículo existente."""

    def __init__(self):
        self.repositorio = VeiculoRepository()

    def executar(self, id, placa, modelo, consumo_por_km, motorista_id):
        veiculo = Veiculo.buscar_por_id(id)
        if veiculo is None:
            raise RecursoNaoEncontrado("Veículo não encontrado.")

        placa = exigir_texto(placa, "Informe a placa.").upper()
        modelo = exigir_texto(modelo, "Informe o modelo.")
        consumo_por_km = exigir_numero_positivo(consumo_por_km, "O custo por km deve ser maior que zero.")

        id_placa = self.repositorio.buscar_id_por_placa(placa)
        if id_placa and id_placa != id:
            raise ValueError("Já existe um veículo com essa placa.")

        if Motorista.buscar_por_id(motorista_id) is None:
            raise ValueError("Motorista não encontrado.")

        veiculo.placa = placa
        veiculo.modelo = modelo
        veiculo.consumo_por_km = consumo_por_km
        veiculo.motorista_id = motorista_id

        return veiculo.atualizar()

from models.veiculo import Veiculo
from models.motorista import Motorista
from repositories import VeiculoRepository
from services.validacoes import exigir_texto, exigir_numero_positivo


class CriarVeiculo:
    """Caso de uso: cadastrar um novo veículo."""

    def __init__(self):
        self.repositorio = VeiculoRepository()

    def executar(self, placa, modelo, consumo_por_km, motorista_id):
        placa = exigir_texto(placa, "Informe a placa.").upper()
        modelo = exigir_texto(modelo, "Informe o modelo.")
        consumo_por_km = exigir_numero_positivo(consumo_por_km, "O custo por km deve ser maior que zero.")

        if self.repositorio.buscar_id_por_placa(placa):
            raise ValueError("Já existe um veículo com essa placa.")

        if Motorista.buscar_por_id(motorista_id) is None:
            raise ValueError("Motorista não encontrado.")

        novo_veiculo = Veiculo(
            placa=placa,
            modelo=modelo,
            consumo_por_km=consumo_por_km,
            motorista_id=motorista_id
        )

        return novo_veiculo.salvar()

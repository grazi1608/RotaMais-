from models.veiculo import Veiculo
from models.motorista import Motorista


class CriarVeiculo:
    """Caso de uso: cadastrar um novo veículo."""

    def executar(self, placa, modelo, consumo_por_km, motorista_id):
        if Veiculo.query.filter_by(placa=placa).first():
            raise ValueError("Já existe um veículo com essa placa.")

        motorista = Motorista.buscar_por_id(motorista_id)
        if motorista is None:
            raise ValueError("Motorista não encontrado.")

        novo_veiculo = Veiculo(
            placa=placa,
            modelo=modelo,
            consumo_por_km=consumo_por_km,
            motorista_id=motorista_id
        )

        return novo_veiculo.salvar()

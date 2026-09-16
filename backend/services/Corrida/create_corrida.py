from models.corrida import Corrida
from models.motorista import Motorista
from models.veiculo import Veiculo


class CriarCorrida:
    """Caso de uso: registrar uma nova corrida, calculando custo e lucro."""

    def executar(self, valor, distancia, motorista_id, veiculo_id):
        motorista = Motorista.buscar_por_id(motorista_id)
        if motorista is None:
            raise ValueError("Motorista não encontrado.")

        veiculo = Veiculo.buscar_por_id(veiculo_id)
        if veiculo is None:
            raise ValueError("Veículo não encontrado.")

        custo_estimado = distancia * veiculo.consumo_por_km
        lucro = valor - custo_estimado

        corrida = Corrida(
            valor=valor,
            custo_estimado=custo_estimado,
            lucro=lucro,
            distancia=distancia,
            motorista_id=motorista_id,
            veiculo_id=veiculo_id
        )

        return corrida.salvar()

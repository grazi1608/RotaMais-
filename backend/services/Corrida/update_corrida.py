from models.corrida import Corrida
from models.motorista import Motorista
from models.veiculo import Veiculo


class AtualizarCorrida:
    """Caso de uso: atualizar uma corrida existente, recalculando custo e lucro."""

    def executar(self, id, valor, distancia, motorista_id, veiculo_id, data_hora=None):
        corrida = Corrida.buscar_por_id(id)
        if corrida is None:
            raise ValueError("Corrida não encontrada.")

        motorista = Motorista.buscar_por_id(motorista_id)
        if motorista is None:
            raise ValueError("Motorista não encontrado.")

        veiculo = Veiculo.buscar_por_id(veiculo_id)
        if veiculo is None:
            raise ValueError("Veículo não encontrado.")

        custo_estimado = distancia * veiculo.consumo_por_km
        lucro = valor - custo_estimado

        corrida.valor = valor
        corrida.distancia = distancia
        corrida.custo_estimado = custo_estimado
        corrida.lucro = lucro
        corrida.motorista_id = motorista_id
        corrida.veiculo_id = veiculo_id

        if data_hora is not None:
            corrida.data_hora = data_hora

        return corrida.atualizar()

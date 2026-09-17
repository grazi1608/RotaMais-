from datetime import datetime
from models.gasto import Gasto
from models.veiculo import Veiculo


class CriarGasto:
    """Caso de uso: registrar um novo gasto (combustível, manutenção, etc.)."""

    def executar(self, tipo, valor, motorista_id, descricao=None, veiculo_id=None, data=None):
        if tipo not in Gasto.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de gasto inválido. Use um de: {', '.join(Gasto.TIPOS_VALIDOS)}.")

        if valor is None or valor <= 0:
            raise ValueError("O valor do gasto deve ser maior que zero.")

        if veiculo_id is not None and Veiculo.buscar_por_id(veiculo_id) is None:
            raise ValueError("Veículo não encontrado.")

        gasto = Gasto(
            tipo=tipo,
            valor=valor,
            motorista_id=motorista_id,
            descricao=descricao,
            veiculo_id=veiculo_id,
            data=data,
        )

        return gasto.salvar()

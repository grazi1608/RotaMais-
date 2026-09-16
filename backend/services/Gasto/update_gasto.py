from models.gasto import Gasto
from .get_gasto import BuscarGasto


class AtualizarGasto:
    """Caso de uso: atualizar um gasto existente do motorista logado."""

    def executar(self, id, motorista_id, tipo, valor, descricao=None, veiculo_id=None, data=None):
        gasto = BuscarGasto().executar(id, motorista_id)

        if tipo not in Gasto.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de gasto inválido. Use um de: {', '.join(Gasto.TIPOS_VALIDOS)}.")

        if valor is None or valor <= 0:
            raise ValueError("O valor do gasto deve ser maior que zero.")

        gasto.tipo = tipo
        gasto.valor = valor
        gasto.descricao = descricao
        gasto.veiculo_id = veiculo_id

        if data is not None:
            gasto.data = data

        return gasto.atualizar()

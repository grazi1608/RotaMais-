from models.gasto import Gasto
from models.veiculo import Veiculo
from services.validacoes import exigir_numero_positivo
from .get_gasto import BuscarGasto


class AtualizarGasto:
    """Caso de uso: atualizar um gasto existente do motorista logado."""

    def executar(self, id, motorista_id, tipo, valor, descricao=None, veiculo_id=None, data=None):
        gasto = BuscarGasto().executar(id, motorista_id)

        if tipo not in Gasto.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de gasto inválido. Use um de: {', '.join(Gasto.TIPOS_VALIDOS)}.")

        valor = exigir_numero_positivo(valor, "O valor do gasto deve ser maior que zero.")

        if veiculo_id is not None and Veiculo.buscar_por_id(veiculo_id) is None:
            raise ValueError("Veículo não encontrado.")

        gasto.tipo = tipo
        gasto.valor = valor
        gasto.descricao = (descricao or "").strip() or None
        gasto.veiculo_id = veiculo_id

        if data is not None:
            gasto.data = data

        return gasto.atualizar()

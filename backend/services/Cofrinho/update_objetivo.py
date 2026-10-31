from services.validacoes import exigir_texto, exigir_numero_positivo
from .get_objetivo import BuscarObjetivoCofrinho


class AtualizarObjetivoCofrinho:
    """Caso de uso: atualizar nome/meta de um objetivo existente."""

    def executar(self, id, motorista_id, nome, valor_meta):
        objetivo = BuscarObjetivoCofrinho().executar(id, motorista_id)

        objetivo.nome = exigir_texto(nome, "Informe um nome para o objetivo.")
        objetivo.valor_meta = exigir_numero_positivo(valor_meta, "O valor da meta deve ser maior que zero.")

        return objetivo.atualizar()

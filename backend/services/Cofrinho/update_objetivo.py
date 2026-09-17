from .get_objetivo import BuscarObjetivoCofrinho


class AtualizarObjetivoCofrinho:
    """Caso de uso: atualizar nome/meta de um objetivo existente."""

    def executar(self, id, motorista_id, nome, valor_meta):
        objetivo = BuscarObjetivoCofrinho().executar(id, motorista_id)

        if valor_meta is None or valor_meta <= 0:
            raise ValueError("O valor da meta deve ser maior que zero.")

        objetivo.nome = nome
        objetivo.valor_meta = valor_meta

        return objetivo.atualizar()

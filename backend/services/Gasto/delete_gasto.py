from .get_gasto import BuscarGasto


class ExcluirGasto:
    """Caso de uso: excluir um gasto do motorista logado."""

    def executar(self, id, motorista_id):
        gasto = BuscarGasto().executar(id, motorista_id)
        gasto.deletar()
        return {"mensagem": "Gasto excluído com sucesso."}

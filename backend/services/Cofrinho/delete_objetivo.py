from .get_objetivo import BuscarObjetivoCofrinho


class ExcluirObjetivoCofrinho:
    """Caso de uso: excluir um objetivo do cofrinho."""

    def executar(self, id, motorista_id):
        objetivo = BuscarObjetivoCofrinho().executar(id, motorista_id)
        objetivo.deletar()
        return {"mensagem": "Objetivo excluído com sucesso."}

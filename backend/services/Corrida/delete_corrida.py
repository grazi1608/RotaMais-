from models.corrida import Corrida
from services.excecoes import RecursoNaoEncontrado


class ExcluirCorrida:
    """Caso de uso: excluir uma corrida existente."""

    def executar(self, id):
        corrida = Corrida.buscar_por_id(id)

        if corrida is None:
            raise RecursoNaoEncontrado("Corrida não encontrada.")

        corrida.deletar()

        return {"mensagem": "Corrida excluída com sucesso."}

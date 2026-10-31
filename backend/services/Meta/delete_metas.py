from models.meta import Meta
from services.excecoes import RecursoNaoEncontrado


class ExcluirMeta:
    """Caso de uso: excluir uma meta existente."""

    def executar(self, id):
        meta = Meta.buscar_por_id(id)
        if meta is None:
            raise RecursoNaoEncontrado("Meta não encontrada.")

        meta.deletar()

        return {"mensagem": "Meta excluída com sucesso."}

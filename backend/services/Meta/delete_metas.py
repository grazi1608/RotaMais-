from models.meta import Meta


class ExcluirMeta:
    """Caso de uso: excluir uma meta existente."""

    def executar(self, id):
        meta = Meta.buscar_por_id(id)
        if meta is None:
            raise ValueError("Meta não encontrada.")

        meta.deletar()

        return {"mensagem": "Meta excluída com sucesso."}

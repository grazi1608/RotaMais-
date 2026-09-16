from models.meta import Meta


class ListarMetas:
    """Caso de uso: listar todas as metas cadastradas."""

    def executar(self):
        return Meta.listar_todos()

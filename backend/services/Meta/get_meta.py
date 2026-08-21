from models.meta import Meta


class BuscarMeta:
    """Caso de uso: buscar uma meta pelo id."""

    def executar(self, id):
        meta = Meta.buscar_por_id(id)

        if meta is None:
            raise ValueError("Meta não encontrada.")

        return meta

from models.meta import Meta


class AtualizarMeta:
    """Caso de uso: atualizar uma meta existente."""

    def executar(self, id, valor_meta=None, data_inicio=None, data_fim=None, concluida=None, motorista_id=None):
        meta = Meta.buscar_por_id(id)
        if meta is None:
            raise ValueError("Meta não encontrada.")

        if valor_meta is not None:
            meta.valor_meta = valor_meta
        if data_inicio is not None:
            meta.data_inicio = data_inicio
        if data_fim is not None:
            meta.data_fim = data_fim
        if concluida is not None:
            meta.concluida = concluida
        if motorista_id is not None:
            meta.motorista_id = motorista_id

        return meta.atualizar()

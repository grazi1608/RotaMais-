from models.meta import Meta


class CriarMeta:
    """Caso de uso: cadastrar uma nova meta financeira para um motorista."""

    def executar(self, valor_meta, data_fim, motorista_id, data_inicio=None, concluida=False):
        nova_meta = Meta(
            valor_meta=valor_meta,
            data_fim=data_fim,
            motorista_id=motorista_id,
            data_inicio=data_inicio,
            concluida=concluida
        )

        return nova_meta.salvar()

from models.objetivo_cofrinho import ObjetivoCofrinho


class CriarObjetivoCofrinho:
    """Caso de uso: criar um novo objetivo de economia no cofrinho."""

    def executar(self, nome, valor_meta, motorista_id):
        if not nome:
            raise ValueError("Informe um nome para o objetivo.")

        if valor_meta is None or valor_meta <= 0:
            raise ValueError("O valor da meta deve ser maior que zero.")

        objetivo = ObjetivoCofrinho(
            nome=nome,
            valor_meta=valor_meta,
            motorista_id=motorista_id,
        )

        return objetivo.salvar()

from datetime import date

from models.meta import Meta
from models.motorista import Motorista
from services.validacoes import exigir_numero_positivo


class CriarMeta:
    """Caso de uso: cadastrar uma nova meta financeira para um motorista."""

    def executar(self, valor_meta, data_fim, motorista_id, data_inicio=None, concluida=False):
        valor_meta = exigir_numero_positivo(valor_meta, "O valor da meta deve ser maior que zero.")

        if data_fim is None:
            raise ValueError("Informe a data final da meta.")

        data_inicio = data_inicio or date.today()
        if data_fim < data_inicio:
            raise ValueError("A data final não pode ser anterior à data de início.")

        if Motorista.buscar_por_id(motorista_id) is None:
            raise ValueError("Motorista não encontrado.")

        nova_meta = Meta(
            valor_meta=valor_meta,
            data_fim=data_fim,
            motorista_id=motorista_id,
            data_inicio=data_inicio,
            concluida=bool(concluida)
        )

        return nova_meta.salvar()

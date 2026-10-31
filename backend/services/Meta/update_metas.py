from models.meta import Meta
from models.motorista import Motorista
from services.excecoes import RecursoNaoEncontrado
from services.validacoes import exigir_numero_positivo


class AtualizarMeta:
    """Caso de uso: atualizar uma meta existente (só os campos informados)."""

    def executar(self, id, valor_meta=None, data_inicio=None, data_fim=None, concluida=None, motorista_id=None):
        meta = Meta.buscar_por_id(id)
        if meta is None:
            raise RecursoNaoEncontrado("Meta não encontrada.")

        if valor_meta is not None:
            meta.valor_meta = exigir_numero_positivo(valor_meta, "O valor da meta deve ser maior que zero.")
        if data_inicio is not None:
            meta.data_inicio = data_inicio
        if data_fim is not None:
            meta.data_fim = data_fim
        if concluida is not None:
            meta.concluida = bool(concluida)
        if motorista_id is not None:
            if Motorista.buscar_por_id(motorista_id) is None:
                raise ValueError("Motorista não encontrado.")
            meta.motorista_id = motorista_id

        if meta.data_fim < meta.data_inicio:
            raise ValueError("A data final não pode ser anterior à data de início.")

        return meta.atualizar()

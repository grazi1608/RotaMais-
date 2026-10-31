from models.motorista import Motorista
from services.excecoes import RecursoNaoEncontrado


class ExcluirMotorista:
    """Caso de uso: excluir um motorista existente (veículos, corridas, metas,
    gastos e objetivos dele saem junto)."""

    def executar(self, id):
        motorista = Motorista.buscar_por_id(id)

        if motorista is None:
            raise RecursoNaoEncontrado("Motorista não encontrado.")

        motorista.deletar()

        return {"mensagem": "Motorista excluído com sucesso."}

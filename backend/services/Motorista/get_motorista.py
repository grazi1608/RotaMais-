from models.motorista import Motorista
from services.excecoes import RecursoNaoEncontrado


class BuscarMotorista:
    """Caso de uso: buscar um motorista pelo id."""

    def executar(self, id):
        motorista = Motorista.buscar_por_id(id)

        if motorista is None:
            raise RecursoNaoEncontrado("Motorista não encontrado.")

        return motorista.to_dict()

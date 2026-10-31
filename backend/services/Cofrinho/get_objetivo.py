from models.objetivo_cofrinho import ObjetivoCofrinho
from services.excecoes import RecursoNaoEncontrado


class BuscarObjetivoCofrinho:
    """Caso de uso: buscar um objetivo pelo id, garantindo que pertence ao motorista logado."""

    def executar(self, id, motorista_id):
        objetivo = ObjetivoCofrinho.buscar_por_id(id)

        if objetivo is None or objetivo.motorista_id != motorista_id:
            raise RecursoNaoEncontrado("Objetivo não encontrado.")

        return objetivo

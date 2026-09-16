from models.gasto import Gasto


class BuscarGasto:
    """Caso de uso: buscar um gasto pelo id, garantindo que pertence ao motorista logado."""

    def executar(self, id, motorista_id):
        gasto = Gasto.buscar_por_id(id)

        if gasto is None or gasto.motorista_id != motorista_id:
            raise ValueError("Gasto não encontrado.")

        return gasto

from models.corrida import Corrida


class BuscarCorrida:
    """Caso de uso: buscar uma corrida pelo id."""

    def executar(self, id):
        corrida = Corrida.buscar_por_id(id)

        if corrida is None:
            raise ValueError("Corrida não encontrada.")

        return corrida.to_dict()

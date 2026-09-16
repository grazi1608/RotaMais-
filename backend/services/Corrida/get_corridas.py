from models.corrida import Corrida


class ListarCorridas:
    """Caso de uso: listar todas as corridas registradas."""

    def executar(self):
        corridas = Corrida.listar_todos()
        return [corrida.to_dict() for corrida in corridas]

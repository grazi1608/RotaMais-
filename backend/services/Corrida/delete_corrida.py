from models.corrida import Corrida


class ExcluirCorrida:
    """Caso de uso: excluir uma corrida existente."""

    def executar(self, id):
        corrida = Corrida.buscar_por_id(id)

        if corrida is None:
            raise ValueError("Corrida não encontrada.")

        corrida.deletar()

        return {"mensagem": "Corrida excluída com sucesso."}

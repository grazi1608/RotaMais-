from models.motorista import Motorista


class ExcluirMotorista:
    """Caso de uso: excluir um motorista existente."""

    def executar(self, id):
        motorista = Motorista.buscar_por_id(id)

        if motorista is None:
            raise ValueError("Motorista não encontrado.")

        motorista.deletar()

        return {"mensagem": "Motorista excluído com sucesso."}

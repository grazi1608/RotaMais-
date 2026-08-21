from models.motorista import Motorista


class BuscarMotorista:
    """Caso de uso: buscar um motorista pelo id."""

    def executar(self, id):
        motorista = Motorista.buscar_por_id(id)

        if motorista is None:
            raise ValueError("Motorista não encontrado.")

        return motorista.to_dict()

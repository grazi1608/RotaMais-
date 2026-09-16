from models.motorista import Motorista


class ListarMotoristas:
    """Caso de uso: listar todos os motoristas cadastrados."""

    def executar(self):
        motoristas = Motorista.listar_todos()
        return [motorista.to_dict() for motorista in motoristas]

from models.gasto import Gasto


class ListarGastosDoMotorista:
    """Caso de uso: listar os gastos de um motorista, do mais recente para o mais antigo."""

    def executar(self, motorista_id):
        gastos = (
            Gasto.query
            .filter_by(motorista_id=motorista_id)
            .order_by(Gasto.data.desc())
            .all()
        )
        return [gasto.to_dict() for gasto in gastos]

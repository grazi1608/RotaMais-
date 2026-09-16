from models.objetivo_cofrinho import ObjetivoCofrinho


class ListarObjetivosCofrinho:
    """Caso de uso: listar os objetivos de cofrinho de um motorista e o total guardado."""

    def executar(self, motorista_id):
        objetivos = ObjetivoCofrinho.query.filter_by(motorista_id=motorista_id).all()

        return {
            "total_guardado": sum(o.valor_guardado for o in objetivos),
            "objetivos": [o.to_dict() for o in objetivos],
        }

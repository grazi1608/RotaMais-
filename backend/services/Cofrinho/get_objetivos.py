from models.objetivo_cofrinho import ObjetivoCofrinho
from repositories import CofrinhoRepository


class ListarObjetivosCofrinho:
    """Caso de uso: listar os objetivos de cofrinho de um motorista e o total guardado."""

    def __init__(self):
        self.repositorio = CofrinhoRepository()

    def executar(self, motorista_id):
        linhas = self.repositorio.listar_por_motorista(motorista_id)
        total_guardado = self.repositorio.total_guardado_por_motorista(motorista_id)

        objetivos = [
            {
                **linha,
                "progresso": ObjetivoCofrinho.calcular_progresso(
                    linha["valor_guardado"], linha["valor_meta"]
                ),
            }
            for linha in linhas
        ]

        return {
            "total_guardado": float(total_guardado or 0),
            "objetivos": objetivos,
        }

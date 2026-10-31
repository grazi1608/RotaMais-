from models.objetivo_cofrinho import ObjetivoCofrinho
from services.validacoes import exigir_texto, exigir_numero_positivo


class CriarObjetivoCofrinho:
    """Caso de uso: criar um novo objetivo de economia no cofrinho."""

    def executar(self, nome, valor_meta, motorista_id):
        nome = exigir_texto(nome, "Informe um nome para o objetivo.")
        valor_meta = exigir_numero_positivo(valor_meta, "O valor da meta deve ser maior que zero.")

        objetivo = ObjetivoCofrinho(
            nome=nome,
            valor_meta=valor_meta,
            motorista_id=motorista_id,
        )

        return objetivo.salvar()

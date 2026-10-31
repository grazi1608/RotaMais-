from services.validacoes import exigir_numero_positivo
from .get_objetivo import BuscarObjetivoCofrinho


class GuardarDinheiroNoObjetivo:
    """Caso de uso: adicionar um valor guardado a um objetivo do cofrinho."""

    def executar(self, id, motorista_id, valor):
        objetivo = BuscarObjetivoCofrinho().executar(id, motorista_id)
        valor = exigir_numero_positivo(valor, "Informe um valor maior que zero para guardar.")

        objetivo.guardar(valor)

        return objetivo.atualizar()

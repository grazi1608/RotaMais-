from .get_objetivo import BuscarObjetivoCofrinho


class GuardarDinheiroNoObjetivo:
    """Caso de uso: adicionar um valor guardado a um objetivo do cofrinho."""

    def executar(self, id, motorista_id, valor):
        if valor is None or valor <= 0:
            raise ValueError("Informe um valor maior que zero para guardar.")

        objetivo = BuscarObjetivoCofrinho().executar(id, motorista_id)
        objetivo.guardar(valor)

        return objetivo.atualizar()

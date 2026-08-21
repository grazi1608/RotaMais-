from repositories import RelatorioRepository


class GerarRelatorioLucro:
    """Caso de uso: gerar o relatório de lucro por motorista.

    Coordena a chamada ao Repository (consulta agregada) — não acessa
    o banco diretamente, isso é responsabilidade do Repository.
    """

    def __init__(self):
        self.repositorio = RelatorioRepository()

    def executar(self):
        return self.repositorio.lucro_por_motorista()

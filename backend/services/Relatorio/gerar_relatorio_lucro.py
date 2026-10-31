from repositories import RelatorioRepository


class GerarRelatorioLucro:
    """Caso de uso: gerar o relatório de lucro por motorista.

    Coordena a chamada ao Repository (consulta agregada em SQL) — não acessa
    o banco diretamente, isso é responsabilidade do Repository.
    """

    def __init__(self):
        self.repositorio = RelatorioRepository()

    def executar(self):
        return [
            {
                "motorista_id": linha["motorista_id"],
                "motorista_nome": linha["motorista_nome"],
                "total_corridas": int(linha["total_corridas"]),
                "total_faturado": float(linha["total_faturado"]),
                "total_custo": float(linha["total_custo"]),
                "total_lucro": float(linha["total_lucro"]),
            }
            for linha in self.repositorio.lucro_por_motorista()
        ]

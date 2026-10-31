from repositories.base_repository import BaseRepository


class RelatorioRepository(BaseRepository):
    """Consultas especiais de relatório (agregações/agrupamentos) que não
    fazem sentido morar na Model nem no Service — apenas acesso a dados
    complexo, sem regra de negócio."""

    def lucro_por_motorista(self):
        """Agrupa as corridas por motorista e soma valor, custo e lucro."""
        return self._buscar_todos(
            """
            SELECT
                m.id                               AS motorista_id,
                m.nome                             AS motorista_nome,
                COUNT(c.id)                        AS total_corridas,
                COALESCE(SUM(c.valor), 0)          AS total_faturado,
                COALESCE(SUM(c.custo_estimado), 0) AS total_custo,
                COALESCE(SUM(c.lucro), 0)          AS total_lucro
            FROM motoristas m
            LEFT JOIN corridas c ON c.motorista_id = m.id
            GROUP BY m.id, m.nome
            ORDER BY total_lucro DESC
            """
        )

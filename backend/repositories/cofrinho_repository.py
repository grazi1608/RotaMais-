from repositories.base_repository import BaseRepository


class CofrinhoRepository(BaseRepository):
    """Consultas dos objetivos do cofrinho com filtro específico (SQL escrito)."""

    def listar_por_motorista(self, motorista_id):
        return self._buscar_todos(
            """
            SELECT id, nome, valor_meta, valor_guardado, motorista_id
            FROM objetivos_cofrinho
            WHERE motorista_id = :motorista_id
            ORDER BY id
            """,
            {"motorista_id": motorista_id},
        )

    def total_guardado_por_motorista(self, motorista_id):
        """Soma de tudo o que o motorista já guardou em todos os objetivos."""
        return self._buscar_valor(
            """
            SELECT COALESCE(SUM(valor_guardado), 0)
            FROM objetivos_cofrinho
            WHERE motorista_id = :motorista_id
            """,
            {"motorista_id": motorista_id},
        )

from repositories.base_repository import BaseRepository


class GastoRepository(BaseRepository):
    """Consultas de Gasto com filtro específico (SQL escrito)."""

    def listar_por_motorista(self, motorista_id):
        """Gastos do motorista, do mais recente para o mais antigo."""
        return self._buscar_todos(
            """
            SELECT id, tipo, descricao, valor, data, motorista_id, veiculo_id
            FROM gastos
            WHERE motorista_id = :motorista_id
            ORDER BY data DESC, id DESC
            """,
            {"motorista_id": motorista_id},
        )

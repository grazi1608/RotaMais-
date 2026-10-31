from repositories.base_repository import BaseRepository


class VeiculoRepository(BaseRepository):
    """Consultas de Veículo com filtro específico (SQL escrito)."""

    def buscar_id_por_placa(self, placa):
        # As placas são gravadas em maiúsculas (ver Veiculo.__init__).
        return self._buscar_id(
            "SELECT id FROM veiculos WHERE placa = :placa",
            {"placa": placa.upper()},
        )

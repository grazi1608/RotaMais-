from repositories.base_repository import BaseRepository


class MotoristaRepository(BaseRepository):
    """Consultas de Motorista com filtro específico (SQL escrito).

    Devolvem só o id encontrado; o Service carrega o objeto pela Model
    (Motorista.buscar_por_id) quando precisa dele.
    """

    def buscar_id_por_cpf(self, cpf):
        return self._buscar_id(
            "SELECT id FROM motoristas WHERE cpf = :cpf",
            {"cpf": cpf},
        )

    def buscar_id_por_cnh(self, cnh):
        return self._buscar_id(
            "SELECT id FROM motoristas WHERE cnh = :cnh",
            {"cnh": cnh},
        )

    def buscar_id_por_email(self, email):
        return self._buscar_id(
            "SELECT id FROM motoristas WHERE LOWER(email) = LOWER(:email)",
            {"email": email},
        )

    def buscar_id_por_email_ou_telefone(self, identificador):
        """Login: o motorista pode entrar com o e-mail ou com o telefone."""
        return self._buscar_id(
            """
            SELECT id FROM motoristas
            WHERE LOWER(email) = LOWER(:identificador) OR telefone = :identificador
            """,
            {"identificador": identificador},
        )

    def buscar_id_por_token(self, token):
        return self._buscar_id(
            "SELECT id FROM motoristas WHERE token = :token",
            {"token": token},
        )

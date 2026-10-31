from sqlalchemy import text

from models import db


class BaseRepository:
    """
    Superclasse dos Repositories.

    Os Repositories guardam as consultas especiais do sistema (filtros
    específicos, relatórios, agregações) escritas em SQL (SELECT, JOIN,
    GROUP BY...). O SQLAlchemy aqui serve apenas como conexão: o texto da
    consulta é nosso e os parâmetros vão separados (:nome), o que evita
    SQL Injection.

    Controllers e Services nunca escrevem SQL — só chamam estes métodos.
    """

    def _buscar_todos(self, sql, parametros=None):
        """Executa um SELECT e devolve uma lista de dicionários."""
        resultado = db.session.execute(text(sql), parametros or {})
        return [dict(linha) for linha in resultado.mappings().all()]

    def _buscar_um(self, sql, parametros=None):
        """Executa um SELECT e devolve só a primeira linha (ou None)."""
        resultado = db.session.execute(text(sql), parametros or {})
        linha = resultado.mappings().first()
        return dict(linha) if linha else None

    def _buscar_valor(self, sql, parametros=None):
        """Executa um SELECT que devolve um único valor (ex.: COUNT, SUM)."""
        return db.session.execute(text(sql), parametros or {}).scalar()

    def _buscar_id(self, sql, parametros=None):
        """Executa um SELECT id ... e devolve o id encontrado (ou None)."""
        linha = self._buscar_um(sql, parametros)
        return linha["id"] if linha else None

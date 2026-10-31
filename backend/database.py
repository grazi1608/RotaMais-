"""Acesso ao banco de dados com SQL puro (módulo sqlite3 da biblioteca padrão).

Não usamos ORM: todo SQL do projeto está escrito como texto, com parâmetros
(`?`) para evitar SQL injection. Este módulo só abre a conexão e executa o
SQL que as Models e os Repositories mandam.
"""

import os
import sqlite3

PASTA_BACKEND = os.path.abspath(os.path.dirname(__file__))

# Caminho ABSOLUTO do banco: sempre backend/instance/rotamais.db, não importa de
# qual pasta o "python app.py" foi executado. (ROTAMAIS_DB permite trocar o
# arquivo, útil em testes.)
CAMINHO_BANCO = os.environ.get("ROTAMAIS_DB") or os.path.join(
    PASTA_BACKEND, "instance", "rotamais.db"
)
CAMINHO_SCHEMA = os.path.join(PASTA_BACKEND, "schema.sql")


def conectar():
    """Abre uma conexão. Linhas retornam como sqlite3.Row (acesso por nome da coluna)."""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    # No SQLite as chaves estrangeiras só valem se ativadas em cada conexão.
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def executar(sql, parametros=()):
    """Executa INSERT/UPDATE/DELETE, confirma a transação e devolve o id inserido."""
    conexao = conectar()
    try:
        cursor = conexao.execute(sql, parametros)
        conexao.commit()
        return cursor.lastrowid
    finally:
        conexao.close()


def buscar_um(sql, parametros=()):
    """Executa um SELECT e devolve a primeira linha (ou None)."""
    conexao = conectar()
    try:
        return conexao.execute(sql, parametros).fetchone()
    finally:
        conexao.close()


def buscar_todos(sql, parametros=()):
    """Executa um SELECT e devolve todas as linhas."""
    conexao = conectar()
    try:
        return conexao.execute(sql, parametros).fetchall()
    finally:
        conexao.close()


def init_db():
    """Cria as tabelas (se ainda não existirem) a partir do schema.sql."""
    os.makedirs(os.path.dirname(CAMINHO_BANCO), exist_ok=True)

    with open(CAMINHO_SCHEMA, encoding="utf-8") as arquivo:
        script = arquivo.read()

    conexao = conectar()
    try:
        conexao.executescript(script)
        conexao.commit()
    finally:
        conexao.close()

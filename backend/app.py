import os
import secrets
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from controllers import TODOS_OS_BLUEPRINTS
from models import db

PASTA_BACKEND = Path(__file__).resolve().parent


@event.listens_for(Engine, "connect")
def _ativar_chaves_estrangeiras(conexao, _registro):
    """No SQLite as chaves estrangeiras só valem se ativadas em cada conexão."""
    if conexao.__class__.__module__.startswith("sqlite3"):
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.close()


def carregar_chave_secreta():
    """Chave secreta do Flask, lida do .env (SECRET_KEY). Se não estiver
    configurada, usa uma chave aleatória só para esta execução."""
    chave = os.getenv("SECRET_KEY", "")
    if not chave or chave == "troque-por-uma-chave-aleatoria":
        print("AVISO: SECRET_KEY não configurada no backend/.env. Usando uma chave temporária.")
        return secrets.token_urlsafe(32)
    return chave


def endereco_do_banco():
    """SQLite em backend/instance/rotamais.db, não importa de qual pasta o
    "python app.py" foi executado. (ROTAMAIS_DB permite trocar o arquivo,
    útil em testes; DATABASE_URL permite usar outro banco.)"""
    url_configurada = os.getenv("DATABASE_URL")
    if url_configurada:
        return url_configurada

    arquivo = Path(os.getenv("ROTAMAIS_DB") or PASTA_BACKEND / "instance" / "rotamais.db")
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{arquivo.as_posix()}"


def create_app():
    load_dotenv(PASTA_BACKEND / ".env")

    # A API roda sozinha (porta 5000); o frontend é servido por outro servidor
    # (porta 5500) e consome a API por fetch — por isso o CORS liberado.
    app = Flask(__name__)
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = endereco_do_banco()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = carregar_chave_secreta()
    app.json.ensure_ascii = False

    db.init_app(app)

    # Registro dos Blueprints da API (JSON)
    for blueprint, prefixo in TODOS_OS_BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix=prefixo)

    # Tratamento central de erro de banco: a transação é desfeita e a API
    # responde 500. Assim nenhum Controller precisa conhecer o db.session.
    @app.errorhandler(SQLAlchemyError)
    def erro_de_banco(erro):
        db.session.rollback()
        return jsonify({"erro": "Erro ao acessar o banco de dados."}), 500

    @app.get("/")
    def api_info():
        return jsonify({
            "mensagem": "API do RotaMais (Flask + SQLAlchemy) funcionando.",
            "frontend": "http://127.0.0.1:5500",
            "rotas": {
                "motoristas": "/motoristas",
                "veiculos": "/veiculos",
                "corridas": "/corridas",
                "metas": "/metas",
                "relatorios": "/relatorios/lucro-por-motorista",
                "auth": "/auth/registrar, /auth/login, /auth/logout, /auth/me",
                "gastos": "/gastos",
                "cofrinho": "/cofrinho, /cofrinho/<id>/guardar",
            },
        })

    with app.app_context():
        # Cria as tabelas das Models que ainda não existem (não apaga dados).
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "True") == "True"
    app.run(debug=debug, host="127.0.0.1", port=5000)

from flask import Flask, jsonify
from flask_cors import CORS

from models import db

from controllers.motorista_controller import motorista_bp
from controllers.veiculo_controller import veiculo_bp
from controllers.corrida_controller import corrida_bp
from controllers.meta_controller import meta_bp
from controllers.relatorio_controller import relatorio_bp


def create_app():
    # A API agora é 100% JSON. O frontend é estático (HTML/CSS/JS puro)
    # e roda separado (outra origem/porta), por isso liberamos o CORS.
    app = Flask(__name__)
    CORS(app)  # libera o acesso da API para o frontend estático (outra origem/porta)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rotamais.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "rotamais"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Registro dos Blueprints da API (JSON)
    app.register_blueprint(motorista_bp, url_prefix="/motoristas")
    app.register_blueprint(veiculo_bp, url_prefix="/veiculos")
    app.register_blueprint(corrida_bp, url_prefix="/corridas")
    app.register_blueprint(meta_bp, url_prefix="/metas")
    app.register_blueprint(relatorio_bp, url_prefix="/relatorios")

    @app.get("/")
    def home():
        return jsonify({
            "mensagem": "API do RotaMais (Flask + SQLAlchemy) funcionando.",
            "rotas": {
                "motoristas": "/motoristas",
                "veiculos": "/veiculos",
                "corridas": "/corridas",
                "metas": "/metas",
                "relatorios": "/relatorios/lucro-por-motorista",
            },
        })

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

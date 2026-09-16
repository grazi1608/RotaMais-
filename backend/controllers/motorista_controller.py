from flask import Blueprint, request, jsonify
from flask.views import MethodView

from services.Motorista import (
    CriarMotorista,
    BuscarMotorista,
    ListarMotoristas,
    AtualizarMotorista,
    ExcluirMotorista,
)

motorista_bp = Blueprint("motorista", __name__)


class MotoristaController(MethodView):
    """Controller do recurso Motorista: recebe a requisição HTTP, interpreta
    os dados e delega a regra de negócio para o Service correspondente."""

    def get(self, id=None):
        if id is None:
            motoristas = ListarMotoristas().executar()
            return jsonify(motoristas), 200

        try:
            motorista = BuscarMotorista().executar(id)
            return jsonify(motorista), 200
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404

    def post(self):
        dados = request.get_json()

        try:
            motorista = CriarMotorista().executar(
                nome=dados["nome"],
                cpf=dados["cpf"],
                cnh=dados["cnh"],
                telefone=dados.get("telefone"),
                email=dados.get("email"),
            )
            return jsonify(motorista.to_dict()), 201
        except KeyError:
            return jsonify({"erro": "Campos obrigatórios não informados."}), 400
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

    def put(self, id):
        dados = request.get_json()

        try:
            motorista = AtualizarMotorista().executar(
                id=id,
                nome=dados["nome"],
                cpf=dados["cpf"],
                cnh=dados["cnh"],
                telefone=dados.get("telefone"),
                email=dados.get("email"),
            )
            return jsonify(motorista.to_dict()), 200
        except KeyError:
            return jsonify({"erro": "Campos obrigatórios não informados."}), 400
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404

    def delete(self, id):
        try:
            resultado = ExcluirMotorista().executar(id)
            return jsonify(resultado), 200
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404


motorista_view = MotoristaController.as_view("motorista_api")
motorista_bp.add_url_rule("", defaults={"id": None}, view_func=motorista_view, methods=["GET"])
motorista_bp.add_url_rule("", view_func=motorista_view, methods=["POST"])
motorista_bp.add_url_rule("/<int:id>", view_func=motorista_view, methods=["GET", "PUT", "DELETE"])

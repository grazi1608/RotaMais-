from flask import Blueprint, request, jsonify
from flask.views import MethodView
from datetime import datetime

from services.Corrida import (
    CriarCorrida,
    BuscarCorrida,
    ListarCorridas,
    AtualizarCorrida,
    ExcluirCorrida,
)
from utils.auth import login_required

corrida_bp = Blueprint("corrida", __name__)


def formatar_data_hora(data_hora_str):
    """Converte string ISO (ex: '2026-01-01T10:00:00') em datetime, se houver valor."""
    if data_hora_str:
        return datetime.fromisoformat(data_hora_str)
    return None


class CorridaController(MethodView):
    """Controller do recurso Corrida: recebe a requisição HTTP, interpreta
    os dados e delega a regra de negócio para o Service correspondente."""

    decorators = [login_required]

    def get(self, id=None):
        if id is None:
            corridas = ListarCorridas().executar()
            return jsonify(corridas), 200

        try:
            corrida = BuscarCorrida().executar(id)
            return jsonify(corrida), 200
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404

    def post(self):
        dados = request.get_json()

        try:
            corrida = CriarCorrida().executar(
                valor=dados["valor"],
                distancia=dados["distancia"],
                motorista_id=dados["motorista_id"],
                veiculo_id=dados["veiculo_id"],
            )
            return jsonify(corrida.to_dict()), 201
        except KeyError:
            return jsonify({"erro": "Campos obrigatórios não informados."}), 400
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

    def put(self, id):
        dados = request.get_json()

        try:
            corrida = AtualizarCorrida().executar(
                id=id,
                data_hora=formatar_data_hora(dados.get("data_hora")),
                valor=dados["valor"],
                distancia=dados["distancia"],
                motorista_id=dados["motorista_id"],
                veiculo_id=dados["veiculo_id"],
            )
            return jsonify(corrida.to_dict()), 200
        except KeyError:
            return jsonify({"erro": "Campos obrigatórios não informados."}), 400
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404

    def delete(self, id):
        try:
            resultado = ExcluirCorrida().executar(id)
            return jsonify(resultado), 200
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404


corrida_view = CorridaController.as_view("corrida_api")
corrida_bp.add_url_rule("", defaults={"id": None}, view_func=corrida_view, methods=["GET"])
corrida_bp.add_url_rule("", view_func=corrida_view, methods=["POST"])
corrida_bp.add_url_rule("/<int:id>", view_func=corrida_view, methods=["GET", "PUT", "DELETE"])

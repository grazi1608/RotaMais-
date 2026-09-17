from datetime import datetime
from flask import Blueprint, request, jsonify
from flask.views import MethodView

from services.Gasto import (
    CriarGasto,
    BuscarGasto,
    ListarGastosDoMotorista,
    AtualizarGasto,
    ExcluirGasto,
)
from utils.auth import login_required

gasto_bp = Blueprint("gasto", __name__)


def formatar_data_hora(data_hora_str):
    if data_hora_str:
        return datetime.fromisoformat(data_hora_str)
    return None


class GastoController(MethodView):
    """Controller do recurso Gasto: os gastos sempre pertencem ao motorista
    autenticado (request.motorista_atual), nunca a um motorista_id enviado
    pelo cliente — evita que alguém registre gasto em nome de outro."""

    decorators = [login_required]

    def get(self, id=None):
        motorista_id = request.motorista_atual.id

        if id is None:
            gastos = ListarGastosDoMotorista().executar(motorista_id)
            return jsonify(gastos), 200

        try:
            gasto = BuscarGasto().executar(id, motorista_id)
            return jsonify(gasto.to_dict()), 200
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404

    def post(self):
        dados = request.get_json()
        motorista_id = request.motorista_atual.id

        try:
            gasto = CriarGasto().executar(
                tipo=dados["tipo"],
                valor=dados["valor"],
                motorista_id=motorista_id,
                descricao=dados.get("descricao"),
                veiculo_id=dados.get("veiculo_id"),
                data=formatar_data_hora(dados.get("data")),
            )
            return jsonify(gasto.to_dict()), 201
        except KeyError:
            return jsonify({"erro": "Campos obrigatórios não informados."}), 400
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

    def put(self, id):
        dados = request.get_json()
        motorista_id = request.motorista_atual.id

        try:
            gasto = AtualizarGasto().executar(
                id=id,
                motorista_id=motorista_id,
                tipo=dados["tipo"],
                valor=dados["valor"],
                descricao=dados.get("descricao"),
                veiculo_id=dados.get("veiculo_id"),
                data=formatar_data_hora(dados.get("data")),
            )
            return jsonify(gasto.to_dict()), 200
        except KeyError:
            return jsonify({"erro": "Campos obrigatórios não informados."}), 400
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404

    def delete(self, id):
        motorista_id = request.motorista_atual.id

        try:
            resultado = ExcluirGasto().executar(id, motorista_id)
            return jsonify(resultado), 200
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404


gasto_view = GastoController.as_view("gasto_api")
gasto_bp.add_url_rule("", defaults={"id": None}, view_func=gasto_view, methods=["GET"])
gasto_bp.add_url_rule("", view_func=gasto_view, methods=["POST"])
gasto_bp.add_url_rule("/<int:id>", view_func=gasto_view, methods=["GET", "PUT", "DELETE"])

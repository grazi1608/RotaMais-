from flask import Blueprint, request, jsonify
from flask.views import MethodView

from services.Veiculo import (
    CriarVeiculo,
    BuscarVeiculo,
    ListarVeiculos,
    AtualizarVeiculo,
    ExcluirVeiculo,
)

veiculo_bp = Blueprint("veiculo", __name__)


class VeiculoController(MethodView):
    """Controller do recurso Veículo: recebe a requisição HTTP, interpreta
    os dados e delega a regra de negócio para o Service correspondente."""

    def get(self, id=None):
        if id is None:
            veiculos = ListarVeiculos().executar()
            return jsonify(veiculos), 200

        try:
            veiculo = BuscarVeiculo().executar(id)
            return jsonify(veiculo), 200
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404

    def post(self):
        dados = request.get_json()

        try:
            veiculo = CriarVeiculo().executar(
                placa=dados["placa"],
                modelo=dados["modelo"],
                consumo_por_km=dados["consumo_por_km"],
                motorista_id=dados["motorista_id"],
            )
            return jsonify(veiculo.to_dict()), 201
        except KeyError:
            return jsonify({"erro": "Campos obrigatórios não informados."}), 400
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

    def put(self, id):
        dados = request.get_json()

        try:
            veiculo = AtualizarVeiculo().executar(
                id=id,
                placa=dados["placa"],
                modelo=dados["modelo"],
                consumo_por_km=dados["consumo_por_km"],
                motorista_id=dados["motorista_id"],
            )
            return jsonify(veiculo.to_dict()), 200
        except KeyError:
            return jsonify({"erro": "Campos obrigatórios não informados."}), 400
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404

    def delete(self, id):
        try:
            resultado = ExcluirVeiculo().executar(id)
            return jsonify(resultado), 200
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404


veiculo_view = VeiculoController.as_view("veiculo_api")
veiculo_bp.add_url_rule("", defaults={"id": None}, view_func=veiculo_view, methods=["GET"])
veiculo_bp.add_url_rule("", view_func=veiculo_view, methods=["POST"])
veiculo_bp.add_url_rule("/<int:id>", view_func=veiculo_view, methods=["GET", "PUT", "DELETE"])

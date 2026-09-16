from flask import Blueprint, request, jsonify
from flask.views import MethodView

from services.Cofrinho import (
    CriarObjetivoCofrinho,
    BuscarObjetivoCofrinho,
    ListarObjetivosCofrinho,
    AtualizarObjetivoCofrinho,
    GuardarDinheiroNoObjetivo,
    ExcluirObjetivoCofrinho,
)
from utils.auth import login_required

cofrinho_bp = Blueprint("cofrinho", __name__)


class CofrinhoController(MethodView):
    """Controller dos objetivos de cofrinho do motorista autenticado."""

    decorators = [login_required]

    def get(self, id=None):
        motorista_id = request.motorista_atual.id

        if id is None:
            resultado = ListarObjetivosCofrinho().executar(motorista_id)
            return jsonify(resultado), 200

        try:
            objetivo = BuscarObjetivoCofrinho().executar(id, motorista_id)
            return jsonify(objetivo.to_dict()), 200
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404

    def post(self):
        dados = request.get_json()
        motorista_id = request.motorista_atual.id

        try:
            objetivo = CriarObjetivoCofrinho().executar(
                nome=dados["nome"],
                valor_meta=dados["valor_meta"],
                motorista_id=motorista_id,
            )
            return jsonify(objetivo.to_dict()), 201
        except KeyError:
            return jsonify({"erro": "Campos obrigatórios não informados."}), 400
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

    def put(self, id):
        dados = request.get_json()
        motorista_id = request.motorista_atual.id

        try:
            objetivo = AtualizarObjetivoCofrinho().executar(
                id=id,
                motorista_id=motorista_id,
                nome=dados["nome"],
                valor_meta=dados["valor_meta"],
            )
            return jsonify(objetivo.to_dict()), 200
        except KeyError:
            return jsonify({"erro": "Campos obrigatórios não informados."}), 400
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404

    def delete(self, id):
        motorista_id = request.motorista_atual.id

        try:
            resultado = ExcluirObjetivoCofrinho().executar(id, motorista_id)
            return jsonify(resultado), 200
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404


class GuardarDinheiroController(MethodView):
    """Controller da ação específica de 'guardar dinheiro' em um objetivo."""

    decorators = [login_required]

    def post(self, id):
        dados = request.get_json()
        motorista_id = request.motorista_atual.id

        try:
            objetivo = GuardarDinheiroNoObjetivo().executar(
                id=id,
                motorista_id=motorista_id,
                valor=dados.get("valor"),
            )
            return jsonify(objetivo.to_dict()), 200
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400


cofrinho_view = CofrinhoController.as_view("cofrinho_api")
cofrinho_bp.add_url_rule("", defaults={"id": None}, view_func=cofrinho_view, methods=["GET"])
cofrinho_bp.add_url_rule("", view_func=cofrinho_view, methods=["POST"])
cofrinho_bp.add_url_rule("/<int:id>", view_func=cofrinho_view, methods=["GET", "PUT", "DELETE"])

guardar_view = GuardarDinheiroController.as_view("cofrinho_guardar_api")
cofrinho_bp.add_url_rule("/<int:id>/guardar", view_func=guardar_view, methods=["POST"])

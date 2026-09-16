from flask import Blueprint, request, jsonify
from flask.views import MethodView
from datetime import datetime

from services.Meta import (
    CriarMeta,
    ListarMetas,
    BuscarMeta,
    AtualizarMeta,
    ExcluirMeta,
)
from utils.auth import login_required

meta_bp = Blueprint("meta", __name__)


def formatar_data(data_str):
    if data_str:
        return datetime.strptime(data_str, "%Y-%m-%d").date()
    return None


class MetaController(MethodView):
    """Controller do recurso Meta: recebe a requisição HTTP, interpreta
    os dados e delega a regra de negócio para o Service correspondente."""

    decorators = [login_required]

    def get(self, id=None):
        if id is None:
            metas = ListarMetas().executar()
            return jsonify([meta.to_dict() for meta in metas]), 200

        try:
            meta = BuscarMeta().executar(id)
            return jsonify(meta.to_dict()), 200
        except ValueError as erro:
            return jsonify({"error": str(erro)}), 404

    def post(self):
        dados = request.get_json()

        try:
            data_fim = formatar_data(dados.get("data_fim"))
            data_inicio = formatar_data(dados.get("data_inicio"))

            nova_meta = CriarMeta().executar(
                valor_meta=dados.get("valor_meta"),
                data_fim=data_fim,
                motorista_id=dados.get("motorista_id"),
                data_inicio=data_inicio,
                concluida=dados.get("concluida", False),
            )
            return jsonify(nova_meta.to_dict()), 201
        except Exception as erro:
            return jsonify({"error": str(erro)}), 400

    def put(self, id):
        dados = request.get_json()

        try:
            data_fim = formatar_data(dados.get("data_fim"))
            data_inicio = formatar_data(dados.get("data_inicio"))

            meta_atualizada = AtualizarMeta().executar(
                id=id,
                valor_meta=dados.get("valor_meta"),
                data_inicio=data_inicio,
                data_fim=data_fim,
                concluida=dados.get("concluida"),
                motorista_id=dados.get("motorista_id"),
            )
            return jsonify(meta_atualizada.to_dict()), 200
        except ValueError as erro:
            return jsonify({"error": str(erro)}), 404
        except Exception as erro:
            return jsonify({"error": str(erro)}), 400

    def delete(self, id):
        try:
            resultado = ExcluirMeta().executar(id)
            return jsonify(resultado), 200
        except ValueError as erro:
            return jsonify({"error": str(erro)}), 404


meta_view = MetaController.as_view("meta_api")
meta_bp.add_url_rule("", defaults={"id": None}, view_func=meta_view, methods=["GET"])
meta_bp.add_url_rule("", view_func=meta_view, methods=["POST"])
meta_bp.add_url_rule("/<int:id>", view_func=meta_view, methods=["GET", "PUT", "DELETE"])

from flask import Blueprint, jsonify
from flask.views import MethodView

from services.Relatorio import GerarRelatorioLucro

relatorio_bp = Blueprint("relatorio", __name__)


class RelatorioLucroController(MethodView):
    """Controller do relatório de lucro por motorista."""

    def get(self):
        relatorio = GerarRelatorioLucro().executar()
        return jsonify(relatorio), 200


relatorio_view = RelatorioLucroController.as_view("relatorio_lucro_api")
relatorio_bp.add_url_rule("/lucro-por-motorista", view_func=relatorio_view, methods=["GET"])

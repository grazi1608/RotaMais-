from flask import Blueprint

from controllers.base_controller import BaseController
from services.Relatorio import GerarRelatorioLucro
from utils.auth import login_required

relatorio_bp = Blueprint("relatorio", __name__)


class RelatorioLucroController(BaseController):
    """Controller do relatório de lucro por motorista."""

    decorators = [login_required]

    def get(self):
        return self.responder(GerarRelatorioLucro().executar())


relatorio_view = RelatorioLucroController.as_view("relatorio_lucro_api")
relatorio_bp.add_url_rule("/lucro-por-motorista", view_func=relatorio_view, methods=["GET"])

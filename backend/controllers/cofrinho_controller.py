from flask import Blueprint, request

from controllers.base_controller import BaseController
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


class CofrinhoController(BaseController):
    """Controller dos objetivos de cofrinho do motorista autenticado."""

    decorators = [login_required]

    def get(self, id=None):
        motorista_id = request.motorista_atual.id

        if id is None:
            return self.responder(ListarObjetivosCofrinho().executar(motorista_id))

        try:
            objetivo = BuscarObjetivoCofrinho().executar(id, motorista_id)
            return self.responder(objetivo.to_dict())
        except ValueError as erro:
            return self.responder_erro(erro)

    def post(self):
        dados = self.dados_json()

        try:
            objetivo = CriarObjetivoCofrinho().executar(
                nome=dados.get("nome"),
                valor_meta=dados.get("valor_meta"),
                motorista_id=request.motorista_atual.id,
            )
            return self.responder(objetivo.to_dict(), 201)
        except ValueError as erro:
            return self.responder_erro(erro)

    def put(self, id):
        dados = self.dados_json()

        try:
            objetivo = AtualizarObjetivoCofrinho().executar(
                id=id,
                motorista_id=request.motorista_atual.id,
                nome=dados.get("nome"),
                valor_meta=dados.get("valor_meta"),
            )
            return self.responder(objetivo.to_dict())
        except ValueError as erro:
            return self.responder_erro(erro)

    def delete(self, id):
        try:
            resultado = ExcluirObjetivoCofrinho().executar(id, request.motorista_atual.id)
            return self.responder(resultado)
        except ValueError as erro:
            return self.responder_erro(erro)


class GuardarDinheiroController(BaseController):
    """Controller da ação específica de "guardar dinheiro" em um objetivo."""

    decorators = [login_required]

    def post(self, id):
        dados = self.dados_json()

        try:
            objetivo = GuardarDinheiroNoObjetivo().executar(
                id=id,
                motorista_id=request.motorista_atual.id,
                valor=dados.get("valor"),
            )
            return self.responder(objetivo.to_dict())
        except ValueError as erro:
            return self.responder_erro(erro)


CofrinhoController.registrar_rotas(cofrinho_bp, "cofrinho_api")

guardar_view = GuardarDinheiroController.as_view("cofrinho_guardar_api")
cofrinho_bp.add_url_rule("/<int:id>/guardar", view_func=guardar_view, methods=["POST"])

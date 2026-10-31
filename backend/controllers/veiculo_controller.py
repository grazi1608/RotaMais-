from flask import Blueprint

from controllers.base_controller import BaseController
from services.Veiculo import (
    CriarVeiculo,
    BuscarVeiculo,
    ListarVeiculos,
    AtualizarVeiculo,
    ExcluirVeiculo,
)
from utils.auth import login_required

veiculo_bp = Blueprint("veiculo", __name__)


class VeiculoController(BaseController):
    """Controller do recurso Veículo: recebe a requisição HTTP, interpreta
    os dados e delega a regra de negócio para o Service correspondente."""

    decorators = [login_required]

    def get(self, id=None):
        if id is None:
            return self.responder(ListarVeiculos().executar())

        try:
            return self.responder(BuscarVeiculo().executar(id))
        except ValueError as erro:
            return self.responder_erro(erro)

    def post(self):
        dados = self.dados_json()

        try:
            veiculo = CriarVeiculo().executar(
                placa=dados.get("placa"),
                modelo=dados.get("modelo"),
                consumo_por_km=dados.get("consumo_por_km"),
                motorista_id=dados.get("motorista_id"),
            )
            return self.responder(veiculo.to_dict(), 201)
        except ValueError as erro:
            return self.responder_erro(erro)

    def put(self, id):
        dados = self.dados_json()

        try:
            veiculo = AtualizarVeiculo().executar(
                id=id,
                placa=dados.get("placa"),
                modelo=dados.get("modelo"),
                consumo_por_km=dados.get("consumo_por_km"),
                motorista_id=dados.get("motorista_id"),
            )
            return self.responder(veiculo.to_dict())
        except ValueError as erro:
            return self.responder_erro(erro)

    def delete(self, id):
        try:
            return self.responder(ExcluirVeiculo().executar(id))
        except ValueError as erro:
            return self.responder_erro(erro)


VeiculoController.registrar_rotas(veiculo_bp, "veiculo_api")

from flask import Blueprint, request

from controllers.base_controller import BaseController
from services.Gasto import (
    CriarGasto,
    BuscarGasto,
    ListarGastosDoMotorista,
    AtualizarGasto,
    ExcluirGasto,
)
from utils.auth import login_required

gasto_bp = Blueprint("gasto", __name__)


class GastoController(BaseController):
    """Controller do recurso Gasto: os gastos sempre pertencem ao motorista
    autenticado (request.motorista_atual), nunca a um motorista_id enviado
    pelo cliente — evita que alguém registre gasto em nome de outro."""

    decorators = [login_required]

    def get(self, id=None):
        motorista_id = request.motorista_atual.id

        if id is None:
            return self.responder(ListarGastosDoMotorista().executar(motorista_id))

        try:
            gasto = BuscarGasto().executar(id, motorista_id)
            return self.responder(gasto.to_dict())
        except ValueError as erro:
            return self.responder_erro(erro)

    def post(self):
        dados = self.dados_json()

        try:
            gasto = CriarGasto().executar(
                tipo=dados.get("tipo"),
                valor=dados.get("valor"),
                motorista_id=request.motorista_atual.id,
                descricao=dados.get("descricao"),
                veiculo_id=dados.get("veiculo_id"),
                data=self.ler_data_hora(dados.get("data")),
            )
            return self.responder(gasto.to_dict(), 201)
        except ValueError as erro:
            return self.responder_erro(erro)

    def put(self, id):
        dados = self.dados_json()

        try:
            gasto = AtualizarGasto().executar(
                id=id,
                motorista_id=request.motorista_atual.id,
                tipo=dados.get("tipo"),
                valor=dados.get("valor"),
                descricao=dados.get("descricao"),
                veiculo_id=dados.get("veiculo_id"),
                data=self.ler_data_hora(dados.get("data")),
            )
            return self.responder(gasto.to_dict())
        except ValueError as erro:
            return self.responder_erro(erro)

    def delete(self, id):
        try:
            return self.responder(ExcluirGasto().executar(id, request.motorista_atual.id))
        except ValueError as erro:
            return self.responder_erro(erro)


GastoController.registrar_rotas(gasto_bp, "gasto_api")

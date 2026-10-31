from flask import Blueprint

from controllers.base_controller import BaseController
from services.Corrida import (
    CriarCorrida,
    BuscarCorrida,
    ListarCorridas,
    AtualizarCorrida,
    ExcluirCorrida,
)
from utils.auth import login_required

corrida_bp = Blueprint("corrida", __name__)


class CorridaController(BaseController):
    """Controller do recurso Corrida: recebe a requisição HTTP, interpreta
    os dados e delega a regra de negócio para o Service correspondente."""

    decorators = [login_required]

    def get(self, id=None):
        if id is None:
            return self.responder(ListarCorridas().executar())

        try:
            return self.responder(BuscarCorrida().executar(id))
        except ValueError as erro:
            return self.responder_erro(erro)

    def post(self):
        dados = self.dados_json()

        try:
            corrida = CriarCorrida().executar(
                valor=dados.get("valor"),
                distancia=dados.get("distancia"),
                motorista_id=dados.get("motorista_id"),
                veiculo_id=dados.get("veiculo_id"),
            )
            return self.responder(corrida.to_dict(), 201)
        except ValueError as erro:
            return self.responder_erro(erro)

    def put(self, id):
        dados = self.dados_json()

        try:
            corrida = AtualizarCorrida().executar(
                id=id,
                data_hora=self.ler_data_hora(dados.get("data_hora")),
                valor=dados.get("valor"),
                distancia=dados.get("distancia"),
                motorista_id=dados.get("motorista_id"),
                veiculo_id=dados.get("veiculo_id"),
            )
            return self.responder(corrida.to_dict())
        except ValueError as erro:
            return self.responder_erro(erro)

    def delete(self, id):
        try:
            return self.responder(ExcluirCorrida().executar(id))
        except ValueError as erro:
            return self.responder_erro(erro)


CorridaController.registrar_rotas(corrida_bp, "corrida_api")

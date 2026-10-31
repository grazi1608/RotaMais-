from flask import Blueprint

from controllers.base_controller import BaseController
from services.Motorista import (
    CriarMotorista,
    BuscarMotorista,
    ListarMotoristas,
    AtualizarMotorista,
    ExcluirMotorista,
)
from utils.auth import login_required

motorista_bp = Blueprint("motorista", __name__)


class MotoristaController(BaseController):
    """Controller do recurso Motorista: recebe a requisição HTTP, interpreta
    os dados e delega a regra de negócio para o Service correspondente."""

    decorators = [login_required]

    def get(self, id=None):
        if id is None:
            return self.responder(ListarMotoristas().executar())

        try:
            return self.responder(BuscarMotorista().executar(id))
        except ValueError as erro:
            return self.responder_erro(erro)

    def post(self):
        dados = self.dados_json()

        try:
            motorista = CriarMotorista().executar(
                nome=dados.get("nome"),
                cpf=dados.get("cpf"),
                cnh=dados.get("cnh"),
                telefone=dados.get("telefone"),
                email=dados.get("email"),
            )
            return self.responder(motorista.to_dict(), 201)
        except ValueError as erro:
            return self.responder_erro(erro)

    def put(self, id):
        dados = self.dados_json()

        try:
            motorista = AtualizarMotorista().executar(
                id=id,
                nome=dados.get("nome"),
                cpf=dados.get("cpf"),
                cnh=dados.get("cnh"),
                telefone=dados.get("telefone"),
                email=dados.get("email"),
            )
            return self.responder(motorista.to_dict())
        except ValueError as erro:
            return self.responder_erro(erro)

    def delete(self, id):
        try:
            return self.responder(ExcluirMotorista().executar(id))
        except ValueError as erro:
            return self.responder_erro(erro)


MotoristaController.registrar_rotas(motorista_bp, "motorista_api")

from flask import Blueprint, request

from controllers.base_controller import BaseController
from services.Auth import RegistrarUsuario, AutenticarUsuario, EncerrarSessao
from utils.auth import login_required

auth_bp = Blueprint("auth", __name__)


class AuthController(BaseController):
    """Controller de autenticação: recebe a requisição HTTP, interpreta os
    dados e delega a regra de negócio para o Service correspondente."""

    def registrar(self):
        dados = self.dados_json()

        try:
            motorista = RegistrarUsuario().executar(
                nome=dados.get("nome"),
                cpf=dados.get("cpf"),
                cnh=dados.get("cnh"),
                email=dados.get("email"),
                senha=dados.get("senha"),
                telefone=dados.get("telefone"),
                data_nascimento=self.ler_data(dados.get("data_nascimento")),
            )

            return self.responder({
                "token": motorista.token,
                "motorista": motorista.to_dict()
            }, 201)

        except ValueError as erro:
            return self.responder_erro(erro)

    def login(self):
        dados = self.dados_json()

        try:
            motorista = AutenticarUsuario().executar(
                identificador=dados.get("identificador"),
                senha=dados.get("senha"),
            )

            return self.responder({
                "token": motorista.token,
                "motorista": motorista.to_dict()
            })

        except ValueError as erro:
            return self.responder({"erro": str(erro)}, 401)

    @login_required
    def logout(self):
        resultado = EncerrarSessao().executar(request.motorista_atual)
        return self.responder(resultado)

    @login_required
    def me(self):
        return self.responder({"motorista": request.motorista_atual.to_dict()})


auth_controller = AuthController()

auth_bp.add_url_rule("/registrar", view_func=auth_controller.registrar, methods=["POST"])
auth_bp.add_url_rule("/login", view_func=auth_controller.login, methods=["POST"])
auth_bp.add_url_rule("/logout", view_func=auth_controller.logout, methods=["POST"])
auth_bp.add_url_rule("/me", view_func=auth_controller.me, methods=["GET"])

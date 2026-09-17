from datetime import datetime
from flask import Blueprint, request, jsonify

from services.Auth import RegistrarUsuario, AutenticarUsuario, EncerrarSessao
from utils.auth import login_required

auth_bp = Blueprint("auth", __name__)


def formatar_data(data_str):
    if data_str:
        return datetime.strptime(data_str, "%Y-%m-%d").date()
    return None


class AuthController:
    """Controller de autenticação: recebe a requisição HTTP, interpreta os
    dados e delega a regra de negócio para o Service correspondente."""

    def registrar(self):
        dados = request.get_json()

        try:
            motorista = RegistrarUsuario().executar(
                nome=dados["nome"],
                cpf=dados["cpf"],
                cnh=dados["cnh"],
                email=dados["email"],
                senha=dados["senha"],
                telefone=dados.get("telefone"),
                data_nascimento=formatar_data(dados.get("data_nascimento")),
            )

            return jsonify({
                "token": motorista.token,
                "motorista": motorista.to_dict()
            }), 201

        except KeyError:
            return jsonify({"erro": "Campos obrigatórios não informados."}), 400
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

    def login(self):
        dados = request.get_json()

        try:
            motorista = AutenticarUsuario().executar(
                identificador=dados.get("identificador"),
                senha=dados.get("senha"),
            )

            return jsonify({
                "token": motorista.token,
                "motorista": motorista.to_dict()
            }), 200

        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 401

    @login_required
    def logout(self):
        resultado = EncerrarSessao().executar(request.motorista_atual)
        return jsonify(resultado), 200

    @login_required
    def me(self):
        return jsonify({"motorista": request.motorista_atual.to_dict()}), 200


auth_controller = AuthController()

auth_bp.add_url_rule("/registrar", view_func=auth_controller.registrar, methods=["POST"])
auth_bp.add_url_rule("/login", view_func=auth_controller.login, methods=["POST"])
auth_bp.add_url_rule("/logout", view_func=auth_controller.logout, methods=["POST"])
auth_bp.add_url_rule("/me", view_func=auth_controller.me, methods=["GET"])

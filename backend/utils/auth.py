from functools import wraps
from flask import request, jsonify

from models.motorista import Motorista
from repositories import MotoristaRepository


def _extrair_token():
    cabecalho = request.headers.get("Authorization", "")
    if cabecalho.startswith("Bearer "):
        return cabecalho[len("Bearer "):].strip()
    return None


def login_required(f):
    """Decorator que exige um token válido (Authorization: Bearer <token>).

    Usamos token em vez de sessão/cookie porque o frontend roda em outro
    servidor (porta 5500) que a API (porta 5000) — cookies cross-origin
    exigem configurações de SameSite/Secure frágeis entre navegadores
    diferentes, enquanto um header Authorization funciona de forma simples.
    """

    @wraps(f)
    def decorado(*args, **kwargs):
        token = _extrair_token()

        if not token:
            return jsonify({"erro": "Não autenticado."}), 401

        motorista_id = MotoristaRepository().buscar_id_por_token(token)
        motorista = Motorista.buscar_por_id(motorista_id)

        if motorista is None:
            return jsonify({"erro": "Sessão inválida ou expirada."}), 401

        request.motorista_atual = motorista
        return f(*args, **kwargs)

    return decorado

from datetime import datetime

from flask import jsonify, request
from flask.views import MethodView

from services.excecoes import RecursoNaoEncontrado


class BaseController(MethodView):
    """
    Superclasse dos Controllers (cada Controller é uma classe ligada a um
    recurso do sistema). O Controller só:
      1. recebe a requisição HTTP e interpreta os dados (JSON, URL);
      2. chama o Service do caso de uso;
      3. devolve a resposta JSON com o status HTTP certo.
    Regra de negócio fica no Service; acesso a dados, na Model/Repository.
    """

    @classmethod
    def registrar_rotas(cls, blueprint, nome):
        """Liga a classe às rotas padrão de um recurso:
          ""      -> GET (listar) e POST (cadastrar)
          /<id>   -> GET (consultar), PUT (editar) e DELETE (excluir)
        """
        view = cls.as_view(nome)
        blueprint.add_url_rule("", defaults={"id": None}, view_func=view, methods=["GET"])
        blueprint.add_url_rule("", view_func=view, methods=["POST"])
        blueprint.add_url_rule("/<int:id>", view_func=view, methods=["GET", "PUT", "DELETE"])
        return view

    @staticmethod
    def dados_json():
        """Corpo JSON da requisição (dicionário vazio se não vier JSON válido)."""
        dados = request.get_json(silent=True)
        return dados if isinstance(dados, dict) else {}

    @staticmethod
    def ler_data(texto):
        """Converte 'AAAA-MM-DD' em date (None se vier vazio)."""
        if not texto:
            return None
        try:
            return datetime.strptime(texto, "%Y-%m-%d").date()
        except (TypeError, ValueError):
            raise ValueError("Data inválida. Use o formato AAAA-MM-DD.")

    @staticmethod
    def ler_data_hora(texto):
        """Converte texto ISO (ex.: '2026-01-01T10:00:00') em datetime (None se vier vazio)."""
        if not texto:
            return None
        try:
            return datetime.fromisoformat(texto)
        except (TypeError, ValueError):
            raise ValueError("Data/hora inválida. Use o formato AAAA-MM-DDTHH:MM:SS.")

    @staticmethod
    def responder(dados, status=200):
        return jsonify(dados), status

    @staticmethod
    def responder_erro(erro):
        status = 404 if isinstance(erro, RecursoNaoEncontrado) else 400
        return jsonify({"erro": str(erro)}), status

from flask import Blueprint

from controllers.base_controller import BaseController
from services.Meta import (
    CriarMeta,
    ListarMetas,
    BuscarMeta,
    AtualizarMeta,
    ExcluirMeta,
)
from utils.auth import login_required

meta_bp = Blueprint("meta", __name__)


class MetaController(BaseController):
    """Controller do recurso Meta: recebe a requisição HTTP, interpreta
    os dados e delega a regra de negócio para o Service correspondente."""

    decorators = [login_required]

    def get(self, id=None):
        if id is None:
            metas = ListarMetas().executar()
            return self.responder([meta.to_dict() for meta in metas])

        try:
            return self.responder(BuscarMeta().executar(id).to_dict())
        except ValueError as erro:
            return self.responder_erro(erro)

    def post(self):
        dados = self.dados_json()

        try:
            nova_meta = CriarMeta().executar(
                valor_meta=dados.get("valor_meta"),
                data_fim=self.ler_data(dados.get("data_fim")),
                motorista_id=dados.get("motorista_id"),
                data_inicio=self.ler_data(dados.get("data_inicio")),
                concluida=dados.get("concluida", False),
            )
            return self.responder(nova_meta.to_dict(), 201)
        except ValueError as erro:
            return self.responder_erro(erro)

    def put(self, id):
        dados = self.dados_json()

        try:
            meta_atualizada = AtualizarMeta().executar(
                id=id,
                valor_meta=dados.get("valor_meta"),
                data_inicio=self.ler_data(dados.get("data_inicio")),
                data_fim=self.ler_data(dados.get("data_fim")),
                concluida=dados.get("concluida"),
                motorista_id=dados.get("motorista_id"),
            )
            return self.responder(meta_atualizada.to_dict())
        except ValueError as erro:
            return self.responder_erro(erro)

    def delete(self, id):
        try:
            return self.responder(ExcluirMeta().executar(id))
        except ValueError as erro:
            return self.responder_erro(erro)


MetaController.registrar_rotas(meta_bp, "meta_api")

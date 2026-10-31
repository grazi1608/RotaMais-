from .motorista_controller import motorista_bp
from .veiculo_controller import veiculo_bp
from .corrida_controller import corrida_bp
from .meta_controller import meta_bp
from .relatorio_controller import relatorio_bp
from .auth_controller import auth_bp
from .gasto_controller import gasto_bp
from .cofrinho_controller import cofrinho_bp

# (blueprint, prefixo da URL) — registrados no app.py
TODOS_OS_BLUEPRINTS = [
    (motorista_bp, "/motoristas"),
    (veiculo_bp, "/veiculos"),
    (corrida_bp, "/corridas"),
    (meta_bp, "/metas"),
    (relatorio_bp, "/relatorios"),
    (auth_bp, "/auth"),
    (gasto_bp, "/gastos"),
    (cofrinho_bp, "/cofrinho"),
]

__all__ = ["TODOS_OS_BLUEPRINTS"]

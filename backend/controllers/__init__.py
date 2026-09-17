from .motorista_controller import motorista_bp
from .veiculo_controller import veiculo_bp
from .corrida_controller import corrida_bp
from .meta_controller import meta_bp
from .relatorio_controller import relatorio_bp
from .auth_controller import auth_bp
from .gasto_controller import gasto_bp
from .cofrinho_controller import cofrinho_bp

__all__ = [
    "motorista_bp", "veiculo_bp", "corrida_bp", "meta_bp", "relatorio_bp",
    "auth_bp", "gasto_bp", "cofrinho_bp",
]

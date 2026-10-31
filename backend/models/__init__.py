from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Cada import abaixo registra a tabela da entidade no SQLAlchemy (usado pelo create_all).
from models.base import ModeloBase
from models.cadastro import Cadastro
from models.motorista import Motorista
from models.veiculo import Veiculo
from models.corrida import Corrida
from models.meta import Meta
from models.gasto import Gasto
from models.objetivo_cofrinho import ObjetivoCofrinho

__all__ = [
    "db", "ModeloBase", "Cadastro", "Motorista", "Veiculo",
    "Corrida", "Meta", "Gasto", "ObjetivoCofrinho",
]

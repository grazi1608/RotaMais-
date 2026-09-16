from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importamos os modelos para que o SQLAlchemy tome conhecimento deles
from models.corrida import Corrida
from models.meta import Meta
from models.motorista import Motorista
from models.veiculo import Veiculo
from models.gasto import Gasto
from models.objetivo_cofrinho import ObjetivoCofrinho
from models.base import ModeloBase
from models.cadastro import Cadastro

__all__ = ["db", "Corrida", "Meta", "Motorista", "Veiculo", "Gasto", "ObjetivoCofrinho", "ModeloBase", "Cadastro"]
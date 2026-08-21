from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importamos os modelos para que o SQLAlchemy tome conhecimento deles
from models.corrida import Corrida
from models.meta import Meta
from models.motorista import Motorista
from models.veiculo import Veiculo
from models.base import ModeloBase

__all__ = ["db", "Corrida", "Meta", "Motorista", "Veiculo", "ModeloBase"]
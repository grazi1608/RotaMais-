from models import db
from models.base import ModeloBase

class Motorista(ModeloBase):
    __tablename__ = "motoristas"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    cnh = db.Column(db.String(20), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)

    veiculos = db.relationship(
        "Veiculo",
        back_populates="motorista",
        cascade="all, delete-orphan"
    )
    corridas = db.relationship(
        "Corrida",
        back_populates="motorista",
        cascade="all, delete-orphan"
    )
    metas = db.relationship(
        "Meta",
        back_populates="motorista",
        cascade="all, delete-orphan"
    )

    
    def __init__(self, nome, cpf, cnh, telefone=None, email=None):
        self.nome = nome
        self.cpf = cpf
        self.cnh = cnh
        self.telefone = telefone
        self.email = email
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "cnh": self.cnh,
            "telefone": self.telefone,
            "email": self.email
        }

    def __repr__(self):
        return f"<Motorista {self.nome}>"
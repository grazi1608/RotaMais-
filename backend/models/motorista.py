from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

from models import db
from models.base import ModeloBase
from models.cadastro import Cadastro

class Motorista(Cadastro, ModeloBase):
    __tablename__ = "motoristas"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    cnh = db.Column(db.String(20), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    senha_hash = db.Column(db.String(255))
    token = db.Column(db.String(64), unique=True, nullable=True)

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
    gastos = db.relationship(
        "Gasto",
        back_populates="motorista",
        cascade="all, delete-orphan"
    )
    objetivos_cofrinho = db.relationship(
        "ObjetivoCofrinho",
        back_populates="motorista",
        cascade="all, delete-orphan"
    )

    
    def __init__(self, nome, cpf, cnh, telefone=None, email=None, data_nascimento=None):
        self.nome = nome
        self.cpf = cpf
        self.cnh = cnh
        self.telefone = telefone
        self.email = email
        self.data_nascimento = data_nascimento

    def definir_senha(self, senha):
        """Gera e armazena o hash da senha (nunca a senha em texto puro)."""
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        """Confere se a senha informada bate com o hash armazenado."""
        if not self.senha_hash:
            return False
        return check_password_hash(self.senha_hash, senha)

    def gerar_token(self):
        """Gera um novo token de sessão (usado no login em vez de cookie,
        para não depender de cookies entre origens diferentes)."""
        self.token = secrets.token_hex(32)
        return self.token

    def revogar_token(self):
        """Invalida o token atual (logout)."""
        self.token = None

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "cnh": self.cnh,
            "telefone": self.telefone,
            "email": self.email,
            "data_nascimento": self.data_nascimento.strftime("%Y-%m-%d") if self.data_nascimento else None,
            "data_cadastro": self.data_cadastro.strftime("%Y-%m-%d") if self.data_cadastro else None
        }

    def __repr__(self):
        return f"<Motorista {self.nome}>"
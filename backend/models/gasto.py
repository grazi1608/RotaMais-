from datetime import datetime

from models import db
from models.base import ModeloBase


class Gasto(ModeloBase):
    """Gasto avulso do motorista (combustível, manutenção, etc.),
    separado do custo estimado calculado automaticamente por corrida."""

    __tablename__ = "gastos"

    TIPOS_VALIDOS = ("combustivel", "manutencao", "outro")

    tipo = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.String(255))
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.now)
    motorista_id = db.Column(
        db.Integer, db.ForeignKey("motoristas.id", ondelete="CASCADE"), nullable=False
    )
    veiculo_id = db.Column(db.Integer, db.ForeignKey("veiculos.id", ondelete="SET NULL"))

    motorista = db.relationship("Motorista", back_populates="gastos")
    veiculo = db.relationship("Veiculo", back_populates="gastos")

    def __init__(self, tipo, valor, motorista_id, descricao=None, veiculo_id=None, data=None):
        self.tipo = tipo
        self.valor = valor
        self.motorista_id = motorista_id
        self.descricao = descricao
        self.veiculo_id = veiculo_id
        self.data = data or datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "descricao": self.descricao,
            "valor": self.valor,
            "data": self.data.strftime("%Y-%m-%dT%H:%M:%S") if self.data else None,
            "motorista_id": self.motorista_id,
            "veiculo_id": self.veiculo_id,
        }

    def __repr__(self):
        return f"<Gasto {self.tipo} R${self.valor}>"

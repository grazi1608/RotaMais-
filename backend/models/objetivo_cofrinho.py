from models import db
from models.base import ModeloBase


class ObjetivoCofrinho(ModeloBase):
    """Objetivo de economia do "cofrinho" (ex.: trocar pneus, IPVA),
    diferente da Meta de lucro — aqui o motorista guarda dinheiro aos poucos
    até atingir o valor do objetivo."""

    __tablename__ = "objetivos_cofrinho"

    nome = db.Column(db.String(120), nullable=False)
    valor_meta = db.Column(db.Float, nullable=False)
    valor_guardado = db.Column(db.Float, nullable=False, default=0)
    motorista_id = db.Column(
        db.Integer, db.ForeignKey("motoristas.id", ondelete="CASCADE"), nullable=False
    )

    motorista = db.relationship("Motorista", back_populates="objetivos_cofrinho")

    def __init__(self, nome, valor_meta, motorista_id, valor_guardado=0):
        self.nome = nome
        self.valor_meta = valor_meta
        self.motorista_id = motorista_id
        self.valor_guardado = valor_guardado or 0

    def guardar(self, valor):
        """Soma um valor ao total já guardado neste objetivo."""
        self.valor_guardado = (self.valor_guardado or 0) + valor

    @staticmethod
    def calcular_progresso(valor_guardado, valor_meta):
        """Percentual (0 a 100) do valor guardado em relação à meta."""
        if not valor_meta:
            return 0
        return min(round(((valor_guardado or 0) / valor_meta) * 100), 100)

    def progresso(self):
        return self.calcular_progresso(self.valor_guardado, self.valor_meta)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "valor_meta": self.valor_meta,
            "valor_guardado": self.valor_guardado,
            "progresso": self.progresso(),
            "motorista_id": self.motorista_id,
        }

    def __repr__(self):
        return f"<ObjetivoCofrinho {self.nome}>"

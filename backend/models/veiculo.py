from models import db
from models.base import ModeloBase


class Veiculo(ModeloBase):
    __tablename__ = "veiculos"

    placa = db.Column(db.String(10), unique=True, nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    consumo_por_km = db.Column(db.Float, nullable=False)
    motorista_id = db.Column(
        db.Integer, db.ForeignKey("motoristas.id", ondelete="CASCADE"), nullable=False
    )

    motorista = db.relationship("Motorista", back_populates="veiculos")
    # Composição: as corridas feitas com o veículo saem junto com ele.
    corridas = db.relationship("Corrida", back_populates="veiculo", cascade="all, delete-orphan")
    # Agregação: o gasto continua existindo sem o veículo (veiculo_id vira NULL).
    gastos = db.relationship("Gasto", back_populates="veiculo")

    def __init__(self, placa, modelo, consumo_por_km, motorista_id):
        self.placa = placa.upper()
        self.modelo = modelo
        self.consumo_por_km = consumo_por_km
        self.motorista_id = motorista_id

    def to_dict(self):
        return {
            "id": self.id,
            "placa": self.placa,
            "modelo": self.modelo,
            "consumo_por_km": self.consumo_por_km,
            "motorista_id": self.motorista_id
        }

    def __repr__(self):
        return f"<Veiculo {self.placa}>"

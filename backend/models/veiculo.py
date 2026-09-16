from models import db
from models.base import ModeloBase

class Veiculo(ModeloBase):
    __tablename__ = "veiculos"

    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(8), unique=True, nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    consumo_por_km = db.Column(db.Float, nullable=False)

    motorista_id = db.Column(
        db.Integer,
        db.ForeignKey("motoristas.id"),
        nullable=False
    )
    motorista = db.relationship(
        "Motorista",
        back_populates="veiculos"
        
    )
    corridas = db.relationship(
        "Corrida",
        back_populates="veiculo",
        cascade="all, delete-orphan"
    )

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
from datetime import datetime
from models import db
from models.base import ModeloBase


class Corrida(ModeloBase):
    __tablename__ = "corridas"

    id = db.Column(db.Integer, primary_key=True)

    data_hora = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    valor = db.Column(db.Float, nullable=False)
    custo_estimado = db.Column(db.Float, nullable=False)
    lucro = db.Column(db.Float, nullable=False)
    distancia = db.Column(db.Float, nullable=False)

    motorista_id = db.Column(
        db.Integer,
        db.ForeignKey("motoristas.id"),
        nullable=False
    )
    veiculo_id = db.Column(
        db.Integer,
        db.ForeignKey("veiculos.id"),
        nullable=False
    )
    motorista = db.relationship(
        "Motorista",
        back_populates="corridas"
    )
    veiculo = db.relationship(
        "Veiculo",
        back_populates="corridas"
    )

    def __init__(
        self,
        valor,
        custo_estimado,
        lucro,
        distancia,
        motorista_id,
        veiculo_id,
        data_hora=None
    ):
        self.valor = valor
        self.custo_estimado = custo_estimado
        self.lucro = lucro
        self.distancia = distancia
        self.motorista_id = motorista_id
        self.veiculo_id = veiculo_id

        if data_hora:
            self.data_hora = data_hora

    def to_dict(self):
        return {
            "id": self.id,
            "data_hora": self.data_hora.strftime("%d/%m/%Y %H:%M"),
            "valor": self.valor,
            "custo_estimado": self.custo_estimado,
            "lucro": self.lucro,
            "distancia": self.distancia,
            "motorista_id": self.motorista_id,
            "veiculo_id": self.veiculo_id
        }

    def __repr__(self):
        return f"<Corrida {self.id}>"
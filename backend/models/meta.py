from datetime import date
from models import db
from models.base import ModeloBase

class Meta(ModeloBase):
    __tablename__ = "metas"

    id = db.Column(db.Integer, primary_key=True)
    valor_meta = db.Column(db.Float, nullable=False)

    data_inicio = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )
    data_fim = db.Column(
        db.Date,
        nullable=False
    )
    concluida = db.Column(
        db.Boolean,
        default=False
    )
    motorista_id = db.Column(
        db.Integer,
        db.ForeignKey("motoristas.id"),
        nullable=False
    )
    motorista = db.relationship(
        "Motorista",
        back_populates="metas"
    )

    def __init__(
        self,
        valor_meta,
        data_fim,
        motorista_id,
        data_inicio=None,
        concluida=False
    ):
        self.valor_meta = valor_meta
        self.data_fim = data_fim
        self.motorista_id = motorista_id
        self.concluida = concluida

        if data_inicio:
            self.data_inicio = data_inicio

    def to_dict(self):
        return {
            "id": self.id,
            "valor_meta": self.valor_meta,
            "data_inicio": self.data_inicio.strftime("%d/%m/%Y"),
            "data_fim": self.data_fim.strftime("%d/%m/%Y"),
            "concluida": self.concluida,
            "motorista_id": self.motorista_id
        }

    def __repr__(self):
        return f"<Meta {self.id}>"
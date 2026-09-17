from datetime import datetime
from models import db


class Cadastro:
    """Mixin com o campo comum de data de cadastro — quando o registro foi
    criado no sistema. Não herda de db.Model (não é uma tabela sozinha);
    é combinada com ModeloBase pelas classes que precisam desse campo,
    como Motorista.
    """

    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

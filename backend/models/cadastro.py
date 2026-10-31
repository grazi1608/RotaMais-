from datetime import datetime

from models import db


class Cadastro:
    """Mixin com o campo comum de data de cadastro — quando o registro foi
    criado no sistema. Não é uma tabela sozinha; é combinada com ModeloBase
    pelas classes que precisam desse campo, como Motorista (a coluna fica na
    tabela da classe filha).
    """

    data_cadastro = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def registrar_data_cadastro(self):
        self.data_cadastro = datetime.now()

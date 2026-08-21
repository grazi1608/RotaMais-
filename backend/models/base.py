from . import db


class ModeloBase(db.Model):
    """
    Superclasse abstrata — não vira tabela no banco.
    Todas as classes herdam só o id; quem precisar de data de criação
    declara essa coluna na própria classe (Simulado e Resultado, por agora).

    Concentra aqui as operações básicas de persistência (salvar, atualizar,
    deletar, listar_todos, buscar_por_id) para que os Services não precisem
    manipular db.session diretamente — eles chamam esses métodos da Model.
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def salvar(self):
        """Adiciona (se novo) e confirma o registro no banco."""
        db.session.add(self)
        db.session.commit()
        return self

    def atualizar(self, **campos):
        """Atualiza os atributos informados e confirma no banco."""
        for chave, valor in campos.items():
            if valor is not None and hasattr(self, chave):
                setattr(self, chave, valor)

        db.session.commit()
        return self

    def deletar(self):
        """Remove o registro do banco."""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def listar_todos(cls):
        """Retorna todos os registros da tabela."""
        return cls.query.all()

    @classmethod
    def buscar_por_id(cls, id):
        """Busca um registro pelo id, ou None se não existir."""
        return cls.query.get(id)

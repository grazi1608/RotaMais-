from models import db


class ModeloBase(db.Model):
    """
    Superclasse de todas as Models (__abstract__: o SQLAlchemy não cria uma
    tabela para ela).

    Aqui fica o CRUD convencional feito com o ORM (salvar, atualizar,
    deletar, listar_todos, buscar_por_id). Os Services chamam esses métodos
    e nunca mexem na sessão do banco. Filtros específicos e relatórios ficam
    nos Repositories, em SQL escrito.
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    @staticmethod
    def _confirmar():
        db.session.commit()

    def salvar(self):
        """Grava um registro novo (INSERT) e devolve o próprio objeto."""
        db.session.add(self)
        self._confirmar()
        return self

    def atualizar(self, **campos):
        """UPDATE com os valores atuais do objeto (opcionalmente alterando antes
        os campos informados; valores None são ignorados)."""
        for chave, valor in campos.items():
            if valor is not None and chave in self.__table__.columns:
                setattr(self, chave, valor)

        self._confirmar()
        return self

    def deletar(self):
        """DELETE do registro (os dependentes saem junto pelo cascade dos relacionamentos)."""
        db.session.delete(self)
        self._confirmar()

    @classmethod
    def listar_todos(cls):
        """Todos os registros da tabela, em ordem de id."""
        return db.session.scalars(db.select(cls).order_by(cls.id)).all()

    @classmethod
    def buscar_por_id(cls, id):
        """O registro com esse id, ou None se não existir."""
        if id is None:
            return None
        return db.session.get(cls, id)

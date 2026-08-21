from models.motorista import Motorista


class CriarMotorista:
    """Caso de uso: cadastrar um novo motorista."""

    def executar(self, nome, cpf, cnh, telefone=None, email=None):
        if Motorista.query.filter_by(cpf=cpf).first():
            raise ValueError("Já existe um motorista com esse CPF.")

        if Motorista.query.filter_by(cnh=cnh).first():
            raise ValueError("Já existe um motorista com essa CNH.")

        if email and Motorista.query.filter_by(email=email).first():
            raise ValueError("Já existe um motorista com esse e-mail.")

        novo_motorista = Motorista(
            nome=nome,
            cpf=cpf,
            cnh=cnh,
            telefone=telefone,
            email=email
        )

        return novo_motorista.salvar()

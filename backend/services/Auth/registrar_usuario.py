from models.motorista import Motorista


class RegistrarUsuario:
    """Caso de uso: criar a conta de acesso (e-mail + senha) de um motorista.

    Cadastra o motorista e já devolve um token de sessão (equivalente a
    logá-lo automaticamente após o cadastro).
    """

    def executar(self, nome, cpf, cnh, email, senha, telefone=None, data_nascimento=None):
        if not email or not senha:
            raise ValueError("E-mail e senha são obrigatórios.")

        if Motorista.query.filter_by(email=email).first():
            raise ValueError("Já existe uma conta com esse e-mail.")

        if Motorista.query.filter_by(cpf=cpf).first():
            raise ValueError("Já existe um motorista com esse CPF.")

        if Motorista.query.filter_by(cnh=cnh).first():
            raise ValueError("Já existe um motorista com essa CNH.")

        motorista = Motorista(
            nome=nome,
            cpf=cpf,
            cnh=cnh,
            telefone=telefone,
            email=email,
            data_nascimento=data_nascimento
        )
        motorista.definir_senha(senha)
        motorista.gerar_token()

        return motorista.salvar()

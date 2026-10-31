from models.motorista import Motorista
from repositories import MotoristaRepository
from services.validacoes import exigir_texto


class RegistrarUsuario:
    """Caso de uso: criar a conta de acesso (e-mail + senha) de um motorista.

    Cadastra o motorista e já devolve um token de sessão (equivalente a
    logá-lo automaticamente após o cadastro).
    """

    def __init__(self):
        self.repositorio = MotoristaRepository()

    def executar(self, nome, cpf, cnh, email, senha, telefone=None, data_nascimento=None):
        nome = exigir_texto(nome, "Informe o nome.")
        cpf = exigir_texto(cpf, "Informe o CPF.")
        cnh = exigir_texto(cnh, "Informe a CNH.")
        email = (email or "").strip().lower()
        telefone = (telefone or "").strip() or None

        if not email or not senha:
            raise ValueError("E-mail e senha são obrigatórios.")

        if self.repositorio.buscar_id_por_email(email):
            raise ValueError("Já existe uma conta com esse e-mail.")

        if self.repositorio.buscar_id_por_cpf(cpf):
            raise ValueError("Já existe um motorista com esse CPF.")

        if self.repositorio.buscar_id_por_cnh(cnh):
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

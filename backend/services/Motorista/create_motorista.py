from models.motorista import Motorista
from repositories import MotoristaRepository
from services.validacoes import exigir_texto


class CriarMotorista:
    """Caso de uso: cadastrar um novo motorista."""

    def __init__(self):
        self.repositorio = MotoristaRepository()

    def executar(self, nome, cpf, cnh, telefone=None, email=None):
        nome = exigir_texto(nome, "Informe o nome.")
        cpf = exigir_texto(cpf, "Informe o CPF.")
        cnh = exigir_texto(cnh, "Informe a CNH.")
        # Campos opcionais vazios viram NULL (senão dois "" violam o UNIQUE do e-mail).
        telefone = (telefone or "").strip() or None
        email = (email or "").strip().lower() or None

        if self.repositorio.buscar_id_por_cpf(cpf):
            raise ValueError("Já existe um motorista com esse CPF.")

        if self.repositorio.buscar_id_por_cnh(cnh):
            raise ValueError("Já existe um motorista com essa CNH.")

        if email and self.repositorio.buscar_id_por_email(email):
            raise ValueError("Já existe um motorista com esse e-mail.")

        novo_motorista = Motorista(
            nome=nome,
            cpf=cpf,
            cnh=cnh,
            telefone=telefone,
            email=email
        )

        return novo_motorista.salvar()

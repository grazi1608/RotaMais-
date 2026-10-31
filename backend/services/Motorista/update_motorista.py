from models.motorista import Motorista
from repositories import MotoristaRepository
from services.excecoes import RecursoNaoEncontrado
from services.validacoes import exigir_texto


class AtualizarMotorista:
    """Caso de uso: atualizar os dados de um motorista existente."""

    def __init__(self):
        self.repositorio = MotoristaRepository()

    def executar(self, id, nome, cpf, cnh, telefone=None, email=None):
        motorista = Motorista.buscar_por_id(id)

        if motorista is None:
            raise RecursoNaoEncontrado("Motorista não encontrado.")

        nome = exigir_texto(nome, "Informe o nome.")
        cpf = exigir_texto(cpf, "Informe o CPF.")
        cnh = exigir_texto(cnh, "Informe a CNH.")
        telefone = (telefone or "").strip() or None
        email = (email or "").strip().lower() or None

        id_cpf = self.repositorio.buscar_id_por_cpf(cpf)
        if id_cpf and id_cpf != id:
            raise ValueError("Já existe um motorista com esse CPF.")

        id_cnh = self.repositorio.buscar_id_por_cnh(cnh)
        if id_cnh and id_cnh != id:
            raise ValueError("Já existe um motorista com essa CNH.")

        if email:
            id_email = self.repositorio.buscar_id_por_email(email)
            if id_email and id_email != id:
                raise ValueError("Já existe um motorista com esse e-mail.")

        motorista.nome = nome
        motorista.cpf = cpf
        motorista.cnh = cnh
        motorista.telefone = telefone
        motorista.email = email

        return motorista.atualizar()

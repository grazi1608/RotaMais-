from models.motorista import Motorista


class AtualizarMotorista:
    """Caso de uso: atualizar os dados de um motorista existente."""

    def executar(self, id, nome, cpf, cnh, telefone=None, email=None):
        motorista = Motorista.buscar_por_id(id)

        if motorista is None:
            raise ValueError("Motorista não encontrado.")

        motorista_cpf = Motorista.query.filter_by(cpf=cpf).first()
        if motorista_cpf and motorista_cpf.id != id:
            raise ValueError("Já existe um motorista com esse CPF.")

        motorista_cnh = Motorista.query.filter_by(cnh=cnh).first()
        if motorista_cnh and motorista_cnh.id != id:
            raise ValueError("Já existe um motorista com essa CNH.")

        if email:
            motorista_email = Motorista.query.filter_by(email=email).first()
            if motorista_email and motorista_email.id != id:
                raise ValueError("Já existe um motorista com esse e-mail.")

        motorista.nome = nome
        motorista.cpf = cpf
        motorista.cnh = cnh
        motorista.telefone = telefone
        motorista.email = email

        return motorista.atualizar()

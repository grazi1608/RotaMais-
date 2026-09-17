from models.motorista import Motorista


class AutenticarUsuario:
    """Caso de uso: autenticar um motorista pelo e-mail/telefone e senha,
    gerando um novo token de sessão."""

    def executar(self, identificador, senha):
        if not identificador or not senha:
            raise ValueError("Informe e-mail/telefone e senha.")

        motorista = Motorista.query.filter(
            (Motorista.email == identificador) | (Motorista.telefone == identificador)
        ).first()

        if motorista is None or not motorista.verificar_senha(senha):
            raise ValueError("Credenciais inválidas.")

        motorista.gerar_token()
        motorista.atualizar()

        return motorista

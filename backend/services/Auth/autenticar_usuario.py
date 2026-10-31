from models.motorista import Motorista
from repositories import MotoristaRepository


class AutenticarUsuario:
    """Caso de uso: autenticar um motorista pelo e-mail/telefone e senha,
    gerando um novo token de sessão."""

    def __init__(self):
        self.repositorio = MotoristaRepository()

    def executar(self, identificador, senha):
        identificador = (identificador or "").strip()

        if not identificador or not senha:
            raise ValueError("Informe e-mail/telefone e senha.")

        motorista_id = self.repositorio.buscar_id_por_email_ou_telefone(identificador)
        motorista = Motorista.buscar_por_id(motorista_id)

        # Mensagem genérica de propósito: não revela se o e-mail existe.
        if motorista is None or not motorista.verificar_senha(senha):
            raise ValueError("Credenciais inválidas.")

        motorista.gerar_token()
        motorista.atualizar()

        return motorista

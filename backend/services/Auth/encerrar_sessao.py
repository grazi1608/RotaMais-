class EncerrarSessao:
    """Caso de uso: encerrar a sessão do motorista (logout), invalidando o token."""

    def executar(self, motorista):
        motorista.revogar_token()
        motorista.atualizar()
        return {"mensagem": "Sessão encerrada com sucesso."}

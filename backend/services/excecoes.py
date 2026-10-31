"""
Erros de regra de negócio lançados pelos Services.

O Controller só traduz cada tipo de erro para o status HTTP certo:
  - ValueError           -> 400 (dados inválidos / regra violada)
  - RecursoNaoEncontrado -> 404 (o registro não existe ou não é do motorista logado)
"""


class RecursoNaoEncontrado(ValueError):
    pass

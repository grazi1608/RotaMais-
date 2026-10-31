"""Validações de entrada reaproveitadas pelos Services."""

import math


def exigir_texto(valor, mensagem):
    """Devolve o texto sem espaços nas pontas; erro se vier vazio."""
    texto = str(valor).strip() if valor is not None else ""
    if not texto:
        raise ValueError(mensagem)
    return texto


def exigir_numero_positivo(valor, mensagem):
    """Devolve o valor como float; erro se não for um número maior que zero."""
    if valor is None or isinstance(valor, bool):
        raise ValueError(mensagem)

    try:
        numero = float(valor)
    except (TypeError, ValueError):
        raise ValueError(mensagem)

    if not math.isfinite(numero) or numero <= 0:
        raise ValueError(mensagem)

    return numero

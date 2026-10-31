from datetime import date, datetime


def para_datetime(valor):
    """Converte o valor lido por SQL escrito (texto no SQLite) em datetime."""
    if valor is None or isinstance(valor, datetime):
        return valor
    if isinstance(valor, date):
        return datetime(valor.year, valor.month, valor.day)
    return datetime.fromisoformat(str(valor))

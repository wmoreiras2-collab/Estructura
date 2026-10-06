"""Funciones de validación reutilizables (PROCESO 2)."""

NOTA_MINIMA = 0
NOTA_MAXIMA = 20


def es_email_valido(texto):
    # Validación mínima: un @, algo antes, algo después y un punto en el dominio
    texto = str(texto).strip()
    if texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    return len(usuario) > 0 and "." in dominio and not dominio.startswith(".") \
        and not dominio.endswith(".")


def es_carnet_valido(texto):
    # Solo letras y números, sin espacios (ej: EST2026001)
    texto = str(texto).strip()
    return len(texto) >= 4 and texto.isalnum()


def convertir_entero(valor):
    """Devuelve un int o None si no se puede convertir."""
    try:
        return int(str(valor).strip())
    except ValueError:
        return None


def convertir_numero(valor):
    """Devuelve un float o None. Acepta coma decimal: '18,5'."""
    try:
        numero = float(str(valor).strip().replace(",", "."))
    except ValueError:
        return None
    # float('nan') e 'inf' se convierten sin error, pero no son notas
    if numero != numero or numero in (float("inf"), float("-inf")):
        return None
    return numero


def es_nota_valida(numero):
    return numero is not None and NOTA_MINIMA <= numero <= NOTA_MAXIMA

from babel.numbers import format_currency, format_decimal, format_percent

LANGUAGE = "pt_BR"
CURRENCY = "BRL"


def real_brasileiro(valor: float) -> str:
    return format_currency(valor, CURRENCY, locale=LANGUAGE)


def numero_brasileiro(valor: float) -> str:
    return format_decimal(valor, locale=LANGUAGE)


def porcentagem_brasileira(valor: float, casas_decimais: int = 1) -> str:
    formato = f"#{'#' * 3},##0.{'0' * casas_decimais}%"
    return format_percent(valor, locale=LANGUAGE, format=formato)

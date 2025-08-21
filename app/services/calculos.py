import pandas as pd
import calendar
from pathlib import Path
import json

config_path = Path("data/configuracoes.json")

with config_path.open("r", encoding="utf-8") as f:
    CONFIG = json.load(f)


def receitas_despesas_saldo(df):
    df = df.copy()
    receitas = df[df["natureza"] == "Ganhos"]["valor"].sum()
    despesas = df[df["natureza"] == "Gastos"]["valor"].sum()
    saldo = receitas + despesas
    return receitas, despesas, saldo


def mes_fatura(row):
    dia_compra = row["data"].day
    fechamento = 12

    # Ajusta mês e ano
    if dia_compra >= fechamento:
        mes = row["data"].month + 1
        ano = row["data"].year
        if mes > 12:
            mes = 1
            ano += 1
    else:
        mes = row["data"].month
        ano = row["data"].year

    # Ajusta o dia para não ultrapassar o último dia do mês
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    dia = min(dia_compra, ultimo_dia)

    return pd.Timestamp(year=ano, month=mes, day=dia)


def ajuste_datas_colunas(df):
    df = df.copy()
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["data_fatura"] = df.apply(mes_fatura, axis=1)
    df["ano_mes_fatura_num"] = df["data_fatura"].dt.to_period("M")
    df["ano_mes_fatura"] = df["data_fatura"].dt.strftime("%b/%Y")
    df["ano_mes"] = df["data"].dt.to_period("M").dt.to_timestamp()
    return df


def taxa_mes_para_ano(taxa_mes):
    taxa_ano = (1 + taxa_mes / 100) ** 12 - 1
    return taxa_ano


def calcular_data_fatura(df, banco="BTG"):
    """
    Calcula o status da fatura com base nas movimentações do DataFrame.

    Parâmetros:
        df (pd.DataFrame): deve conter pelo menos as colunas 'data' e 'natureza'.
        banco (str): chave para buscar a data de fechamento em CONFIG["fechamento_fatura"].

    Retorna:
        str: status da fatura (paga, em aberto ou em atraso).
    """

    hoje = pd.Timestamp.today().normalize()
    ano_atual, mes_atual = hoje.year, hoje.month

    dia_fechamento = CONFIG["fechamento_fatura"].get(banco)
    if dia_fechamento is None:
        return f"Banco '{banco}' não encontrado na configuração."

    data_fechamento = pd.Timestamp(year=ano_atual, month=mes_atual, day=dia_fechamento)

    df = df.copy()
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # Fatura paga neste mês
    fatura_paga = df.loc[
        (df["data"].dt.year == ano_atual)
        & (df["data"].dt.month == mes_atual)
        & (df["natureza"] == "Pag.Fatura"),
        "data",
    ]

    dias_faltando = (data_fechamento - hoje).days

    if not fatura_paga.empty:
        data_pagamento = fatura_paga.min().strftime("%d/%m/%Y")
        return f"✅ Fatura paga em {data_pagamento}"

    if dias_faltando > 0:
        return f"⌛ Fatura não paga — faltam {dias_faltando} dias para fechar ({data_fechamento.strftime('%d/%m/%Y')})"

    return f"⚠️ Fatura em atraso há {abs(dias_faltando)} dias (vencimento {data_fechamento.strftime('%d/%m/%Y')})"

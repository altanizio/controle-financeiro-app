import pandas as pd
import calendar


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

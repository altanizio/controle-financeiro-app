import streamlit as st
from services.calculos import receitas_despesas_saldo
from utils.formatar_textos import real_brasileiro


import unicodedata
import re


def normalize_text(text):
    text = (
        unicodedata.normalize("NFKD", str(text))
        .encode("ASCII", "ignore")
        .decode("utf-8")
    )
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def exibir_cartao_inicial(df):
    receitas, despesas, saldo = receitas_despesas_saldo(df)

    col1, col2, col3 = st.columns(3, border=False)
    col1.metric("Receitas", real_brasileiro(receitas))
    col2.metric("Despesas", real_brasileiro(despesas))
    col3.metric("Saldo", real_brasileiro(saldo))


def exibir_n_linhas_df(df):
    col1, col2 = st.columns(2, border=False)

    with col1:
        n_linhas = st.selectbox(
            "Número de linhas (últimas)", [5, 10, 15, "Todas"], index=0
        )
    with col2:
        search = st.text_input("Procurar:")

    rename_col_map = {
        "id": "ID",
        "data": "Data",
        "hora": "Hora",
        "natureza": "Natureza",
        "valor": "Valor",
        "tipo": "Tipo",
        "obs": "Observações",
        "modo_pag": "Método de Pag./Receb.",
        "banco": "Banco",
        "comprovante": "Comprovante",
    }

    df_ajust = df.rename(columns=rename_col_map)

    df_ajust["Valor"] = df_ajust["Valor"].apply(real_brasileiro)

    if search:
        search_norm = normalize_text(search)
        df_ajust = df_ajust[
            df_ajust.apply(
                lambda row: search_norm in normalize_text(row.astype(str).to_string()),
                axis=1,
            )
        ]

    if n_linhas == "Todas":
        st.dataframe(df_ajust, use_container_width=True)
    else:
        st.dataframe(df_ajust.tail(int(n_linhas)), use_container_width=True)

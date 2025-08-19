import streamlit as st
from datetime import date
import pandas as pd


def aplicar_filtros(df, visao_geral=False):
    if df.empty:
        return df

    if df["data"].dtype == "O":
        df["data"] = pd.to_datetime(df["data"], errors="coerce").dt.date

    st.sidebar.markdown("### 🔎 Filtros")

    # Filtro por ano
    anos_unicos = sorted(df["data"].apply(lambda x: x.year).unique())
    anos_extenso = ["Todos", "Ano atual"] + [str(ano) for ano in anos_unicos]
    if visao_geral:
        ano_selecionado = st.sidebar.selectbox("Filtrar por ano", anos_extenso, index=1)
    else:
        ano_selecionado = st.sidebar.selectbox("Filtrar por ano", anos_extenso, index=0)

    hoje = date.today()
    meses_extenso = [
        "Todos",
        "Mês atual",
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]
    mes_selecionado = st.sidebar.selectbox("Filtrar por mês", meses_extenso, index=0)

    data_inicio, data_fim = st.sidebar.date_input(
        "Período", [df["data"].min(), df["data"].max()]
    )

    naturezas = st.sidebar.multiselect(
        "Natureza", df["natureza"].unique(), default=df["natureza"].unique()
    )
    modo = st.sidebar.multiselect(
        "Modo", df["modo_pag"].unique(), default=df["modo_pag"].unique()
    )
    bancos = st.sidebar.multiselect(
        "Banco", df["banco"].unique(), default=df["banco"].unique()
    )
    tipos = st.sidebar.multiselect(
        "Tipo", df["tipo"].unique(), default=df["tipo"].unique()
    )

    df_filtrado = df[
        (df["tipo"].isin(tipos))
        & (df["data"] >= data_inicio)
        & (df["data"] <= data_fim)
        & (df["banco"].isin(bancos))
        & (df["modo_pag"].isin(modo))
        & (df["natureza"].isin(naturezas))
    ]

    if mes_selecionado == "Mês atual":
        df_filtrado = df_filtrado[
            df_filtrado["data"].apply(lambda x: x.month == hoje.month)
        ]
    elif mes_selecionado != "Todos":
        meses_dict = {
            "Janeiro": 1,
            "Fevereiro": 2,
            "Março": 3,
            "Abril": 4,
            "Maio": 5,
            "Junho": 6,
            "Julho": 7,
            "Agosto": 8,
            "Setembro": 9,
            "Outubro": 10,
            "Novembro": 11,
            "Dezembro": 12,
        }
        mes_int = meses_dict[mes_selecionado]
        df_filtrado = df_filtrado[
            df_filtrado["data"].apply(lambda x: x.month == mes_int)
        ]

    if ano_selecionado == "Ano atual":
        df_filtrado = df_filtrado[
            df_filtrado["data"].apply(lambda x: x.year == hoje.year)
        ]
    elif ano_selecionado != "Todos":
        ano_int = int(ano_selecionado)
        df_filtrado = df_filtrado[
            df_filtrado["data"].apply(lambda x: x.year == ano_int)
        ]

    return df_filtrado

import streamlit as st
from pathlib import Path
from storage.database import connect_db, init_db
from services.filtros import aplicar_filtros
import locale
from components.tables_cards import exibir_cartao_inicial
from components.charts import (
    exibir_grafico_cartao_credito,
    exibir_grafico_ganhos_gastos,
    exibir_grafico_bancos,
    exibir_ganhos_gastos_tipo,
)
from services.calculos import ajuste_datas_colunas
from utils.calculadora import calculadora

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

DB_PATH = Path("data/orcamento.db")

init_db(DB_PATH)

st.set_page_config(page_title="Transações", page_icon="📥", layout="wide")

# Remover margem
st.markdown(
    """
    <style>
    header.stAppHeader {
        background-color: transparent;
    }
    section.stMain .block-container {
        padding-top: 0rem;
        z-index: 1;
    }
    </style>""",
    unsafe_allow_html=True,
)

df_original = connect_db(DB_PATH)
df = aplicar_filtros(df_original)

if not df.empty:
    df = ajuste_datas_colunas(df)

    exibir_cartao_inicial(df)

    left, right = st.columns(2)

    with left:
        exibir_ganhos_gastos_tipo(df)
        exibir_grafico_ganhos_gastos(df)
    with right:
        exibir_grafico_cartao_credito(df)
        exibir_grafico_bancos(df_original)

else:
    st.info("Sem dados.")

# Calculadora na barra lateral
calculadora()

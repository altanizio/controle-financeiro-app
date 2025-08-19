import streamlit as st
from pathlib import Path
from services.importacao import importar_dados_excel
from services.exportacao import to_excel
from storage.database import connect_db
from services.filtros import aplicar_filtros
from services.transacoes import (
    formulario_adicionar_transacao,
    formulario_remover_transacao,
    formulario_modificar_transacao,
    formulario_transferencia_transacao,
)
from components.tables_cards import exibir_cartao_inicial, exibir_n_linhas_df
from utils.calculadora import calculadora

DB_PATH = Path("data/orcamento.db")

st.set_page_config(page_title="Transações", page_icon="📥", layout="wide")

st.header("Resumo")


def df_transacoes_conf():
    df = connect_db(DB_PATH)
    df = aplicar_filtros(df)
    return df


df = df_transacoes_conf()

exibir_cartao_inicial(df)

exibir_n_linhas_df(df)

st.header("Operações")

left, center, right = st.columns(3, border=True)

with left:
    formulario_adicionar_transacao()
with center:
    if df.empty:
        st.info("Sem dados para modificar.")
    else:
        formulario_modificar_transacao(df)
with right:
    if df.empty:
        st.info("Sem dados para remover ou transferir.")
    else:
        formulario_remover_transacao(df)
        formulario_transferencia_transacao()

st.header("⬆️ Exportar Transações")

if st.button("Exportar para Excel", type="secondary", use_container_width=True):
    to_excel()

st.header("📥 Importar Transações")

uploaded_file = st.file_uploader(
    "Escolha um arquivo Excel (.xlsx)", type=["xlsx", "xlsm"]
)

if uploaded_file is not None:
    if st.button("Importar do Excel", type="secondary", use_container_width=True):
        try:
            df_importado = importar_dados_excel(uploaded_file)
            st.success(f"{len(df_importado)} registros importados com sucesso!")
            st.dataframe(df_importado)
        except Exception as e:
            st.error(f"Erro ao importar: {e}")

# Exibir calculadora no sidebar
calculadora()

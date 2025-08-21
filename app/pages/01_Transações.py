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
    abrir_comprovante,
)
from components.tables_cards import exibir_cartao_inicial, exibir_n_linhas_df
from utils.calculadora import calculadora
from services.layout_ajustes import remove_deploy_buttom, remove_page_margin

DB_PATH = Path("data/orcamento.db")

st.set_page_config(page_title="Transações", page_icon="📥", layout="wide")

remove_deploy_buttom()
remove_page_margin()


def df_transacoes_conf():
    df = connect_db(DB_PATH)
    df = aplicar_filtros(df)
    return df


df = df_transacoes_conf()

exibir_cartao_inicial(df)

if not df.empty:
    exibir_n_linhas_df(df)
else:
    st.info("Sem dados, por favor adicione transações.")

st.header("Operações")

left, center, right = st.columns(3, border=True)

with left:
    formulario_adicionar_transacao()
with center:
    if not df.empty:
        formulario_modificar_transacao(df)
    else:
        st.info("Sem dados, por favor adicione transações.")
with right:
    if not df.empty:
        formulario_remover_transacao(df)
        formulario_transferencia_transacao()
        abrir_comprovante(df)
    else:
        st.info("Sem dados, por favor adicione transações.")

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

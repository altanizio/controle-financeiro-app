import streamlit as st
from services.calculos import receitas_despesas_saldo


def exibir_cartao_inicial(df):
    receitas, despesas, saldo = receitas_despesas_saldo(df)

    col1, col2, col3 = st.columns(3, border=False)
    col1.metric("Receitas", f"R$ {receitas:,.2f}")
    col2.metric("Despesas", f"R$ {despesas:,.2f}")
    col3.metric("Saldo", f"R$ {saldo:,.2f}")


def exibir_n_linhas_df(df):
    if not df.empty:
        n_linhas = st.selectbox("Número de linhas", [5, 10, 15, "Todas"], index=0)
        if n_linhas == "Todas":
            st.dataframe(df, use_container_width=True)
        else:
            st.dataframe(df.tail(int(n_linhas)), use_container_width=True)
    else:
        st.info("Nenhuma receita cadastrada ainda.")

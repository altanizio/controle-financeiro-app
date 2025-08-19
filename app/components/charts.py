import streamlit as st
import pandas as pd
import plotly.express as px
import locale

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

palette = [
    "#fdb462",  # Light orange
    "#386cb0",  # Blue
    "#7fc97f",  # Light green
    "#ef3b2c",  # Red
    "#662506",  # Dark brown
    "#a6cee3",  # Light blue
    "#fb9a99",  # Pink
    "#984ea3",  # Purple
    "#ffff33",  # Yellow
]


def ajustar_moeda(fig, df):
    fig.update_yaxes(tickformat=",")  # separador de milhares
    fig.update_yaxes(tickprefix="R$ ")

    fig.update_traces(
        hovertemplate=df["valor"].apply(
            lambda x: f"Total: {locale.currency(x, grouping=True)}"
        )
    )


def exibir_grafico_cartao_credito(df):
    resultado_cartao = (
        df[df["modo_pag"] == "Cartão"]
        .groupby(["banco", "ano_mes_fatura", "ano_mes_fatura_num"])["valor"]
        .sum()
        .abs()
        .reset_index()
        .sort_values(["ano_mes_fatura_num"])
    )[["banco", "ano_mes_fatura", "valor"]]

    fig_cartao = px.bar(
        data_frame=resultado_cartao,
        x="ano_mes_fatura",
        y="valor",
        color="banco",
        labels={"banco": "Banco", "ano_mes_fatura": "Data", "valor": "Fatura (R$)"},
        height=400,
        text_auto=True,
        title="Fatura do cartão",
        color_discrete_sequence=palette,
    )

    ajustar_moeda(fig_cartao, resultado_cartao)

    st.plotly_chart(fig_cartao, key="fig_cartao_chart")


def exibir_grafico_ganhos_gastos(df):
    resultado_ganhos_gastos = (
        df[df["natureza"].isin(["Ganhos", "Gastos"])]
        .groupby(["ano_mes", "natureza"])["valor"]
        .sum()
        .abs()
        .reset_index()
        .sort_values(["ano_mes"])
    )

    resultado_ganhos_gastos["ano_mes"] = resultado_ganhos_gastos["ano_mes"].astype(str)
    resultado_ganhos_gastos["ano_mes"] = pd.to_datetime(
        resultado_ganhos_gastos["ano_mes"]
    )

    fig_gastos_ganhos = px.line(
        data_frame=resultado_ganhos_gastos,
        x="ano_mes",
        y="valor",
        color="natureza",
        markers=True,
        labels={"ano_mes": "Data", "valor": "Reais (R$)", "natureza": "Natureza"},
        height=400,
        title="Ganhos e Gastos",
        color_discrete_sequence=palette,
    )

    ajustar_moeda(fig_gastos_ganhos, resultado_ganhos_gastos)

    st.plotly_chart(fig_gastos_ganhos, key="fig_gastos_ganhos_chart")


def exibir_grafico_bancos(df):
    resultado_bancos = (
        df[df["modo_pag"].isin(["Pix", "TED", "Débito"])]
        .groupby(["banco"])["valor"]
        .sum()
        .abs()
        .reset_index()
        .sort_values("valor", ascending=False)
        .query("valor > 0.1")
    )

    fig_banco = px.bar(
        data_frame=resultado_bancos,
        x="banco",
        y="valor",
        labels={"valor": "Reais (R$)", "banco": "Banco"},
        height=400,
        text_auto=True,
        title="Bancos",
        color_discrete_sequence=palette,
    )

    ajustar_moeda(fig_banco, resultado_bancos)

    st.plotly_chart(fig_banco, key="fig_banco_chart")


def exibir_ganhos_gastos_tipo(df):
    resultado_ganhos_gastos_tipo = (
        df[df["natureza"].isin(["Ganhos", "Gastos"])]
        .groupby(["tipo"])["valor"]
        .sum()
        .reset_index()
        .sort_values(["valor"], ascending=False)
    )

    fig_ganhos_gastos_tipo = px.bar(
        data_frame=resultado_ganhos_gastos_tipo,
        x="tipo",
        y="valor",
        labels={"valor": "Reais (R$)", "tipo": "Tipo"},
        height=400,
        text_auto=True,
        title="Ganhos e Gastos por Tipo",
        color_discrete_sequence=palette,
    )

    ajustar_moeda(fig_ganhos_gastos_tipo, resultado_ganhos_gastos_tipo)

    st.plotly_chart(fig_ganhos_gastos_tipo, key="fig_ganhos_gastos_tipo_chart")

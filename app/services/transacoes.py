# Adicionar.py
import streamlit as st
import sqlite3
import json
from pathlib import Path
import time
from datetime import datetime
import os
import platform

DB_PATH = Path("data/orcamento.db")
COMPROVANTE_DIR = Path("data/comprovantes")

CONFIG_PATH = Path("data/configuracoes.json")

with CONFIG_PATH.open("r", encoding="utf-8") as f:
    CONFIG = json.load(f)


def adicionar_transacao(
    data, hora, natureza, valor, tipo, modo_pag, banco, obs, comprovante=""
):
    """
    Insere uma nova transação no banco de dados.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO transacoes (data, hora, natureza, valor, tipo, modo_pag, banco, obs, comprovante)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (data, hora, natureza, valor, tipo, modo_pag, banco, obs, comprovante),
    )

    conn.commit()
    conn.close()


def remover_transacao(id):
    """
    Remove uma transação pelo id no banco de dados.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transacoes WHERE id = ?;", (id,))

    conn.commit()
    conn.close()


def modificar_transacao(
    id,
    data=None,
    hora=None,
    natureza=None,
    valor=None,
    tipo=None,
    modo_pag=None,
    banco=None,
    obs=None,
    comprovante=None,
):
    """
    Modifica uma transação pelo id no banco de dados.
    Atualiza apenas os campos fornecidos (não nulos).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    campos = []
    valores = []

    if data is not None:
        campos.append("data = ?")
        valores.append(data)
    if hora is not None:
        campos.append("hora = ?")
        valores.append(hora)
    if natureza is not None:
        campos.append("natureza = ?")
        valores.append(natureza)
    if valor is not None:
        campos.append("valor = ?")
        valores.append(valor)
    if tipo is not None:
        campos.append("tipo = ?")
        valores.append(tipo)
    if modo_pag is not None:
        campos.append("modo_pag = ?")
        valores.append(modo_pag)
    if banco is not None:
        campos.append("banco = ?")
        valores.append(banco)
    if obs is not None:
        campos.append("obs = ?")
        valores.append(obs)
    if comprovante is not None:
        campos.append("comprovante = ?")
        valores.append(comprovante)

    if campos:  # só executa se houver campos para atualizar
        query = f"UPDATE transacoes SET {', '.join(campos)} WHERE id = ?;"
        valores.append(id)
        cursor.execute(query, valores)

    conn.commit()
    conn.close()


def formulario_adicionar_transacao():
    st.subheader("⬆️ Adicionar Transações")

    with st.form("form_adicionar"):
        data = st.date_input("Data")
        hora = st.time_input("Hora")
        natureza = st.selectbox("Natureza", CONFIG["natureza"])

        valor_input = st.number_input("Valor", min_value=0.0, format="%.2f", step=1.0)
        tipo = st.selectbox("Tipo", CONFIG["tipo"], index=14)
        modo_pag = st.selectbox("Modo de pagamento/recebimento", CONFIG["modo"])

        parcelas = st.number_input("Parcelas", min_value=1, step=1)

        banco = st.selectbox("Banco", CONFIG["banco"], index=5)
        obs = st.text_area("Observações")

        arquivo = st.file_uploader(
            "Nota fiscal/Comprovante", type=["pdf", "jpg", "png", "jpeg"]
        )

        submitted = st.form_submit_button("Adicionar")

        if submitted:
            if arquivo is not None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                ext = os.path.splitext(arquivo.name)[1]

                nome_arquivo = f"{obs}_{timestamp}{ext}"

                caminho_arquivo = os.path.join(COMPROVANTE_DIR, nome_arquivo)

                with open(caminho_arquivo, "wb") as f:
                    f.write(arquivo.getbuffer())

                st.success(f"Comprovante salvo em: {caminho_arquivo}")

                comprovante = caminho_arquivo
            else:
                st.warning("Nenhum comprovante selecionado.")
                comprovante = ""

            valor = valor_input
            if natureza in ["Gastos", "Pag.Fatura"]:
                valor = -valor

            if modo_pag != "Cartão":
                parcelas = 1

            if parcelas == 1:
                adicionar_transacao(
                    data,
                    hora.strftime("%H:%M:%S"),
                    natureza,
                    valor,
                    tipo,
                    modo_pag,
                    banco,
                    obs,
                    comprovante,
                )

            else:
                valor_parcelado = valor / parcelas
                valor_parcelado_2 = round(valor_parcelado, 2)
                valor_parcelado_1 = valor_parcelado_2 + (
                    valor - valor_parcelado_2 * parcelas
                )

                for i in range(parcelas):
                    if i == 0:
                        valor_atual = valor_parcelado_1
                    else:
                        valor_atual = valor_parcelado_2

                    obs_atual = f"{obs}; Parcela: {i + 1}"

                    adicionar_transacao(
                        data,
                        hora.strftime("%H:%M:%S"),
                        natureza,
                        valor_atual,
                        tipo,
                        modo_pag,
                        banco,
                        obs_atual,
                        comprovante,
                    )
            st.success("✅ Transação adicionada com sucesso!")
            time.sleep(1)
            st.rerun()


def formulario_remover_transacao(df):
    st.subheader("❌ Remover Transações")

    max_id = df["id"].max()

    id = st.number_input(
        "ID da transação para remover",
        min_value=0,
        max_value=max_id,
        value=max_id,
        step=1,
    )

    df_id = df[df["id"] == id]

    if df_id.empty:
        st.warning("ID não encontrado!")

    st.dataframe(df_id)

    if st.button("Remover"):
        remover_transacao(id)
        st.success("✅ Transação removida com sucesso!")
        time.sleep(1)
        st.rerun()


def formulario_modificar_transacao(df):
    st.subheader("📋 Modificar Transações")

    max_id = df["id"].max()

    id_selecionado = st.number_input(
        "ID da transação para modificar",
        min_value=0,
        max_value=max_id,
        value=max_id,
        step=1,
    )

    transacao_atual = df[df["id"] == id_selecionado].squeeze()

    if transacao_atual.empty:
        st.warning("ID não encontrado!")

    with st.form("form_modificar"):
        data = st.date_input("Data", value=transacao_atual["data"])
        hora = st.time_input("Hora", value=transacao_atual["hora"])
        natureza = st.selectbox(
            "Natureza",
            CONFIG["natureza"],
            index=CONFIG["natureza"].index(transacao_atual["natureza"]),
        )
        valor = st.number_input(
            "Valor", value=float(transacao_atual["valor"]), format="%.2f"
        )
        tipo = st.selectbox(
            "Tipo", CONFIG["tipo"], index=CONFIG["tipo"].index(transacao_atual["tipo"])
        )
        modo_pag = st.selectbox(
            "Modo de pagamento/recebimento",
            CONFIG["modo"],
            index=CONFIG["modo"].index(transacao_atual["modo_pag"]),
        )
        banco = st.selectbox(
            "Banco",
            CONFIG["banco"],
            index=CONFIG["banco"].index(transacao_atual["banco"]),
        )
        obs = st.text_area("Observações", value=transacao_atual["obs"])
        comprovante = st.text_input(
            "Nota fiscal/Comprovante", value=transacao_atual["comprovante"]
        )

        submitted = st.form_submit_button("Modificar")

        if submitted:
            modificar_transacao(
                id=id_selecionado,
                data=data,
                hora=hora.strftime("%H:%M:%S"),
                natureza=natureza,
                valor=valor,
                tipo=tipo,
                modo_pag=modo_pag,
                banco=banco,
                obs=obs,
                comprovante=comprovante,
            )
            st.success("✅ Transação modificada com sucesso!")
            time.sleep(1)
            st.rerun()


def formulario_transferencia_transacao():
    st.subheader("↔️ Transferência entre bancos")

    with st.form("form_transferencia"):
        data = st.date_input("Data")
        hora = st.time_input("Hora")

        banco_origem = st.selectbox("banco_origem", CONFIG["banco"], index=3)
        banco_destino = st.selectbox("banco_destino", CONFIG["banco"], index=5)

        valor_input = st.number_input("Valor", min_value=0.0, format="%.2f", step=1.0)
        submitted = st.form_submit_button("Adicionar")

        if submitted:
            adicionar_transacao(
                data,
                hora.strftime("%H:%M:%S"),
                "Transferência",
                -valor_input,
                "Transferência",
                "Pix",
                banco_origem,
                "Transferência",
                "",
            )

            adicionar_transacao(
                data,
                hora.strftime("%H:%M:%S"),
                "Transferência",
                valor_input,
                "Transferência",
                "Pix",
                banco_destino,
                "Transferência",
                "",
            )

            st.success("✅ Transferência realizada com sucesso!")
            time.sleep(1)
            st.rerun()


def abrir_comprovante(df):
    st.subheader("📄 Abrir Comprovante")

    max_id = df["id"].max()

    id = st.number_input(
        "ID da transação para abrir o comprovante",
        min_value=0,
        max_value=max_id,
        value=max_id,
        step=1,
    )

    df_id = df[df["id"] == id]

    if df_id.empty:
        st.warning("ID não encontrado!")
    else:
        comprovante = df_id["comprovante"].values[0]
        if comprovante and os.path.exists(comprovante):
            if st.button("Abrir Comprovante"):
                try:
                    if platform.system() == "Windows":
                        os.startfile(comprovante)
                        st.success(
                            f"Abrindo {comprovante} no aplicativo padrão do Windows."
                        )
                    else:
                        raise OSError("Não é Windows")
                except Exception as e:
                    st.warning(f"Não foi possível abrir automaticamente: {e}")
                    with open(comprovante, "rb") as f:
                        st.download_button(
                            label="Baixar Comprovante",
                            data=f,
                            file_name=os.path.basename(comprovante),
                        )
        else:
            st.warning("Nenhum comprovante encontrado para esta transação.")

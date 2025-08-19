from datetime import datetime
from storage.database import connect_db
from pathlib import Path
import streamlit as st

# --- Configuração do banco ---
DB_PATH = Path("data/orcamento.db")


def to_excel():
    data_hora_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"transacoes_{data_hora_atual}.xlsx"
    df = connect_db(DB_PATH)
    path_save = "data/exportações/" + nome_arquivo
    df.to_excel(path_save)
    st.success(f"{len(df)} registros exportados com sucesso!\n Local: {path_save}")

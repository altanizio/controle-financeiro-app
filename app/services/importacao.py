import pandas as pd
import sqlite3
from pathlib import Path


DB_PATH = Path("data/orcamento.db")


def importar_dados_excel(uploaded_file):
    df = pd.read_excel(uploaded_file, sheet_name="Gastos e Ganhos")

    columns = {
        "ID": "id",
        "Data": "data",
        "Hora": "hora",
        "Natureza": "natureza",
        "Valor": "valor",
        "Tipo": "tipo",
        "Observações": "obs",
        "Modo de pag. ou rec.": "modo_pag",
        "Banco": "banco",
        "Nota fiscal/Comprovante": "comprovante",
    }

    missing_cols = [col for col in columns if col not in df.columns]

    if missing_cols:
        raise ValueError(f"As colunas estão faltando no Excel: {missing_cols}")

    df = df.rename(columns=columns)

    df = df[list(columns.values())]

    df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0.0)
    df["data"] = pd.to_datetime(df["data"], errors="coerce").dt.date
    df["hora"] = pd.to_datetime(df["hora"], errors="coerce").dt.time
    df["banco"] = df["banco"].astype(str)  # pode ser texto ou número
    df["modo_pag"] = df["modo_pag"].astype(str)
    df["tipo"] = df["tipo"].astype(str)

    conn = sqlite3.connect(DB_PATH)
    df.to_sql("transacoes", conn, if_exists="append", index=False)
    conn.close()

    return df

import sqlite3
import pandas as pd


def init_db(db_path="data/orcamento.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data DATE NOT NULL,
        hora TIME,
        natureza TEXT NOT NULL,
        valor REAL NOT NULL,
        tipo TEXT NOT NULL,
        obs TEXT,
        modo_pag TEXT NOT NULL,
        banco TEXT,
        comprovante TEXT
    )
    """)
    conn.commit()
    conn.close()


def connect_db(db_path="data/orcamento.db", table="transacoes"):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()
    return df

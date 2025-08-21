import json
import streamlit as st
from pathlib import Path
from services.layout_ajustes import remove_deploy_buttom, remove_page_margin

FILE = Path("data/configuracoes.json")


def load_json():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_json(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


st.title("Configurações")

remove_deploy_buttom()
remove_page_margin()

data = load_json()

for key, value in data.items():
    st.subheader(key)

    # Listas normais
    if isinstance(value, list) and key != "banco":
        new_list = st.text_area(
            f"Editar {key} (um item por linha):", value="\n".join(value), height=150
        )
        data[key] = [v.strip() for v in new_list.split("\n") if v.strip()]

    elif key == "banco":
        new_bancos = st.text_area(
            "Editar bancos (um por linha):", value="\n".join(value), height=150
        )
        bancos = [v.strip() for v in new_bancos.split("\n") if v.strip()]
        data[key] = bancos

        st.markdown("### Fechamento de Fatura")
        if "fechamento_fatura" not in data:
            data["fechamento_fatura"] = {}

        for banco in bancos:
            atual = data["fechamento_fatura"].get(banco, 0)
            data["fechamento_fatura"][banco] = st.number_input(
                f"{banco}", value=atual, step=1
            )

    elif isinstance(value, dict) and key != "fechamento_fatura":
        new_dict = {}
        for subkey, subvalue in value.items():
            new_dict[subkey] = st.text_input(f"{key} - {subkey}", value=str(subvalue))
        data[key] = new_dict

if st.button("Salvar alterações"):
    save_json(data)
    st.success("Configurações salvas com sucesso!")

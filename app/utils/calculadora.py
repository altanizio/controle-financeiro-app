import streamlit as st


def calculadora():
    st.sidebar.title("Calculadora")

    num1 = st.sidebar.number_input("Digite o primeiro número:")
    num2 = st.sidebar.number_input("Digite o segundo número:")

    operacao = st.sidebar.selectbox("Escolha a operação:", ["+", "-", "*", "/"])

    if st.sidebar.button("Calcular"):
        if operacao == "+":
            resultado = num1 + num2
        elif operacao == "-":
            resultado = num1 - num2
        elif operacao == "*":
            resultado = num1 * num2
        elif operacao == "/":
            if num2 != 0:
                resultado = num1 / num2
            else:
                resultado = "Erro: divisão por zero!"
        st.sidebar.success(f"O resultado é: {resultado}")

import streamlit as st
import requests

BACKEND_URL = "https://seu-backend-no-render.onrender.com"

st.title("Ingestão de Dados")

# Formulário
nome = st.text_input("Nome")
email = st.text_input("Email")

if st.button("Enviar"):
    if nome and email:
        # Enviar dados para o backend
        response = requests.post(
            f"{BACKEND_URL}/dados", json={"nome": nome, "email": email}
        )

        if response.status_code == 201:
            st.success("Dados enviados com sucesso!")
        else:
            st.error("Erro ao enviar os dados!")
    else:
        st.warning("Preencha todos os campos!")

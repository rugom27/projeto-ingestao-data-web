import streamlit as st
import requests

# URL do backend no Render
BACKEND_URL = "https://projeto-ingestao-data-web.onrender.com"

# Título da aplicação
st.title("Gestão de Reuniões com Clientes")

# Buscar lista de clientes
try:
    response = requests.get(f"{BACKEND_URL}/clientes")
    response.raise_for_status()  # Gera exceção para códigos de erro HTTP
    clientes = response.json()
except requests.exceptions.RequestException as e:
    st.error(f"Erro ao buscar clientes: {e}")
    clientes = []

# Selecionar cliente
if clientes:
    cliente_options = {cliente["id"]: cliente["name"] for cliente in clientes}
    cliente_id = st.selectbox("Selecione o cliente", options=cliente_options.keys(), format_func=lambda x: cliente_options[x])
else:
    cliente_id = None

# Campos da reunião
data_reuniao = st.date_input("Data da reunião")
descricao = st.text_area("Descrição da reunião")

# Botão de envio
if st.button("Registar reunião"):
    if cliente_id and data_reuniao and descricao:
        try:
            # Envia os dados para o backend
            response = requests.post(
                f"{BACKEND_URL}/reunioes",
                json={"cliente_id": cliente_id, "data_reuniao": str(data_reuniao), "descricao": descricao}
            )
            response.raise_for_status()  # Gera exceção para códigos de erro HTTP
            st.success("Reunião registada com sucesso!")
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao registar reunião: {e}")
    else:
        st.warning("Por favor, preencha todos os campos.")
import streamlit as st
import requests

# URL do backend
BACKEND_URL = "https://projeto-ingestao-data-web.onrender.com"

# Título da aplicação
st.title("Gestão de Reuniões e Vendas")

# Função para carregar dados paginados
def fetch_paginated_data(endpoint, page, limit):
    try:
        response = requests.get(f"{BACKEND_URL}/{endpoint}", params={"skip": page * limit, "limit": limit})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao procurar dados: {e}")
        return []

# Paginação para Clientes
st.header("Clientes")
page_clientes = st.number_input("Página de Clientes", min_value=0, step=1, format="%d")
clientes_por_pagina = 10
clientes = fetch_paginated_data("clientes", page_clientes, clientes_por_pagina)
if clientes:
    cliente_options = {cliente["id"]: cliente["name"] for cliente in clientes}
    cliente_id = st.selectbox("Selecione o cliente", options=cliente_options.keys(), format_func=lambda x: cliente_options[x])
else:
    cliente_id = None

novo_cliente = st.checkbox("Adicionar novo cliente?")
if novo_cliente:
    with st.form("form_novo_cliente"):
        nome_cliente = st.text_input("Nome do Cliente")
        numero_cliente = st.text_input("Número do Cliente")
        cod_postal = st.text_input("Código Postal")
        tipo_cliente = st.text_input("Tipo de Cliente")
        distrito = st.text_input("Distrito")
        latitude = st.number_input("Latitude", format="%.6f")
        longitude = st.number_input("Longitude", format="%.6f")
        submit_cliente = st.form_submit_button("Registrar Cliente")
        if submit_cliente:
            novo_cliente_data = {
                "name": nome_cliente,
                "numero_cliente": numero_cliente,
                "cod_postal": cod_postal,
                "tipo_cliente": tipo_cliente,
                "distrito": distrito,
                "latitude": latitude,
                "longitude": longitude,
            }
            try:
                response = requests.post(f"{BACKEND_URL}/clientes", json=novo_cliente_data)
                response.raise_for_status()
                st.success("Cliente registado com sucesso!")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao registar cliente: {e}")

# Paginação para Produtos
st.header("Produtos")
page_produtos = st.number_input("Página de Produtos", min_value=0, step=1, format="%d")
produtos_por_pagina = 10
produtos = fetch_paginated_data("produtos", page_produtos, produtos_por_pagina)
if produtos:
    produto_options = {produto["id"]: produto["ref"] for produto in produtos}
    produto_id = st.selectbox("Selecione o Produto", options=produto_options.keys(), format_func=lambda x: produto_options[x])
else:
    produto_id = None

novo_produto = st.checkbox("Adicionar novo produto?")
if novo_produto:
    with st.form("form_novo_produto"):
        ref_produto = st.text_input("Referência do Produto")
        submit_produto = st.form_submit_button("Registar Produto")
        if submit_produto:
            novo_produto_data = {
                "ref": ref_produto
            }
            try:
                response = requests.post(f"{BACKEND_URL}/produtos", json=novo_produto_data)
                response.raise_for_status()
                st.success("Produto registado com sucesso!")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao registar produto: {e}")

# Submeter Reunião
st.header("Submeter Dados")
data_reuniao = st.date_input("Data da Reunião")
descricao_reuniao = st.text_area("Descrição da Reunião")
houve_venda = st.radio("Foi feita uma venda?", ("Sim", "Não"))

if st.button("Registar Reunião"):
    reuniao_data = {
        "cliente_id": cliente_id,
        "data_reuniao": str(data_reuniao),
        "descricao": descricao_reuniao,
        "houve_venda": houve_venda,
        "produto_id": produto_id if houve_venda == "Sim" else None,
        "quantidade_vendida": None,
        "preco_vendido": None,
        "razao_nao_venda": None if houve_venda == "Sim" else "Sem venda",
    }
    try:
        response = requests.post(f"{BACKEND_URL}/reunioes", json=reuniao_data)
        response.raise_for_status()
        st.success("Reunião registada com sucesso!")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao registar reunião: {e}")

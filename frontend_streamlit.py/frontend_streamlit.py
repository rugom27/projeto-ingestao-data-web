import streamlit as st
import requests

# URL do backend
BACKEND_URL = "https://projeto-ingestao-data-web.onrender.com"

# Título da aplicação
st.title("Gestão de Reuniões e Vendas")

# Passo 1: Seleção ou Registo de Cliente
st.header("Cliente")
try:
    response = requests.get(f"{BACKEND_URL}/clientes")
    response.raise_for_status()
    clientes = response.json()
except requests.exceptions.RequestException as e:
    st.error(f"Erro ao buscar clientes: {e}")
    clientes = []

cliente_id = None
if clientes:
    cliente_options = {cliente["id"]: cliente["name"] for cliente in clientes}
    cliente_id = st.selectbox("Selecione o cliente", options=cliente_options.keys(), format_func=lambda x: cliente_options[x])

novo_cliente = st.checkbox("Cliente novo?")
if novo_cliente:
    with st.form("novo_cliente_form"):
        name = st.text_input("Nome do Cliente", max_chars=100)
        numero_cliente = st.text_input("Número do Cliente (Opcional)")
        cod_postal = st.text_input("Código Postal")
        tipo_cliente = st.text_input("Tipo de Cliente")
        distrito = st.text_input("Distrito")
        latitude = st.number_input("Latitude", format="%.6f")
        longitude = st.number_input("Longitude", format="%.6f")
        submit_cliente = st.form_submit_button("Registar Cliente")

        if submit_cliente:
            cliente_data = {
                "name": name,
                "numero_cliente": numero_cliente or None,
                "cod_postal": cod_postal,
                "tipo_cliente": tipo_cliente,
                "distrito": distrito,
                "latitude": latitude,
                "longitude": longitude,
            }
            try:
                response = requests.post(f"{BACKEND_URL}/clientes", json=cliente_data)
                response.raise_for_status()
                st.success("Cliente registado com sucesso!")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao registar cliente: {e}")

# Passo 2: Descrição da Reunião
st.header("Reunião")
data_reuniao = st.date_input("Data da Reunião")
descricao_reuniao = st.text_area("Descrição da Reunião")

# Passo 3: Produto Vendido e Quantidade
st.header("Venda")
try:
    response = requests.get(f"{BACKEND_URL}/produtos")
    response.raise_for_status()
    produtos = response.json()
except requests.exceptions.RequestException as e:
    st.error(f"Erro ao buscar produtos: {e}")
    produtos = []

if produtos:
    produto_options = {produto["id"]: produto["ref"] for produto in produtos}
    produto_id = st.selectbox("Selecione o Produto", options=produto_options.keys(), format_func=lambda x: produto_options[x])
else:
    produto_id = None

novo_produto = st.checkbox("Adicionar novo produto?")
if novo_produto:
    novo_produto_nome = st.text_input("Nome do novo produto")
    if st.button("Adicionar Produto"):
        produto_data = {"ref": novo_produto_nome}
        try:
            response = requests.post(f"{BACKEND_URL}/produtos", json=produto_data)
            response.raise_for_status()
            st.success("Produto adicionado com sucesso!")
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao adicionar produto: {e}")

quantidade = st.number_input("Quantidade Vendida", min_value=1, step=1)
valor_manual = st.number_input("Valor Vendido (Manual)", min_value=0.0, format="%.2f")
valor_calculado = quantidade * valor_manual  # Exemplo de cálculo automático (substituir pelo valor real do produto)
st.text(f"Valor calculado (sugestão): {valor_calculado:.2f} EUR")

# Submeter Reunião e Venda
st.header("Submeter Dados")
if st.button("Registar Reunião e Venda"):
    if cliente_id and data_reuniao and descricao_reuniao and produto_id and quantidade:
        # Enviar dados da reunião
        reuniao_data = {
            "cliente_id": cliente_id,
            "data_reuniao": str(data_reuniao),
            "descricao": descricao_reuniao,
        }
        try:
            response_reuniao = requests.post(f"{BACKEND_URL}/reunioes", json=reuniao_data)
            response_reuniao.raise_for_status()
            st.success("Reunião registada com sucesso!")
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao registar reunião: {e}")

        # Enviar dados da venda
        venda_data = {
            "produto_id": produto_id,
            "quantidade": quantidade,
            "valor_vendido": valor_manual,
        }
        try:
            response_venda = requests.post(f"{BACKEND_URL}/vendas", json=venda_data)
            response_venda.raise_for_status()
            st.success("Venda registada com sucesso!")
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao registar venda: {e}")
    else:
        st.warning("Por favor, preencha todos os campos antes de submeter.")
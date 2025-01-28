import streamlit as st
import requests
import time

# URL do backend
BACKEND_URL = "https://projeto-ingestao-data-web.onrender.com"

# Título da aplicação
st.title("Gestão de Reuniões e Vendas")

# Placeholder para mensagens
status_placeholder = st.empty()


# Função para carregar dados com barra de progresso
def fetch_data_with_progress(endpoint):
    status_placeholder.text("Carregando dados...")
    progress_bar = st.progress(0)

    try:
        response = requests.get(f"{BACKEND_URL}/{endpoint}")
        response.raise_for_status()
        data = response.json()
        for percent in range(1, 101):
            time.sleep(0.05)  # Simular carregamento
            progress_bar.progress(percent)
        status_placeholder.text("Dados carregados com sucesso!")
        return data
    except requests.exceptions.RequestException as e:
        status_placeholder.text(f"Erro ao carregar dados: {e}")
        return []


# Carregar dados de clientes e reuniões
clientes = fetch_data_with_progress("clientes")

# Exibir dados carregados
st.header("Clientes")
if clientes:
    cliente_options = {cliente["id"]: cliente["name"] for cliente in clientes}
    cliente_id = st.selectbox(
        "Selecione o cliente",
        options=cliente_options.keys(),
        format_func=lambda x: cliente_options[x],
    )

    # Buscar reuniões anteriores do cliente
    if cliente_id:
        try:
            reunioes_response = requests.get(
                f"{BACKEND_URL}/reunioes?cliente_id={cliente_id}"
            )
            reunioes_response.raise_for_status()
            reunioes_cliente = reunioes_response.json()
            if reunioes_cliente:
                st.subheader("Reuniões anteriores do cliente")
                st.table(reunioes_cliente)
            else:
                st.info("Este cliente não tem reuniões registadas.")
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao procurar reuniões: {e}")
else:
    st.info("Nenhum cliente disponível.")

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

st.header("Reunião")
data_reuniao = st.date_input("Data da Reunião")
descricao_reuniao = st.text_area("Descrição da Reunião")

# Perguntar se houve venda
houve_venda = st.radio("Foi feita uma venda?", ("Sim", "Não"))

if houve_venda == "Sim":
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
        produto_id = st.selectbox(
            "Selecione o Produto",
            options=produto_options.keys(),
            format_func=lambda x: produto_options[x],
        )
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
    valor_manual = st.number_input(
        "Valor Vendido (Manual)", min_value=0.0, format="%.2f"
    )
    valor_calculado = quantidade * valor_manual
    st.text(f"Valor calculado (sugestão): {valor_calculado:.2f} EUR")

elif houve_venda == "Não":
    razao_nao_venda = st.text_area("Razão pela qual não houve venda")

st.header("Submeter Dados")
if st.button("Registar Reunião"):
    # Garantir que o cliente_id é válido
    if cliente_id is None:
        st.error("Por favor, selecione um cliente antes de registar a reunião.")
    else:
        # Construção inicial do JSON
        reuniao_data = {
            "cliente_id": cliente_id,
            "data_reuniao": str(data_reuniao),
            "descricao": descricao_reuniao,
            "houve_venda": houve_venda,
        }

        # Dados adicionais dependendo de "houve_venda"
        if houve_venda == "Sim":
            # Verificar campos obrigatórios para vendas
            if produto_id is None or quantidade <= 0 or valor_manual <= 0:
                st.error("Por favor, preencha todos os campos relacionados à venda.")
            else:
                reuniao_data.update(
                    {
                        "produto_id": produto_id,
                        "quantidade_vendida": quantidade,
                        "preco_vendido": valor_manual,
                        "razao_nao_venda": None,
                    }
                )
        elif houve_venda == "Não":
            # Garantir que a razão da não venda está preenchida
            if not razao_nao_venda.strip():
                st.error("Por favor, preencha a razão pela qual não houve venda.")
            else:
                reuniao_data.update(
                    {
                        "produto_id": None,
                        "quantidade_vendida": None,
                        "preco_vendido": None,
                        "razao_nao_venda": razao_nao_venda.strip(),
                    }
                )

        # Enviar somente se todos os dados forem válidos
        st.write(reuniao_data)  # DEBUG: Verificar o JSON gerado no frontend
        try:
            response = requests.post(f"{BACKEND_URL}/reunioes", json=reuniao_data)
            response.raise_for_status()
            st.success("Reunião registada com sucesso!")
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao registar reunião: {e}")

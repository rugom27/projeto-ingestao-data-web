import streamlit as st
from application.database import insert_cliente, insert_venda, get_clientes


def main():
    st.title("Gestão de Clientes e Vendas")

    menu = ["Inserir Cliente", "Inserir Venda"]
    escolha = st.sidebar.selectbox("Menu", menu)

    if escolha == "Inserir Cliente":
        st.subheader("Inserir Novo Cliente")
        with st.form("form_cliente"):
            numero_cliente = st.text_input("Número do Cliente (ID)")
            name = st.text_input("Nome")
            cod_postal = st.text_input("Código Postal")
            tipo_cliente = st.text_input("Tipo de Cliente")
            ranking = st.text_input("Ranking")
            cultura = st.text_input("Cultura")
            area_culturas = st.number_input(
                "Área das Culturas", min_value=0.0, step=0.1
            )
            responsavel_principal = st.text_input("Responsável Principal")
            responsavel_secundario = st.text_input("Responsável Secundário")
            distrito = st.text_input("Distrito")
            latitude = st.number_input("Latitude", step=0.0001)
            longitude = st.number_input("Longitude", step=0.0001)
            submit = st.form_submit_button("Salvar Cliente")

            if submit:
                if numero_cliente and name:
                    cliente_data = {
                        "numero_cliente": numero_cliente,
                        "name": name,
                        "cod_postal": cod_postal,
                        "tipo_cliente": tipo_cliente,
                        "ranking": ranking,
                        "cultura": cultura,
                        "area_culturas": area_culturas,
                        "responsavel_principal": responsavel_principal,
                        "responsavel_secundario": responsavel_secundario,
                        "distrito": distrito,
                        "latitude": latitude,
                        "longitude": longitude,
                    }
                    insert_cliente(cliente_data)
                    st.success("Cliente adicionado com sucesso!")
                else:
                    st.error("Os campos Número do Cliente e Nome são obrigatórios.")

    elif escolha == "Inserir Venda":
        st.subheader("Inserir Nova Venda")
        clientes = get_clientes()
        cliente_opcoes = {
            f"{cliente[1]} ({cliente[0]})": cliente[0] for cliente in clientes
        }
        cliente_selecionado = st.selectbox(
            "Selecione o Cliente", list(cliente_opcoes.keys())
        )

        with st.form("form_venda"):
            ref = st.text_input("Referência")
            design = st.text_input("Designação")
            data = st.date_input("Data da Venda")
            quant = st.number_input("Quantidade", min_value=1, step=1)
            eur = st.number_input("Valor em Euros", min_value=0.0, step=0.01)
            submit = st.form_submit_button("Salvar Venda")

            if submit:
                if cliente_selecionado and data and quant > 0 and eur > 0:
                    venda_data = {
                        "numero_de_cliente": cliente_opcoes[cliente_selecionado],
                        "ref": ref,
                        "design": design,
                        "data": str(data),
                        "quant": quant,
                        "eur": eur,
                    }
                    insert_venda(venda_data)
                    st.success("Venda adicionada com sucesso!")
                else:
                    st.error("Todos os campos são obrigatórios.")


if __name__ == "__main__":
    main()

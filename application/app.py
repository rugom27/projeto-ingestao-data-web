import streamlit as st
from database import get_clientes, insert_report


# Página principal
def main():
    st.title("Gestão de Relatórios e Clientes")

    # Secção para selecionar o cliente
    st.subheader("Adicionar Relatório")
    clientes = get_clientes()
    cliente_opcoes = {f"{cliente[1]} ({cliente[0]})": cliente for cliente in clientes}

    # Dropdown para seleção de cliente
    cliente_selecionado = st.selectbox(
        "Selecione o Cliente", list(cliente_opcoes.keys())
    )

    if cliente_selecionado:
        cliente_info = cliente_opcoes[cliente_selecionado]
        cliente_id, cliente_nome = cliente_info

        # Mostrar informações do cliente
        st.text_input("ID do Cliente", cliente_id, disabled=True)
        st.text_input("Nome do Cliente", cliente_nome, disabled=True)

        # Outros campos para o relatório
        data = st.date_input("Data do Relatório")
        detalhes = st.text_area("Detalhes do Relatório")
        tipo = st.selectbox("Tipo de Relatório", ["Reunião", "Venda", "Outro"])

        # Botão para submeter
        if st.button("Submeter Relatório"):
            if detalhes:
                # Inserir o relatório na base de dados
                report_data = {
                    "cliente_id": cliente_id,
                    "data": str(data),
                    "detalhes": detalhes,
                    "tipo": tipo,
                }
                insert_report(report_data)
                st.success("Relatório adicionado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos obrigatórios.")


if __name__ == "__main__":
    main()

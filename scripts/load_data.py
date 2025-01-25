import pandas as pd
from app.database import insert_cliente, insert_venda

# Caminho do ficheiro Excel
EXCEL_PATH = "data/full_data.xlsx"

def load_clientes(sheet_name="clientes_processado"):
    """Carrega dados da folha 'clientes_processado' para a tabela clientes."""
    df = pd.read_excel(EXCEL_PATH, sheet_name=sheet_name)
    # Limpar colunas desnecessárias
    df = df.drop(columns=['Unnamed: 12', 'Unnamed: 13'], errors='ignore')
    df.columns = [
        'Name', 'Numero Cliente', 'Cód-Postal', 'Tipo de Cliente', 'Ranking',
        'Cultura', 'Área das culturas', 'Responsável_principal', 'Responsável_secundário',
        'Distrito', 'latitude', 'longitude'
    ]
    # Inserir dados na tabela clientes
    for _, row in df.iterrows():
        cliente_data = {
            'numero_cliente': row['Numero Cliente'],
            'name': row['Name'],
            'cod_postal': row['Cód-Postal'],
            'tipo_cliente': row['Tipo de Cliente'],
            'ranking': row['Ranking'],
            'cultura': row['Cultura'],
            'area_culturas': row['Área das culturas'],
            'responsavel_principal': row['Responsável_principal'],
            'responsavel_secundario': row['Responsável_secundário'],
            'distrito': row['Distrito'],
            'latitude': row['latitude'],
            'longitude': row['longitude']
        }
        insert_cliente(cliente_data)
    print("Clientes carregados com sucesso!")

def load_vendas(sheet_name="vendas_2023_2024_processado"):
    """Carrega dados da folha 'vendas_2023_2024_processado' para a tabela vendas."""
    df = pd.read_excel(EXCEL_PATH, sheet_name=sheet_name)
    # Limpar colunas desnecessárias
    df = df.drop(columns=['Column1'], errors='ignore')
    df.columns = ['nome', 'ref', 'design', 'Data', 'Quant', 'Eur', 'numero_de_cliente']
    # Inserir dados na tabela vendas
    for _, row in df.iterrows():
        venda_data = {
            'numero_de_cliente': row['numero_de_cliente'],
            'ref': row['ref'],
            'design': row['design'],
            'data': row['Data'],
            'quant': row['Quant'],
            'eur': row['Eur']
        }
        insert_venda(venda_data)
    print("Vendas carregadas com sucesso!")

if __name__ == "__main__":
    print("Carregando dados do Excel para a base de dados...")
    load_clientes()
    load_vendas()
    print("Todos os dados foram carregados com sucesso!")

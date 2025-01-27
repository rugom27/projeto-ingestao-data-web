from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from typing import List
from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()

# Obter a URL da base de dados do arquivo .env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("A variável de ambiente DATABASE_URL não está configurada no .env ou no ambiente.")

# Inicializar o FastAPI
app = FastAPI()

# Conexão com a base de dados
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar à base de dados: {e}")

# Modelo de dados para a reunião
class ReuniaoData(BaseModel):
    cliente_id: int
    data_reuniao: str
    descricao: str

# Modelo de dados para o produto
class ProdutoData(BaseModel):
    ref: str

def carregar_dados():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Carregar e preparar dados de clientes
        clientes_df = pd.read_csv("data/clientes.csv")
        clientes_df = clientes_df.rename(columns={
            "Name": "name",
            "Numero Cliente": "numero_cliente",
            "Cód-Postal": "cod_postal",
            "Tipo de Cliente": "tipo_cliente",
            "Cultura": "cultura",
            "Área das culturas": "area_culturas",
            "Responsável_principal": "responsavel_principal",
            "Responsável_secundário": "responsavel_secundario",
            "Distrito": "distrito",
            "latitude": "latitude",
            "longitude": "longitude"
        })
        clientes_df = clientes_df.drop(columns=[col for col in clientes_df.columns if "Unnamed" in col])
        clientes_df = clientes_df.where(pd.notnull(clientes_df), None)

        # Inserir dados de clientes no banco
        for _, row in clientes_df.iterrows():
            data = tuple(row.values)  # Certificar-se de que os dados sejam uma tupla
            try:
                print(f"Inserindo cliente: {data}")  # Debug para verificar os dados
                cursor.execute(
                    """
                    INSERT INTO clientes (name, numero_cliente, cod_postal, tipo_cliente, cultura, area_culturas, responsavel_principal, responsavel_secundario, distrito, latitude, longitude)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    data
                )
            except Exception as e:
                print(f"Erro ao inserir cliente: {data}. Detalhes: {e}")
                conn.rollback()  # Rollback em caso de erro

        # Carregar e preparar dados de vendas
        vendas_df = pd.read_csv("data/vendas.csv")
        vendas_df = vendas_df.rename(columns={
            "Indice": "indice",
            "nome": "nome",
            "ref": "ref",
            "design": "design",
            "Data": "data",
            "Quant": "quant",
            "Eur": "eur",
            "numero_de_cliente": "numero_de_cliente"
        })
        vendas_df = vendas_df.where(pd.notnull(vendas_df), None)

        # Inserir dados de vendas no banco
        for _, row in vendas_df.iterrows():
            data = tuple(row.values)  # Certificar-se de que os dados sejam uma tupla
            try:
                print(f"Inserindo venda: {data}")  # Debug para verificar os dados
                cursor.execute(
                    """
                    INSERT INTO vendas (indice, nome, ref, design, data, quant, eur, numero_de_cliente)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    data
                )
            except Exception as e:
                print(f"Erro ao inserir venda: {data}. Detalhes: {e}")
                conn.rollback()  # Rollback em caso de erro

        # Confirmar as alterações no banco de dados
        conn.commit()
        print("Carga de dados concluída com sucesso!")

    except Exception as e:
        print(f"Erro durante a carga de dados: {e}")
        conn.rollback()  # Rollback em caso de erro
    finally:
        cursor.close()
        conn.close()

# Endpoint para listar clientes
@app.get("/clientes")
async def listar_clientes():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name FROM clientes")
        clientes = cursor.fetchall()
        return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar clientes: {e}")
    finally:
        cursor.close()
        conn.close()

# Endpoint para listar produtos
@app.get("/produtos")
async def listar_produtos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT produto_id AS id, ref FROM produtos")
        produtos = cursor.fetchall()
        return produtos
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")  # Log do erro
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produtos: {e}")
    finally:
        cursor.close()
        conn.close()


# Endpoint para inserir reunião
@app.post("/reunioes")
async def inserir_reuniao(reuniao: ReuniaoData):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO reunioes (cliente_id, data_reuniao, descricao)
            VALUES (%s, %s, %s)
            """,
            (reuniao.cliente_id, reuniao.data_reuniao, reuniao.descricao)
        )
        conn.commit()
        return {"message": "Reunião registrada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Endpoint para inserir produto
@app.post("/produtos")
async def inserir_produto(produto: ProdutoData):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO produtos (ref)
            VALUES (%s)
            """,
            (produto.ref,)
        )
        conn.commit()
        return {"message": "Produto registrado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


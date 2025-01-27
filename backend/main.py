from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
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
    houve_venda: str
    produto_id: int = None
    quantidade_vendida: int = None
    preco_vendido: float = None
    razao_nao_venda: str = None

# Modelo de dados para o produto
class ProdutoData(BaseModel):
    ref: str

# Endpoint para listar clientes
@app.get("/clientes")
async def listar_clientes():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name FROM clientes")
        clientes = cursor.fetchall()
        if not clientes:
            return {"message": "Nenhum cliente encontrado."}
        return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar clientes: {e}")
    finally:
        cursor.close()
        conn.close()

# Endpoint para listar reuniões
@app.get("/reunioes")
async def listar_reunioes(cliente_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM reunioes WHERE cliente_id = %s", (cliente_id,))
        reunioes = cursor.fetchall()
        if len(reunioes) == 0:  # Verificar explicitamente o comprimento
            return {"message": "Não existem reuniões para este cliente."}
        return reunioes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar reuniões: {e}")



# Endpoint para inserir reunião
@app.post("/reunioes")
async def inserir_reuniao(reuniao: ReuniaoData):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO reunioes (cliente_id, data_reuniao, descricao, houve_venda, produto_id, quantidade_vendida, preco_vendido, razao_nao_venda)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                reuniao.cliente_id,
                reuniao.data_reuniao,
                reuniao.descricao,
                reuniao.houve_venda,
                reuniao.produto_id,
                reuniao.quantidade_vendida,
                reuniao.preco_vendido,
                reuniao.razao_nao_venda,
            )
        )
        conn.commit()
        return {"message": "Reunião registrada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Endpoint para listar produtos
@app.get("/produtos")
async def listar_produtos():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT produto_id AS id, ref FROM produtos")
        produtos = cursor.fetchall()
        if not produtos:
            return {"message": "Nenhum produto encontrado."}
        return produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produtos: {e}")
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
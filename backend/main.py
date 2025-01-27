from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
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
        raise HTTPException(status_code=500, detail=f"Erro ao conetar à base de dados: {e}")

# Modelo de dados para o cliente
class ClienteData(BaseModel):
    name: str
    numero_cliente: Optional[str] = None
    cod_postal: str
    tipo_cliente: str
    distrito: str
    latitude: float
    longitude: float

# Modelo de dados para o produto
class ProdutoData(BaseModel):
    ref: str

# Modelo de dados para a reunião
class ReuniaoData(BaseModel):
    cliente_id: int
    data_reuniao: str
    descricao: str
    houve_venda: str
    produto_id: Optional[int] = None
    quantidade_vendida: Optional[int] = None
    preco_vendido: Optional[float] = None
    razao_nao_venda: Optional[str] = None

# Endpoint para listar clientes com paginação
@app.get("/clientes")
async def listar_clientes(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name FROM clientes ORDER BY id LIMIT %s OFFSET %s", (limit, skip))
        clientes = cursor.fetchall()
        return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao procurar clientes: {e}")
    finally:
        cursor.close()
        conn.close()

# Endpoint para adicionar novo cliente
@app.post("/clientes")
async def adicionar_cliente(cliente: ClienteData):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO clientes (name, numero_cliente, cod_postal, tipo_cliente, distrito, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (cliente.name, cliente.numero_cliente, cliente.cod_postal, cliente.tipo_cliente, cliente.distrito, cliente.latitude, cliente.longitude)
        )
        conn.commit()
        novo_cliente_id = cursor.fetchone()["id"]
        return {"id": novo_cliente_id, "message": "Cliente adicionado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar cliente: {e}")
    finally:
        cursor.close()
        conn.close()

# Endpoint para listar produtos com paginação
@app.get("/produtos")
async def listar_produtos(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT produto_id AS id, ref FROM produtos ORDER BY produto_id LIMIT %s OFFSET %s", (limit, skip))
        produtos = cursor.fetchall()
        return produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao procurar produtos: {e}")
    finally:
        cursor.close()
        conn.close()

# Endpoint para adicionar novo produto
@app.post("/produtos")
async def adicionar_produto(produto: ProdutoData):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO produtos (ref)
            VALUES (%s)
            RETURNING produto_id
            """,
            (produto.ref,)
        )
        conn.commit()
        novo_produto_id = cursor.fetchone()["produto_id"]
        return {"id": novo_produto_id, "message": "Produto adicionado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar produto: {e}")
    finally:
        cursor.close()
        conn.close()

# Endpoint para adicionar reunião
@app.post("/reunioes")
async def inserir_reuniao(reuniao: ReuniaoData):
    if not reuniao.cliente_id:
        raise HTTPException(status_code=422, detail="cliente_id é obrigatório.")
    if not reuniao.data_reuniao:
        raise HTTPException(status_code=422, detail="data_reuniao é obrigatória.")
    if not reuniao.descricao:
        raise HTTPException(status_code=422, detail="descricao é obrigatória.")

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

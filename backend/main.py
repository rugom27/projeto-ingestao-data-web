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
    raise RuntimeError(
        "A variável de ambiente DATABASE_URL não está configurada no .env ou no ambiente."
    )

# Inicializar o FastAPI
app = FastAPI()


# Conexão com a base de dados
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao conectar à base de dados: {e}"
        )


# Modelo de dados para a reunião
class ReuniaoData(BaseModel):
    def __init__(
        self,
        cliente_id: int,
        data_reuniao: str,
        descricao: str,
        houve_venda: str,
        produto_id: int = None,
        quantidade_vendida: int = None,
        preco_vendido: float = None,
        razao_nao_venda: str = None,
    ):
        self.cliente_id = cliente_id
        self.data_reuniao = data_reuniao
        self.descricao = descricao
        self.houve_venda = houve_venda
        self.produto_id = produto_id
        self.quantidade_vendida = quantidade_vendida
        self.preco_vendido = preco_vendido
        self.razao_nao_venda = razao_nao_venda

    # Empty constructor
    def __init__(self):
        self.cliente_id = None
        self.data_reuniao = None
        self.descricao = None
        self.houve_venda = None
        self.produto_id = None
        self.quantidade_vendida = None
        self.preco_vendido = None
        self.razao_nao_venda = None


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
        raise HTTPException(status_code=500, detail=f"Erro ao procurar clientes: {e}")
    finally:
        cursor.close()
        conn.close()


# Listar reunioes
@app.get("/reunioes")
async def listar_reunioes(cliente_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if not cliente_id:
            raise HTTPException(
                status_code=400, detail="O parâmetro cliente_id é obrigatório."
            )

        cursor.execute("SELECT * FROM reunioes WHERE cliente_id = %s", (cliente_id,))
        reunioes = cursor.fetchall()
        if not reunioes:
            return {"message": "Não existem reuniões para este cliente."}
        return reunioes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao procurar reuniões: {e}")
    finally:
        cursor.close()
        conn.close()


# Endpoint para inserir reunião
@app.post("/reunioes")
async def inserir_reuniao(reuniao: dict):
    print("teste1")
    print(reuniao)
    print(reuniao.cliente_id)
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
            ),
        )
        conn.commit()
        return {"message": "Reunião registada com sucesso!"}
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
        raise HTTPException(status_code=500, detail=f"Erro ao procurar produtos: {e}")
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
            (produto.ref,),
        )
        conn.commit()
        return {"message": "Produto registado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

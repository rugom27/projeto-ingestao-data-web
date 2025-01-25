import sqlite3

DB_PATH = "data/operational_database.db"


def create_tables():
    """Cria as tabelas necessárias no banco de dados."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)

    cursor = conn.cursor()

    # Tabela de clientes
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS clientes (
        numero_cliente TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        cod_postal TEXT,
        tipo_cliente TEXT,
        ranking TEXT,
        cultura TEXT,
        area_culturas REAL,
        responsavel_principal TEXT,
        responsavel_secundario TEXT,
        distrito TEXT,
        latitude REAL,
        longitude REAL
    )
    """
    )

    # Tabela de vendas
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_de_cliente TEXT NOT NULL,
        ref TEXT,
        design TEXT,
        data TEXT NOT NULL,
        quant INTEGER NOT NULL,
        eur REAL NOT NULL,
        FOREIGN KEY(numero_de_cliente) REFERENCES clientes(numero_cliente)
    )
    """
    )

    conn.commit()
    conn.close()


def insert_cliente(data):
    """Insere um novo cliente na tabela."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
    INSERT INTO clientes (
        numero_cliente, name, cod_postal, tipo_cliente, ranking, cultura, area_culturas,
        responsavel_principal, responsavel_secundario, distrito, latitude, longitude
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            data["numero_cliente"],
            data["name"],
            data["cod_postal"],
            data["tipo_cliente"],
            data["ranking"],
            data["cultura"],
            data["area_culturas"],
            data["responsavel_principal"],
            data["responsavel_secundario"],
            data["distrito"],
            data["latitude"],
            data["longitude"],
        ),
    )
    conn.commit()
    conn.close()


def insert_venda(data):
    """Insere uma nova venda na tabela."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Verifica se numero_de_cliente não está vazio
        if not data["numero_de_cliente"]:
            raise ValueError("numero_de_cliente não pode estar vazio!")

        cursor.execute(
            """
            INSERT INTO vendas (
                numero_de_cliente, ref, design, data, quant, eur
            ) VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                data["numero_de_cliente"],
                data["ref"],
                data["design"],
                data["data"],
                data["quant"],
                data["eur"],
            ),
        )
        conn.commit()
    finally:
        conn.close()


def get_clientes():
    """Obtém a lista de clientes."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT numero_cliente, name FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes


# Inicializar tabelas caso não existam
create_tables()

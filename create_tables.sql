-- Tabela de clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    numero_cliente TEXT UNIQUE, -- Agora permite NULL
    cod_postal VARCHAR(20),
    tipo_cliente VARCHAR(50),
    ranking INT,
    cultura VARCHAR(100),
    area_culturas FLOAT,
    responsavel_principal VARCHAR(100),
    responsavel_secundario VARCHAR(100),
    distrito VARCHAR(50),
    latitude FLOAT,
    longitude FLOAT
);

ALTER TABLE clientes
DROP COLUMN ranking;


-- Tabela de vendas
CREATE TABLE vendas (
    id SERIAL PRIMARY KEY,
    indice INT,
    nome VARCHAR(100),
    ref VARCHAR(50),
    design VARCHAR(100),
    data DATE,
    quant INT,
    eur FLOAT,
    numero_de_cliente TEXT, -- Alterado para TEXT e permite NULL
    FOREIGN KEY (numero_de_cliente) REFERENCES clientes(numero_cliente) -- Permite referenciar NULL
);

-- Tabela de reuniões
CREATE TABLE reunioes (
    id SERIAL PRIMARY KEY,
    cliente_id INT,
    data_reuniao DATE,
    descricao TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Tabela de clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    numero_cliente TEXT UNIQUE, -- Agora permite NULL
    cod_postal VARCHAR(100),
    tipo_cliente VARCHAR(50),
    cultura VARCHAR(100),
    area_culturas VARCHAR(100),
    responsavel_principal VARCHAR(100),
    responsavel_secundario VARCHAR(100),
    distrito VARCHAR(50),
    latitude FLOAT,
    longitude FLOAT
);


-- Tabela de vendas
CREATE TABLE vendas (
    id SERIAL PRIMARY KEY,
    indice INT,
    nome VARCHAR(100),
    ref VARCHAR(100),
    design VARCHAR(100),
    data TEXT,
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


ALTER TABLE vendas DROP CONSTRAINT vendas_numero_de_cliente_fkey;



-- Remover a chave estrangeira existente na tabela vendas
ALTER TABLE vendas
DROP CONSTRAINT IF EXISTS fk_produto;

-- Remover a coluna produto_id da tabela vendas, se necessário
ALTER TABLE vendas
DROP COLUMN IF EXISTS produto_id;

-- Corrigir a tabela produtos para usar a coluna correta (design)
TRUNCATE TABLE produtos; -- Limpar a tabela produtos para reprocessar os dados

-- Inserir valores distintos da coluna "design" da tabela vendas na tabela produtos
INSERT INTO produtos (ref)
SELECT DISTINCT design -- Usar a coluna correta
FROM vendas;

-- Alterar a tabela vendas para adicionar novamente a coluna produto_id e configurar a chave estrangeira
ALTER TABLE vendas
ADD COLUMN produto_id INT,
ADD CONSTRAINT fk_produto
    FOREIGN KEY (produto_id) REFERENCES produtos(produto_id);

-- Atualizar a tabela vendas para preencher a coluna produto_id com base na correspondência de "design"
UPDATE vendas
SET produto_id = p.produto_id
FROM produtos p
WHERE vendas.design = p.ref;

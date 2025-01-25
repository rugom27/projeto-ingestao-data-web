"""
Módulo principal da aplicação.

Responsável por inicializar e configurar o ambiente da aplicação.
"""

from .database import create_tables, insert_cliente, insert_venda, get_clientes

__all__ = [
    "create_tables",
    "insert_cliente",
    "insert_venda",
    "get_clientes",
]

# Inicialização das tabelas ao importar o módulo
create_tables()

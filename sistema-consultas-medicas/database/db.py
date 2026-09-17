"""
Camada de conexao com o MySQL.
Todos os models usam get_connection() para abrir uma conexao por operacao.
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


def get_connection():
    """Abre e retorna uma nova conexao com o banco de dados MySQL."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as erro:
        print(f"[ERRO] Nao foi possivel conectar ao MySQL: {erro}")
        raise

"""
Configuracao de acesso ao banco de dados MySQL.

Edite os valores abaixo de acordo com a sua instalacao local do MySQL
(os mesmos dados usados na extensao Database Client do VS Code).
"""

import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "sua_senha_aqui"),
    "database": os.getenv("DB_NAME", "clinica_consultas"),
}

# Chave usada pelo Flask para sessao/flash messages.
SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta-troque-em-producao")

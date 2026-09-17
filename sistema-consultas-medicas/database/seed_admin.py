"""
Script utilitario para criar o primeiro usuario ADMINISTRADOR.

Execute uma unica vez, a partir da raiz do projeto:
    python -m database.seed_admin
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from werkzeug.security import generate_password_hash
from database.db import get_connection


def criar_admin(nome="Administrador do Sistema", email="admin@clinica.com", senha="admin123"):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT idUsuario FROM usuario WHERE email = %s", (email,))
        if cursor.fetchone():
            print(f"Usuario '{email}' ja existe. Nada foi alterado.")
            return

        senha_hash = generate_password_hash(senha)
        cursor.execute(
            """INSERT INTO usuario (nome, email, senha, perfil, ativo)
               VALUES (%s, %s, %s, 'ADMINISTRADOR', 1)""",
            (nome, email, senha_hash),
        )
        conn.commit()
        print(f"Usuario administrador criado com sucesso!")
        print(f"  E-mail: {email}")
        print(f"  Senha:  {senha}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    criar_admin()

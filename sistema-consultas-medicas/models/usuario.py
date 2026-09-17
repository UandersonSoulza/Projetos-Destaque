"""Model: Usuario (RF01, RF02, RF03 / RN01, RN02)."""

from mysql.connector import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_connection


class Usuario:
    def __init__(self, id_usuario=None, nome=None, email=None, perfil=None,
                 ativo=True, data_cadastro=None):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self.perfil = perfil
        self.ativo = ativo
        self.data_cadastro = data_cadastro

    # ---------- Cadastrar ----------
    @staticmethod
    def criar(nome, email, senha, perfil):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            senha_hash = generate_password_hash(senha)
            cursor.execute(
                """INSERT INTO usuario (nome, email, senha, perfil, ativo)
                   VALUES (%s, %s, %s, %s, 1)""",
                (nome, email, senha_hash, perfil),
            )
            conn.commit()
            return cursor.lastrowid
        except IntegrityError:
            conn.rollback()
            raise ValueError("Ja existe um usuario cadastrado com este e-mail.")
        finally:
            cursor.close()
            conn.close()

    # ---------- Listar ----------
    @staticmethod
    def listar_todos():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT idUsuario, nome, email, perfil, ativo, dataCadastro "
                "FROM usuario ORDER BY nome"
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ---------- Buscar por codigo ----------
    @staticmethod
    def buscar_por_id(id_usuario):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT idUsuario, nome, email, perfil, ativo, dataCadastro "
                "FROM usuario WHERE idUsuario = %s",
                (id_usuario,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    # ---------- Buscar por e-mail (usado no login) ----------
    @staticmethod
    def buscar_por_email(email):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    # ---------- Autenticar (RF01) ----------
    @staticmethod
    def autenticar(email, senha):
        usuario = Usuario.buscar_por_email(email)
        if not usuario:
            return None
        if not usuario["ativo"]:
            return None
        if not check_password_hash(usuario["senha"], senha):
            return None
        usuario.pop("senha", None)
        return usuario

    # ---------- Alterar ----------
    @staticmethod
    def atualizar(id_usuario, nome, email, perfil):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE usuario SET nome=%s, email=%s, perfil=%s WHERE idUsuario=%s",
                (nome, email, perfil, id_usuario),
            )
            conn.commit()
            return cursor.rowcount
        except IntegrityError:
            conn.rollback()
            raise ValueError("Ja existe um usuario cadastrado com este e-mail.")
        finally:
            cursor.close()
            conn.close()

    # ---------- Ativar / desativar ----------
    @staticmethod
    def alternar_status(id_usuario):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE usuario SET ativo = NOT ativo WHERE idUsuario = %s", (id_usuario,)
            )
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

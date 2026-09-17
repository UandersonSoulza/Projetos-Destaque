"""Model: Paciente (RF04, RF05, RF06 / RN03)."""

from mysql.connector import IntegrityError
from database.db import get_connection


class Paciente:
    def __init__(self, id_paciente=None, nome=None, cpf=None, data_nascimento=None,
                 telefone=None, email=None, endereco=None):
        self.id_paciente = id_paciente
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.email = email
        self.endereco = endereco

    # ---------- Cadastrar ----------
    @staticmethod
    def criar(nome, cpf, data_nascimento, telefone, email, endereco):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO paciente (nome, cpf, dataNascimento, telefone, email, endereco)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (nome, cpf, data_nascimento, telefone, email, endereco),
            )
            conn.commit()
            return cursor.lastrowid
        except IntegrityError:
            conn.rollback()
            raise ValueError("Ja existe um paciente cadastrado com este CPF.")
        finally:
            cursor.close()
            conn.close()

    # ---------- Listar ----------
    @staticmethod
    def listar_todos():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM paciente ORDER BY nome")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ---------- Buscar por codigo ----------
    @staticmethod
    def buscar_por_id(id_paciente):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM paciente WHERE idPaciente = %s", (id_paciente,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    # ---------- Buscar por nome ----------
    @staticmethod
    def buscar_por_nome(nome):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM paciente WHERE nome LIKE %s ORDER BY nome", (f"%{nome}%",)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ---------- Busca unificada: codigo, nome ou CPF ----------
    @staticmethod
    def buscar(termo):
        """RF05: busca por codigo (idPaciente) ou por nome/CPF."""
        termo = (termo or "").strip()
        if termo.isdigit():
            encontrado = Paciente.buscar_por_id(int(termo))
            if encontrado:
                return [encontrado]
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT * FROM paciente
                   WHERE nome LIKE %s OR cpf LIKE %s
                   ORDER BY nome""",
                (f"%{termo}%", f"%{termo}%"),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ---------- Alterar ----------
    @staticmethod
    def atualizar(id_paciente, nome, cpf, data_nascimento, telefone, email, endereco):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """UPDATE paciente
                   SET nome=%s, cpf=%s, dataNascimento=%s, telefone=%s, email=%s, endereco=%s
                   WHERE idPaciente=%s""",
                (nome, cpf, data_nascimento, telefone, email, endereco, id_paciente),
            )
            conn.commit()
            return cursor.rowcount
        except IntegrityError:
            conn.rollback()
            raise ValueError("Ja existe um paciente cadastrado com este CPF.")
        finally:
            cursor.close()
            conn.close()

    # ---------- Excluir ----------
    @staticmethod
    def excluir(id_paciente):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM paciente WHERE idPaciente = %s", (id_paciente,))
            conn.commit()
            return cursor.rowcount
        except IntegrityError:
            conn.rollback()
            # RN10: impedir exclusao de paciente com consultas/exames vinculados
            raise ValueError(
                "Nao e possivel excluir este paciente pois ele possui "
                "consultas ou exames registrados."
            )
        finally:
            cursor.close()
            conn.close()

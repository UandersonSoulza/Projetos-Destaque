"""Model: Medico (RF07, RF08, RF09 / RN04)."""

from mysql.connector import IntegrityError
from database.db import get_connection


class Medico:
    def __init__(self, id_medico=None, nome=None, crm=None, especialidade=None,
                 telefone=None, email=None, id_usuario=None):
        self.id_medico = id_medico
        self.nome = nome
        self.crm = crm
        self.especialidade = especialidade
        self.telefone = telefone
        self.email = email
        self.id_usuario = id_usuario

    # ---------- Cadastrar ----------
    @staticmethod
    def criar(nome, crm, especialidade, telefone, email, id_usuario=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO medico (nome, crm, especialidade, telefone, email, idUsuario)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (nome, crm, especialidade, telefone, email, id_usuario),
            )
            conn.commit()
            return cursor.lastrowid
        except IntegrityError:
            conn.rollback()
            raise ValueError("Ja existe um medico cadastrado com este CRM.")
        finally:
            cursor.close()
            conn.close()

    # ---------- Listar ----------
    @staticmethod
    def listar_todos():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM medico ORDER BY nome")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ---------- Buscar por codigo ----------
    @staticmethod
    def buscar_por_id(id_medico):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM medico WHERE idMedico = %s", (id_medico,))
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
                "SELECT * FROM medico WHERE nome LIKE %s ORDER BY nome", (f"%{nome}%",)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ---------- Buscar por especialidade ----------
    @staticmethod
    def buscar_por_especialidade(especialidade):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM medico WHERE especialidade LIKE %s ORDER BY nome",
                (f"%{especialidade}%",),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ---------- Busca unificada: codigo, nome ou CRM ----------
    @staticmethod
    def buscar(termo):
        """RF08: busca por codigo (idMedico) ou por nome/CRM."""
        termo = (termo or "").strip()
        if termo.isdigit():
            encontrado = Medico.buscar_por_id(int(termo))
            if encontrado:
                return [encontrado]
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT * FROM medico
                   WHERE nome LIKE %s OR crm LIKE %s
                   ORDER BY nome""",
                (f"%{termo}%", f"%{termo}%"),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ---------- Buscar por idUsuario (visao "meus dados" do proprio medico) ----------
    @staticmethod
    def buscar_por_usuario(id_usuario):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM medico WHERE idUsuario = %s", (id_usuario,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    # ---------- Alterar ----------
    @staticmethod
    def atualizar(id_medico, nome, crm, especialidade, telefone, email, id_usuario=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """UPDATE medico
                   SET nome=%s, crm=%s, especialidade=%s, telefone=%s, email=%s, idUsuario=%s
                   WHERE idMedico=%s""",
                (nome, crm, especialidade, telefone, email, id_usuario, id_medico),
            )
            conn.commit()
            return cursor.rowcount
        except IntegrityError:
            conn.rollback()
            raise ValueError("Ja existe um medico cadastrado com este CRM.")
        finally:
            cursor.close()
            conn.close()

    # ---------- Excluir ----------
    @staticmethod
    def excluir(id_medico):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM medico WHERE idMedico = %s", (id_medico,))
            conn.commit()
            return cursor.rowcount
        except IntegrityError:
            conn.rollback()
            # RN10: impedir exclusao de medico com consultas/exames vinculados
            raise ValueError(
                "Nao e possivel excluir este medico pois ele possui "
                "consultas ou exames registrados."
            )
        finally:
            cursor.close()
            conn.close()

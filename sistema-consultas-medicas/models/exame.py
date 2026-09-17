"""Model: Exame (RF14, RF15, RF16 / RN11, RN12)."""

from mysql.connector import IntegrityError
from database.db import get_connection

STATUS_VALIDOS = ("SOLICITADO", "AGENDADO", "REALIZADO", "CANCELADO")


class Exame:
    def __init__(self, id_exame=None, nome=None, tipo=None, data_solicitacao=None,
                 data_realizacao=None, resultado=None, observacoes=None, status="SOLICITADO",
                 id_paciente=None, id_medico=None, id_consulta=None, id_usuario=None):
        self.id_exame = id_exame
        self.nome = nome
        self.tipo = tipo
        self.data_solicitacao = data_solicitacao
        self.data_realizacao = data_realizacao
        self.resultado = resultado
        self.observacoes = observacoes
        self.status = status
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.id_consulta = id_consulta
        self.id_usuario = id_usuario

    # ---------- Solicitar (RF14) ----------
    @staticmethod
    def criar(nome, tipo, observacoes, id_paciente, id_medico, id_consulta=None, id_usuario=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO exame
                   (nome, tipo, observacoes, status, idPaciente, idMedico, idConsulta, idUsuario)
                   VALUES (%s, %s, %s, 'SOLICITADO', %s, %s, %s, %s)""",
                (nome, tipo, observacoes, id_paciente, id_medico, id_consulta, id_usuario),
            )
            conn.commit()
            return cursor.lastrowid
        except IntegrityError:
            conn.rollback()
            raise ValueError(
                "Nao foi possivel solicitar o exame: verifique paciente, medico e consulta informados."
            )
        finally:
            cursor.close()
            conn.close()

    # ---------- Consultar (RF16) ----------
    @staticmethod
    def listar_todos():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT e.*, p.nome AS nomePaciente, m.nome AS nomeMedico
                   FROM exame e
                   JOIN paciente p ON p.idPaciente = e.idPaciente
                   JOIN medico m ON m.idMedico = e.idMedico
                   ORDER BY e.dataSolicitacao DESC"""
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(id_exame):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT e.*, p.nome AS nomePaciente, m.nome AS nomeMedico
                   FROM exame e
                   JOIN paciente p ON p.idPaciente = e.idPaciente
                   JOIN medico m ON m.idMedico = e.idMedico
                   WHERE e.idExame = %s""",
                (id_exame,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_paciente(nome_paciente):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT e.*, p.nome AS nomePaciente, m.nome AS nomeMedico
                   FROM exame e
                   JOIN paciente p ON p.idPaciente = e.idPaciente
                   JOIN medico m ON m.idMedico = e.idMedico
                   WHERE p.nome LIKE %s
                   ORDER BY e.dataSolicitacao DESC""",
                (f"%{nome_paciente}%",),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ---------- Registrar resultado (RF15) ----------
    @staticmethod
    def registrar_resultado(id_exame, data_realizacao, resultado, status="REALIZADO"):
        if status not in STATUS_VALIDOS:
            raise ValueError("Status invalido para exame.")
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """UPDATE exame
                   SET dataRealizacao=%s, resultado=%s, status=%s
                   WHERE idExame=%s""",
                (data_realizacao, resultado, status, id_exame),
            )
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ---------- Alterar dados gerais ----------
    @staticmethod
    def atualizar(id_exame, nome, tipo, observacoes, status):
        if status not in STATUS_VALIDOS:
            raise ValueError("Status invalido para exame.")
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE exame SET nome=%s, tipo=%s, observacoes=%s, status=%s WHERE idExame=%s",
                (nome, tipo, observacoes, status, id_exame),
            )
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ---------- Excluir ----------
    @staticmethod
    def excluir(id_exame):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM exame WHERE idExame = %s", (id_exame,))
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

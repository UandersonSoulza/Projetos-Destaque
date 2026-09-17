"""Model: Consulta (RF10-RF13 / RN05-RN10)."""

from datetime import date
from mysql.connector import IntegrityError
from database.db import get_connection

STATUS_VALIDOS = ("AGENDADA", "REALIZADA", "CANCELADA")


class Consulta:
    def __init__(self, id_consulta=None, data_consulta=None, hora_consulta=None,
                 status="AGENDADA", motivo=None, observacoes=None,
                 id_paciente=None, id_medico=None, id_usuario=None):
        self.id_consulta = id_consulta
        self.data_consulta = data_consulta
        self.hora_consulta = hora_consulta
        self.status = status
        self.motivo = motivo
        self.observacoes = observacoes
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.id_usuario = id_usuario

    # ---------- Validacoes de negocio ----------
    @staticmethod
    def _validar_data(data_consulta):
        # RN07: a data nao pode ser anterior a data atual
        if isinstance(data_consulta, str):
            data_obj = date.fromisoformat(data_consulta)
        else:
            data_obj = data_consulta
        if data_obj < date.today():
            raise ValueError("A data da consulta nao pode ser anterior a data atual.")

    @staticmethod
    def _medico_ocupado(id_medico, data_consulta, hora_consulta, ignorar_id=None):
        # RN06: um medico nao pode ter duas consultas no mesmo dia/horario
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = """SELECT idConsulta FROM consulta
                     WHERE idMedico = %s AND dataConsulta = %s AND horaConsulta = %s
                       AND status <> 'CANCELADA'"""
            params = [id_medico, data_consulta, hora_consulta]
            if ignorar_id:
                sql += " AND idConsulta <> %s"
                params.append(ignorar_id)
            cursor.execute(sql, tuple(params))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

    # ---------- Agendar (RF10) ----------
    @staticmethod
    def criar(data_consulta, hora_consulta, motivo, observacoes, id_paciente, id_medico, id_usuario=None):
        Consulta._validar_data(data_consulta)
        if Consulta._medico_ocupado(id_medico, data_consulta, hora_consulta):
            raise ValueError("Este medico ja possui uma consulta agendada nesta data e horario.")

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO consulta
                   (dataConsulta, horaConsulta, status, motivo, observacoes,
                    idPaciente, idMedico, idUsuario)
                   VALUES (%s, %s, 'AGENDADA', %s, %s, %s, %s, %s)""",
                (data_consulta, hora_consulta, motivo, observacoes,
                 id_paciente, id_medico, id_usuario),
            )
            conn.commit()
            return cursor.lastrowid
        except IntegrityError:
            conn.rollback()
            raise ValueError(
                "Nao foi possivel agendar: verifique se o paciente e o medico "
                "informados existem, ou se o horario ja esta ocupado."
            )
        finally:
            cursor.close()
            conn.close()

    # ---------- Listar (RF11) ----------
    @staticmethod
    def listar_todas():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT c.*, p.nome AS nomePaciente, m.nome AS nomeMedico
                   FROM consulta c
                   JOIN paciente p ON p.idPaciente = c.idPaciente
                   JOIN medico m ON m.idMedico = c.idMedico
                   ORDER BY c.dataConsulta DESC, c.horaConsulta DESC"""
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(id_consulta):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT c.*, p.nome AS nomePaciente, m.nome AS nomeMedico
                   FROM consulta c
                   JOIN paciente p ON p.idPaciente = c.idPaciente
                   JOIN medico m ON m.idMedico = c.idMedico
                   WHERE c.idConsulta = %s""",
                (id_consulta,),
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
                """SELECT c.*, p.nome AS nomePaciente, m.nome AS nomeMedico
                   FROM consulta c
                   JOIN paciente p ON p.idPaciente = c.idPaciente
                   JOIN medico m ON m.idMedico = c.idMedico
                   WHERE p.nome LIKE %s
                   ORDER BY c.dataConsulta DESC""",
                (f"%{nome_paciente}%",),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_medico(nome_medico):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT c.*, p.nome AS nomePaciente, m.nome AS nomeMedico
                   FROM consulta c
                   JOIN paciente p ON p.idPaciente = c.idPaciente
                   JOIN medico m ON m.idMedico = c.idMedico
                   WHERE m.nome LIKE %s
                   ORDER BY c.dataConsulta DESC""",
                (f"%{nome_medico}%",),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_data(data_consulta):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """SELECT c.*, p.nome AS nomePaciente, m.nome AS nomeMedico
                   FROM consulta c
                   JOIN paciente p ON p.idPaciente = c.idPaciente
                   JOIN medico m ON m.idMedico = c.idMedico
                   WHERE c.dataConsulta = %s
                   ORDER BY c.horaConsulta""",
                (data_consulta,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ---------- Alterar ----------
    @staticmethod
    def atualizar(id_consulta, data_consulta, hora_consulta, motivo, observacoes,
                  id_paciente, id_medico):
        Consulta._validar_data(data_consulta)
        if Consulta._medico_ocupado(id_medico, data_consulta, hora_consulta, ignorar_id=id_consulta):
            raise ValueError("Este medico ja possui uma consulta agendada nesta data e horario.")

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """UPDATE consulta
                   SET dataConsulta=%s, horaConsulta=%s, motivo=%s, observacoes=%s,
                       idPaciente=%s, idMedico=%s
                   WHERE idConsulta=%s""",
                (data_consulta, hora_consulta, motivo, observacoes,
                 id_paciente, id_medico, id_consulta),
            )
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ---------- Atender: mudar status (RF12) ----------
    @staticmethod
    def atualizar_status(id_consulta, novo_status, observacoes=None):
        if novo_status not in STATUS_VALIDOS:
            raise ValueError("Status invalido. Use AGENDADA, REALIZADA ou CANCELADA.")

        conn = get_connection()
        cursor = conn.cursor()
        try:
            if observacoes is not None:
                cursor.execute(
                    "UPDATE consulta SET status=%s, observacoes=%s WHERE idConsulta=%s",
                    (novo_status, observacoes, id_consulta),
                )
            else:
                cursor.execute(
                    "UPDATE consulta SET status=%s WHERE idConsulta=%s",
                    (novo_status, id_consulta),
                )
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()

    # ---------- Cancelar (RF13 / RN09: mantem o registro) ----------
    @staticmethod
    def cancelar(id_consulta):
        return Consulta.atualizar_status(id_consulta, "CANCELADA")

    # ---------- Excluir definitivamente (RF13) ----------
    @staticmethod
    def excluir(id_consulta):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM consulta WHERE idConsulta = %s", (id_consulta,))
            conn.commit()
            return cursor.rowcount
        except IntegrityError:
            conn.rollback()
            raise ValueError(
                "Nao e possivel excluir esta consulta pois existe um exame vinculado a ela."
            )
        finally:
            cursor.close()
            conn.close()

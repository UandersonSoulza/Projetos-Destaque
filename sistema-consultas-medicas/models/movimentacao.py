"""Model: Movimentacao (Log de Movimentacoes / auditoria do sistema).

Registra automaticamente as principais acoes realizadas no sistema
(login, cadastros, agendamentos, cancelamentos, exclusoes etc.) para
que o Administrador possa acompanhar tudo o que acontece na aplicacao.
"""

from database.db import get_connection


class Movimentacao:
    def __init__(self, id_movimentacao=None, tipo=None, entidade=None,
                 descricao=None, autor=None, id_usuario=None, data_hora=None):
        self.id_movimentacao = id_movimentacao
        self.tipo = tipo
        self.entidade = entidade
        self.descricao = descricao
        self.autor = autor
        self.id_usuario = id_usuario
        self.data_hora = data_hora

    # ---------- Registrar uma nova movimentacao ----------
    @staticmethod
    def registrar(tipo, entidade, descricao, autor, id_usuario=None):
        """Grava uma linha no log. Nunca deve derrubar a acao principal:
        qualquer erro aqui e apenas impresso no console."""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO movimentacao (tipo, entidade, descricao, autor, idUsuario)
                   VALUES (%s, %s, %s, %s, %s)""",
                (tipo, entidade, descricao, autor, id_usuario),
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as erro:  # nao deve interromper o fluxo principal
            print(f"[AVISO] Falha ao registrar movimentacao: {erro}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ---------- Listar (mais recentes primeiro) ----------
    @staticmethod
    def listar(termo="", entidade="", limite=200):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM movimentacao WHERE 1=1"
            parametros = []

            if entidade:
                sql += " AND entidade = %s"
                parametros.append(entidade)

            if termo:
                sql += " AND (descricao LIKE %s OR autor LIKE %s OR tipo LIKE %s)"
                like = f"%{termo}%"
                parametros.extend([like, like, like])

            sql += " ORDER BY dataHora DESC, idMovimentacao DESC LIMIT %s"
            parametros.append(limite)

            cursor.execute(sql, tuple(parametros))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # ---------- Contagem total (para o cabecalho da pagina) ----------
    @staticmethod
    def contar_total():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM movimentacao")
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()

"""Rotas: Consulta (RF10, RF11, RF12, RF13)."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.consulta import Consulta
from models.paciente import Paciente
from models.medico import Medico
from models.movimentacao import Movimentacao
from routes.auth import login_required, perfil_required

consulta_bp = Blueprint("consulta", __name__)

# RF10/RF13: agendar, alterar via agenda e cancelar/excluir sao acoes de
# Atendente e Administrador. O Medico tambem pode alterar (RF12: atender
# e registrar observacoes), mas nao agenda nem exclui.
PERFIS_AGENDAM = ("ADMINISTRADOR", "ATENDENTE")
PERFIS_ALTERAM = ("ADMINISTRADOR", "ATENDENTE", "MEDICO")


@consulta_bp.route("/consultas")
@login_required
def listar():
    filtro_tipo = request.args.get("filtro_tipo", "")
    termo = request.args.get("busca", "").strip()

    if termo and (filtro_tipo == "codigo" or (not filtro_tipo and termo.isdigit())):
        encontrada = Consulta.buscar_por_id(int(termo)) if termo.isdigit() else None
        consultas = [encontrada] if encontrada else []
    elif termo and filtro_tipo == "paciente":
        consultas = Consulta.buscar_por_paciente(termo)
    elif termo and filtro_tipo == "medico":
        consultas = Consulta.buscar_por_medico(termo)
    elif termo and filtro_tipo == "data":
        consultas = Consulta.buscar_por_data(termo)
    else:
        consultas = Consulta.listar_todas()

    return render_template(
        "consultas.html",
        consultas=consultas,
        pacientes=Paciente.listar_todos(),
        medicos=Medico.listar_todos(),
        busca=termo,
        filtro_tipo=filtro_tipo,
    )


@consulta_bp.route("/consultas/novo", methods=["POST"])
@perfil_required(*PERFIS_AGENDAM)
def criar():
    try:
        id_paciente = request.form["idPaciente"]
        Consulta.criar(
            data_consulta=request.form["dataConsulta"],
            hora_consulta=request.form["horaConsulta"],
            motivo=request.form.get("motivo", "").strip(),
            observacoes=request.form.get("observacoes", "").strip(),
            id_paciente=id_paciente,
            id_medico=request.form["idMedico"],
            id_usuario=session.get("usuario_id"),
        )
        paciente = Paciente.buscar_por_id(id_paciente)
        nome_paciente = paciente["nome"] if paciente else f"#{id_paciente}"
        Movimentacao.registrar(
            tipo="AGENDAMENTO", entidade="CONSULTA",
            descricao=f"Consulta agendada para {nome_paciente}",
            autor=session.get("usuario_nome", "Sistema"),
            id_usuario=session.get("usuario_id"),
        )
        flash("Consulta agendada com sucesso.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("consulta.listar"))


@consulta_bp.route("/consultas/<int:id_consulta>/editar", methods=["POST"])
@perfil_required(*PERFIS_ALTERAM)
def editar(id_consulta):
    try:
        Consulta.atualizar(
            id_consulta=id_consulta,
            data_consulta=request.form["dataConsulta"],
            hora_consulta=request.form["horaConsulta"],
            motivo=request.form.get("motivo", "").strip(),
            observacoes=request.form.get("observacoes", "").strip(),
            id_paciente=request.form["idPaciente"],
            id_medico=request.form["idMedico"],
        )
        flash("Consulta atualizada com sucesso.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("consulta.listar"))


@consulta_bp.route("/consultas/<int:id_consulta>/status", methods=["POST"])
@perfil_required(*PERFIS_ALTERAM)
def atualizar_status(id_consulta):
    try:
        novo_status = request.form["status"]
        Consulta.atualizar_status(
            id_consulta,
            novo_status=novo_status,
            observacoes=request.form.get("observacoes"),
        )
        Movimentacao.registrar(
            tipo="ATUALIZACAO", entidade="CONSULTA",
            descricao=f"Consulta #{id_consulta} atualizada para {novo_status}",
            autor=session.get("usuario_nome", "Sistema"),
            id_usuario=session.get("usuario_id"),
        )
        flash("Status da consulta atualizado.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("consulta.listar"))


@consulta_bp.route("/consultas/<int:id_consulta>/cancelar", methods=["POST"])
@perfil_required(*PERFIS_AGENDAM)
def cancelar(id_consulta):
    Consulta.cancelar(id_consulta)
    Movimentacao.registrar(
        tipo="CANCELAMENTO", entidade="CONSULTA",
        descricao=f"Consulta #{id_consulta} cancelada",
        autor=session.get("usuario_nome", "Sistema"),
        id_usuario=session.get("usuario_id"),
    )
    flash("Consulta cancelada.", "sucesso")
    return redirect(url_for("consulta.listar"))


@consulta_bp.route("/consultas/<int:id_consulta>/excluir", methods=["POST"])
@perfil_required(*PERFIS_AGENDAM)
def excluir(id_consulta):
    try:
        Consulta.excluir(id_consulta)
        Movimentacao.registrar(
            tipo="EXCLUSAO", entidade="CONSULTA",
            descricao=f"Consulta #{id_consulta} excluida",
            autor=session.get("usuario_nome", "Sistema"),
            id_usuario=session.get("usuario_id"),
        )
        flash("Consulta excluida com sucesso.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("consulta.listar"))

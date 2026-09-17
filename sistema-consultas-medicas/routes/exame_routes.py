"""Rotas: Exame (RF14, RF15, RF16)."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.exame import Exame
from models.paciente import Paciente
from models.medico import Medico
from models.consulta import Consulta
from models.movimentacao import Movimentacao
from routes.auth import login_required, perfil_required

exame_bp = Blueprint("exame", __name__)

# RF14: quem solicita/registra resultado/edita e o Medico (e o
# Administrador, por gestao). Atendente e Paciente apenas consultam (RF16).
PERFIS_GERENCIAM_EXAME = ("ADMINISTRADOR", "MEDICO")


@exame_bp.route("/exames")
@login_required
def listar():
    termo = request.args.get("busca", "").strip()
    if termo and termo.isdigit():
        encontrado = Exame.buscar_por_id(int(termo))
        exames = [encontrado] if encontrado else []
    elif termo:
        exames = Exame.buscar_por_paciente(termo)
    else:
        exames = Exame.listar_todos()
    return render_template(
        "exames.html",
        exames=exames,
        pacientes=Paciente.listar_todos(),
        medicos=Medico.listar_todos(),
        consultas=Consulta.listar_todas(),
        busca=termo,
    )


@exame_bp.route("/exames/novo", methods=["POST"])
@perfil_required(*PERFIS_GERENCIAM_EXAME)
def criar():
    try:
        id_consulta = request.form.get("idConsulta") or None
        id_paciente = request.form["idPaciente"]
        nome_exame = request.form["nome"].strip()
        Exame.criar(
            nome=nome_exame,
            tipo=request.form.get("tipo", "").strip(),
            observacoes=request.form.get("observacoes", "").strip(),
            id_paciente=id_paciente,
            id_medico=request.form["idMedico"],
            id_consulta=id_consulta,
            id_usuario=session.get("usuario_id"),
        )
        paciente = Paciente.buscar_por_id(id_paciente)
        nome_paciente = paciente["nome"] if paciente else f"#{id_paciente}"
        Movimentacao.registrar(
            tipo="CADASTRO", entidade="EXAME",
            descricao=f"Exame {nome_exame} solicitado para {nome_paciente}",
            autor=session.get("usuario_nome", "Sistema"),
            id_usuario=session.get("usuario_id"),
        )
        flash("Exame solicitado com sucesso.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("exame.listar"))


@exame_bp.route("/exames/<int:id_exame>/resultado", methods=["POST"])
@perfil_required(*PERFIS_GERENCIAM_EXAME)
def registrar_resultado(id_exame):
    try:
        Exame.registrar_resultado(
            id_exame=id_exame,
            data_realizacao=request.form["dataRealizacao"],
            resultado=request.form.get("resultado", "").strip(),
            status=request.form.get("status", "REALIZADO"),
        )
        Movimentacao.registrar(
            tipo="ATUALIZACAO", entidade="EXAME",
            descricao=f"Resultado do exame #{id_exame} registrado",
            autor=session.get("usuario_nome", "Sistema"),
            id_usuario=session.get("usuario_id"),
        )
        flash("Resultado registrado com sucesso.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("exame.listar"))


@exame_bp.route("/exames/<int:id_exame>/editar", methods=["POST"])
@perfil_required(*PERFIS_GERENCIAM_EXAME)
def editar(id_exame):
    try:
        Exame.atualizar(
            id_exame=id_exame,
            nome=request.form["nome"].strip(),
            tipo=request.form.get("tipo", "").strip(),
            observacoes=request.form.get("observacoes", "").strip(),
            status=request.form["status"],
        )
        flash("Exame atualizado com sucesso.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("exame.listar"))


@exame_bp.route("/exames/<int:id_exame>/excluir", methods=["POST"])
@perfil_required("ADMINISTRADOR")
def excluir(id_exame):
    Exame.excluir(id_exame)
    flash("Exame excluido com sucesso.", "sucesso")
    return redirect(url_for("exame.listar"))

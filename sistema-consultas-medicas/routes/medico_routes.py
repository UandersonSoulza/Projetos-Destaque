"""Rotas: Medico (RF07, RF08, RF09)."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.medico import Medico
from models.movimentacao import Movimentacao
from routes.auth import login_required, perfil_required

medico_bp = Blueprint("medico", __name__)


@medico_bp.route("/medicos")
@login_required
def listar():
    termo = request.args.get("busca", "").strip()
    especialidade = request.args.get("especialidade", "").strip()

    # RF08 / doc. de requisitos: o Medico consulta apenas os seus proprios
    # dados. Administrador e Atendente veem/pesquisam o cadastro completo.
    if session.get("usuario_perfil") == "MEDICO" and not especialidade and not termo:
        proprio = Medico.buscar_por_usuario(session.get("usuario_id"))
        medicos = [proprio] if proprio else []
    elif especialidade:
        medicos = Medico.buscar_por_especialidade(especialidade)
    elif termo:
        medicos = Medico.buscar(termo)
    else:
        medicos = Medico.listar_todos()
    return render_template("medicos.html", medicos=medicos, busca=termo, especialidade=especialidade)


@medico_bp.route("/medicos/novo", methods=["POST"])
@perfil_required("ADMINISTRADOR")
def criar():
    try:
        nome = request.form["nome"].strip()
        Medico.criar(
            nome=nome,
            crm=request.form["crm"].strip(),
            especialidade=request.form["especialidade"].strip(),
            telefone=request.form.get("telefone", "").strip(),
            email=request.form.get("email", "").strip(),
        )
        Movimentacao.registrar(
            tipo="CADASTRO", entidade="MEDICO",
            descricao=f"Medico {nome} cadastrado",
            autor=session.get("usuario_nome", "Sistema"),
            id_usuario=session.get("usuario_id"),
        )
        flash("Medico cadastrado com sucesso.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("medico.listar"))


@medico_bp.route("/medicos/<int:id_medico>/editar", methods=["POST"])
@perfil_required("ADMINISTRADOR", "ATENDENTE")
def editar(id_medico):
    try:
        Medico.atualizar(
            id_medico=id_medico,
            nome=request.form["nome"].strip(),
            crm=request.form["crm"].strip(),
            especialidade=request.form["especialidade"].strip(),
            telefone=request.form.get("telefone", "").strip(),
            email=request.form.get("email", "").strip(),
        )
        flash("Medico atualizado com sucesso.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("medico.listar"))


@medico_bp.route("/medicos/<int:id_medico>/excluir", methods=["POST"])
@perfil_required("ADMINISTRADOR")
def excluir(id_medico):
    try:
        Medico.excluir(id_medico)
        flash("Medico excluido com sucesso.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("medico.listar"))

"""Rotas: Paciente (RF04, RF05, RF06)."""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.paciente import Paciente
from models.movimentacao import Movimentacao
from routes.auth import login_required, perfil_required

paciente_bp = Blueprint("paciente", __name__)

# RF03 / doc. de requisitos: cadastro, alteracao e exclusao de pacientes
# sao responsabilidade de Atendente e Administrador. Medico e Paciente
# podem apenas consultar (RF05, "visualizar dados do paciente").
PERFIS_GERENCIAM_PACIENTE = ("ADMINISTRADOR", "ATENDENTE")


@paciente_bp.route("/pacientes")
@login_required
def listar():
    termo = request.args.get("busca", "").strip()
    pacientes = Paciente.buscar(termo) if termo else Paciente.listar_todos()
    return render_template("pacientes.html", pacientes=pacientes, busca=termo)


@paciente_bp.route("/pacientes/novo", methods=["POST"])
@perfil_required(*PERFIS_GERENCIAM_PACIENTE)
def criar():
    try:
        nome = request.form["nome"].strip()
        Paciente.criar(
            nome=nome,
            cpf=request.form["cpf"].strip(),
            data_nascimento=request.form["dataNascimento"],
            telefone=request.form.get("telefone", "").strip(),
            email=request.form.get("email", "").strip(),
            endereco=request.form.get("endereco", "").strip(),
        )
        Movimentacao.registrar(
            tipo="CADASTRO", entidade="PACIENTE",
            descricao=f"Paciente {nome} cadastrado",
            autor=session.get("usuario_nome", "Sistema"),
            id_usuario=session.get("usuario_id"),
        )
        flash("Paciente cadastrado com sucesso.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("paciente.listar"))


@paciente_bp.route("/pacientes/<int:id_paciente>/editar", methods=["POST"])
@perfil_required(*PERFIS_GERENCIAM_PACIENTE)
def editar(id_paciente):
    try:
        Paciente.atualizar(
            id_paciente=id_paciente,
            nome=request.form["nome"].strip(),
            cpf=request.form["cpf"].strip(),
            data_nascimento=request.form["dataNascimento"],
            telefone=request.form.get("telefone", "").strip(),
            email=request.form.get("email", "").strip(),
            endereco=request.form.get("endereco", "").strip(),
        )
        flash("Paciente atualizado com sucesso.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("paciente.listar"))


@paciente_bp.route("/pacientes/<int:id_paciente>/excluir", methods=["POST"])
@perfil_required(*PERFIS_GERENCIAM_PACIENTE)
def excluir(id_paciente):
    try:
        Paciente.excluir(id_paciente)
        flash("Paciente excluido com sucesso.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("paciente.listar"))

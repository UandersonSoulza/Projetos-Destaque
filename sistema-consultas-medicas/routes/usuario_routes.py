"""Rotas: Usuario / Autenticacao (RF01, RF02, RF03)."""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.usuario import Usuario
from models.movimentacao import Movimentacao
from routes.auth import perfil_required

usuario_bp = Blueprint("usuario", __name__)

PERFIS_VALIDOS = {"ADMINISTRADOR", "ATENDENTE", "MEDICO", "PACIENTE"}

# RF03 / seguranca: no autocadastro publico (tela "Criar conta"), NINGUEM
# pode virar Administrador sozinho - senao qualquer visitante poderia
# assumir o controle total do sistema. Administrador so e criado por um
# Administrador ja logado (rota /usuarios/novo) ou pelo seed inicial
# (database/seed_admin.py).
PERFIS_AUTOCADASTRO = {"ATENDENTE", "MEDICO", "PACIENTE"}


@usuario_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        usuario = Usuario.autenticar(email, senha)
        if usuario:
            session["usuario_id"] = usuario["idUsuario"]
            session["usuario_nome"] = usuario["nome"]
            session["usuario_perfil"] = usuario["perfil"]
            Movimentacao.registrar(
                tipo="LOGIN", entidade="SISTEMA",
                descricao="Login realizado com sucesso",
                autor=usuario["email"], id_usuario=usuario["idUsuario"],
            )
            flash(f"Bem-vindo(a), {usuario['nome']}!", "sucesso")
            return redirect(url_for("index"))
        flash("E-mail, senha invalidos ou usuario inativo.", "erro")
    return render_template("login.html")


@usuario_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    """Cadastro publico de conta (tela "Criar conta").

    Qualquer visitante pode criar sua propria conta e escolher o perfil
    de acesso. Ao final, o usuario ja entra autenticado automaticamente.
    """
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        perfil = request.form.get("perfil", "").strip().upper()
        senha = request.form.get("senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")

        dados_form = {"nome": nome, "email": email, "perfil": perfil}

        if not nome or not email or not perfil:
            flash("Preencha todos os campos obrigatorios.", "erro")
            return render_template("registro.html", **dados_form)

        if perfil not in PERFIS_AUTOCADASTRO:
            flash("Selecione um perfil de acesso valido.", "erro")
            return render_template("registro.html", **dados_form)

        if not senha or len(senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "erro")
            return render_template("registro.html", **dados_form)

        if senha != confirmar_senha:
            flash("As senhas informadas nao coincidem.", "erro")
            return render_template("registro.html", **dados_form)

        try:
            id_usuario = Usuario.criar(nome=nome, email=email, senha=senha, perfil=perfil)
        except ValueError as erro:
            flash(str(erro), "erro")
            return render_template("registro.html", **dados_form)

        Movimentacao.registrar(
            tipo="CADASTRO", entidade="USUARIO",
            descricao=f"Conta criada para {email}",
            autor=email, id_usuario=id_usuario,
        )

        # Autentica automaticamente o usuario recem-criado.
        session["usuario_id"] = id_usuario
        session["usuario_nome"] = nome
        session["usuario_perfil"] = perfil
        Movimentacao.registrar(
            tipo="LOGIN", entidade="SISTEMA",
            descricao="Login realizado com sucesso",
            autor=email, id_usuario=id_usuario,
        )

        flash(f"Conta criada com sucesso! Bem-vindo(a), {nome}.", "sucesso")
        return redirect(url_for("index"))

    return render_template("registro.html")


@usuario_bp.route("/logout")
def logout():
    session.clear()
    flash("Sessao encerrada.", "sucesso")
    return redirect(url_for("usuario.login"))


@usuario_bp.route("/usuarios")
@perfil_required("ADMINISTRADOR")
def listar():
    usuarios = Usuario.listar_todos()
    return render_template("usuarios.html", usuarios=usuarios)


@usuario_bp.route("/usuarios/novo", methods=["POST"])
@perfil_required("ADMINISTRADOR")
def criar():
    senha = request.form.get("senha", "")
    if not senha.strip():
        flash("Informe uma senha para o novo usuario.", "erro")
        return redirect(url_for("usuario.listar"))
    try:
        nome = request.form["nome"].strip()
        email = request.form["email"].strip()
        id_usuario = Usuario.criar(
            nome=nome,
            email=email,
            senha=senha,
            perfil=request.form["perfil"],
        )
        Movimentacao.registrar(
            tipo="CADASTRO", entidade="USUARIO",
            descricao=f"Usuario {nome} cadastrado",
            autor=session.get("usuario_nome", "Administrador"),
            id_usuario=session.get("usuario_id"),
        )
        flash("Usuario cadastrado com sucesso.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("usuario.listar"))


@usuario_bp.route("/usuarios/<int:id_usuario>/editar", methods=["POST"])
@perfil_required("ADMINISTRADOR")
def editar(id_usuario):
    try:
        Usuario.atualizar(
            id_usuario=id_usuario,
            nome=request.form["nome"].strip(),
            email=request.form["email"].strip(),
            perfil=request.form["perfil"],
        )
        flash("Usuario atualizado com sucesso.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("usuario.listar"))


@usuario_bp.route("/usuarios/<int:id_usuario>/status", methods=["POST"])
@perfil_required("ADMINISTRADOR")
def alternar_status(id_usuario):
    Usuario.alternar_status(id_usuario)
    flash("Status do usuario atualizado.", "sucesso")
    return redirect(url_for("usuario.listar"))

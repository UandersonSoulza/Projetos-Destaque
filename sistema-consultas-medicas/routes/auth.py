"""Utilitarios de autenticacao/autorizacao usados pelas rotas (RF03)."""

from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    @wraps(f)
    def decorado(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Faca login para continuar.", "erro")
            return redirect(url_for("usuario.login"))
        return f(*args, **kwargs)
    return decorado


def perfil_required(*perfis_permitidos):
    """Restringe o acesso a rota aos perfis informados (ex: ADMINISTRADOR)."""
    def decorator(f):
        @wraps(f)
        def decorado(*args, **kwargs):
            if "usuario_id" not in session:
                flash("Faca login para continuar.", "erro")
                return redirect(url_for("usuario.login"))
            if session.get("usuario_perfil") not in perfis_permitidos:
                flash("Voce nao tem permissao para acessar esta pagina.", "erro")
                return redirect(url_for("index"))
            return f(*args, **kwargs)
        return decorado
    return decorator

"""Rotas: Movimentacao (Log de Movimentacoes / auditoria do sistema)."""

from flask import Blueprint, render_template, request
from models.movimentacao import Movimentacao
from routes.auth import perfil_required

movimentacao_bp = Blueprint("movimentacao", __name__)


@movimentacao_bp.route("/movimentacoes")
@perfil_required("ADMINISTRADOR")
def listar():
    termo = request.args.get("busca", "").strip()
    entidade = request.args.get("entidade", "").strip()
    movimentacoes = Movimentacao.listar(termo=termo, entidade=entidade)
    total = Movimentacao.contar_total()
    return render_template(
        "movimentacoes.html",
        movimentacoes=movimentacoes,
        total=total,
        busca=termo,
        entidade=entidade,
    )

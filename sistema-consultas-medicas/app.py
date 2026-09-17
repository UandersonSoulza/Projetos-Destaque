"""
Sistema de Gerenciamento de Consultas Medicas
Ponto de entrada da aplicacao Flask.
"""

from flask import Flask, render_template, session
from config import SECRET_KEY
from routes.auth import login_required

from routes.usuario_routes import usuario_bp
from routes.paciente_routes import paciente_bp
from routes.medico_routes import medico_bp
from routes.consulta_routes import consulta_bp
from routes.exame_routes import exame_bp
from routes.movimentacao_routes import movimentacao_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(usuario_bp)
app.register_blueprint(paciente_bp)
app.register_blueprint(medico_bp)
app.register_blueprint(consulta_bp)
app.register_blueprint(exame_bp)
app.register_blueprint(movimentacao_bp)


@app.route("/")
@login_required
def index():
    return render_template("index.html", usuario_nome=session.get("usuario_nome"))


@app.context_processor
def variaveis_globais():
    return {
        "usuario_logado": session.get("usuario_nome"),
        "perfil_logado": session.get("usuario_perfil"),
    }


if __name__ == "__main__":
    app.run(debug=True)

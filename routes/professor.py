from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.turma import Turma
from models.aluno import Aluno
from models.aula import Aula
from models.presenca import Presenca
from datetime import datetime

professor_bp = Blueprint('professor', __name__)

# --- GERENCIAMENTO DE TURMAS ---

@professor_bp.route("/turmas")
def listar_turmas():
    turmas = Turma.query.all()
    return render_template("index.html", turmas=turmas)

@professor_bp.route("/turmas/nova", methods=["GET", "POST"])
def criar_turma():
    if request.method == "POST":
        nome = request.form.get("nome")
        carga_horaria = request.form.get("carga_horaria")
        
        nova_turma = Turma(nome=nome, carga_horaria=carga_horaria)
        db.session.add(nova_turma)
        db.session.commit()
        flash("Turma criada com sucesso!", "success")
        return redirect(url_for("professor.listar_turmas"))
    
    return render_template("turma_form.html")

@professor_bp.route("/turmas/<int:id>")
def ver_turma(id):
    turma = Turma.query.get_or_404(id)
    # Ordena as aulas por data
    aulas = Aula.query.filter_by(turma_id=id).order_by(Aula.data_aula.desc()).all()
    return render_template("turma_detalhes.html", turma=turma, aulas=aulas)


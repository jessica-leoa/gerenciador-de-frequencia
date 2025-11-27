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


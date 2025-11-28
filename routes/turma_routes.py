from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.turma_service import (
    create_turma, get_turmas, get_turma, update_turma, delete_turma
)
from services.aula_service import (
    aulas_by_turma, create_aula
)
from services.aluno_service import (
    aluno_existe, create_aluno
)
turma_bp = Blueprint("turmas", __name__)

@turma_bp.post("/nova")
def create():
    data = {}
    data["nome"] = request.form.get("nome")
    data["carga_horaria"] = request.form.get("carga_horaria")
    create_turma(data)
    flash("Turma criada com sucesso!", "success")
    return redirect(url_for("turmas.list_all"))

@turma_bp.get("/nova")
def form():
    return render_template("turma_form.html")

@turma_bp.get("/")
def list_all():
    turmas = get_turmas()
    return render_template("index.html", turmas=turmas)

@turma_bp.get("/<int:id>")
def get_one(id):
    turma = get_turma(id)
    aulas = aulas_by_turma(id)
    return render_template("turma_detalhes.html", turma=turma, aulas=aulas)

@turma_bp.post("/<int:id>")
def update(id):
    data = {}
    data["nome"] = request.form.get("nome")
    data["carga_horaria"] = request.form.get("carga_horaria")
    update_turma(id, data)
    flash("Turma atualizada!", "success")
    return redirect(url_for("turmas.get_one", id=id))

@turma_bp.delete("/<int:id>")
def delete(id):
    delete_turma(id)
    flash("Turma deletada!", "success")
    return redirect(url_for("turmas.list_all"))

@turma_bp.post("/<int:turma_id>/aluno")
def adicionar_aluno(turma_id):
    if aluno_existe(matricula=request.form.get("matricula")):
        flash("Erro: Matrícula já existe no sistema.", "danger")
        return redirect(url_for("turmas.get_one", id=turma_id))
    
    data = {}
    data["nome"] = request.form.get("nome")
    data["matricula"] = request.form.get("matricula")
    data["turma_id"] = turma_id
    create_aluno(data)
    flash("Aluno matriculado com sucesso!", "success")
    return redirect(url_for("turmas.get_one", id=turma_id))

@turma_bp.post("/<int:turma_id>/aula")
def criar_aula(turma_id):
    data = {}
    data_str = request.form.get("data_aula")
    data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
    data["data_aula"] = data_obj
    data["turma_id"] = turma_id
    nova_aula = create_aula(data)

    flash("Aula agendada! Realize a chamada agora.", "success")
    return redirect(url_for("professor.realizar_chamada", aula_id=nova_aula.id))
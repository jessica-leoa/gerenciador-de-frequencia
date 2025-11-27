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

@professor_bp.route("/turmas/<int:id>/editar", methods=["POST"])
def editar_turma(id):
    turma = Turma.query.get_or_404(id)
    turma.nome = request.form.get("nome")
    turma.carga_horaria = request.form.get("carga_horaria")
    db.session.commit()
    flash("Turma atualizada!", "success")
    return redirect(url_for("professor.ver_turma", id=id))

# --- GERENCIAMENTO DE ALUNOS ---

@professor_bp.route("/turmas/<int:turma_id>/aluno/novo", methods=["POST"])
def adicionar_aluno(turma_id):
    nome = request.form.get("nome")
    matricula = request.form.get("matricula")
    
    # Verifica duplicidade simples
    existe = Aluno.query.filter_by(matricula=matricula).first()
    if existe:
        flash("Erro: Matrícula já existe no sistema.", "danger")
        return redirect(url_for("professor.ver_turma", id=turma_id))

    novo_aluno = Aluno(nome=nome, matricula=matricula, turma_id=turma_id)
    db.session.add(novo_aluno)
    db.session.commit()
    flash("Aluno matriculado com sucesso!", "success")
    return redirect(url_for("professor.ver_turma", id=turma_id))

# --- GERENCIAMENTO DE AULAS E CHAMADA ---
@professor_bp.route("/turmas/<int:turma_id>/aula/nova", methods=["POST"])
def criar_aula(turma_id):
    data_str = request.form.get("data_aula")
    data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
    
    nova_aula = Aula(turma_id=turma_id, data_aula=data_obj)
    db.session.add(nova_aula)
    db.session.commit()
    
    flash("Aula agendada! Realize a chamada agora.", "success")
    
    return redirect(url_for("professor.realizar_chamada", aula_id=nova_aula.id))

@professor_bp.route("/aula/<int:aula_id>/chamada", methods=["GET", "POST"])
def realizar_chamada(aula_id):
    aula = Aula.query.get_or_404(aula_id)
    turma = Turma.query.get(aula.turma_id)
    alunos = Aluno.query.filter_by(turma_id=turma.id).all()
    
    if request.method == "POST":
       
        for aluno in alunos:
            
            status_presenca = request.form.get(f"presenca_{aluno.id}") == "on"
            
            registro = Presenca.query.filter_by(aluno_id=aluno.id, aula_id=aula.id).first()
            
            if registro:
                registro.presenca = status_presenca
            else:
                novo_registro = Presenca(
                    aluno_id=aluno.id,
                    aula_id=aula.id,  
                    presenca=status_presenca
                )
                db.session.add(novo_registro)
        
        db.session.commit()
        flash("Chamada salva com sucesso!", "success")
        return redirect(url_for("professor.ver_turma", id=turma.id))

    lista_chamada = []
    for aluno in alunos:
        registro = Presenca.query.filter_by(aluno_id=aluno.id, aula_id=aula.id).first()
        presente = registro.presenca if registro else True 
        lista_chamada.append({
            'aluno': aluno,
            'presente': presente
        })

    return render_template("chamada.html", aula=aula, turma=turma, lista_chamada=lista_chamada)
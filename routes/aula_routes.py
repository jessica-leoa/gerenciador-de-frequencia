from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.aluno import Aluno
from models.turma import Turma
from models.presenca import Presenca
from extensions import db

alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.route("/alunos")
def listar_alunos():
    """Lista todos os alunos"""
    lista_alunos = Aluno.query.all()
    turmas = Turma.query.all()
    return render_template("alunos.html", lista_alunos=lista_alunos, turmas=turmas)

@alunos_bp.route("/alunos/adicionar", methods=["POST"])
def adicionar_aluno():
    """Adiciona um novo aluno (MATRÍCULA)"""
    nome = request.form.get('nome')
    matricula = request.form.get('matricula')
    turma_id = request.form.get('turma_id')

    # Validações
    if not nome or not matricula:
        flash("Nome e matrícula são obrigatórios!", "danger")
        return redirect(url_for('alunos.listar_alunos'))

    try:
        # Verifica se a matrícula já existe
        if Aluno.query.filter_by(matricula=matricula).first():
            flash("Matrícula já existe!", "danger")
            return redirect(url_for('alunos.listar_alunos'))

        # Cria o aluno
        novo_aluno = Aluno(
            nome=nome.strip(),
            matricula=matricula.strip(),
            turma_id=turma_id if turma_id else None
        )

        db.session.add(novo_aluno)
        db.session.commit()
        
        flash("Aluno matriculado com sucesso!", "success")
        
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao matricular aluno: {str(e)}", "danger")
    
    return redirect(url_for('alunos.listar_alunos'))

@alunos_bp.route("/alunos/<int:aluno_id>/editar", methods=["POST"])
def editar_aluno(aluno_id):
    """Edita um aluno existente"""
    aluno = Aluno.query.get_or_404(aluno_id)
    
    nome = request.form.get('nome')
    matricula = request.form.get('matricula')
    turma_id = request.form.get('turma_id')

    # Validações
    if not nome or not matricula:
        flash("Nome e matrícula são obrigatórios!", "danger")
        return redirect(url_for('alunos.listar_alunos'))

    try:
        # Verifica se a matrícula já existe (excluindo o próprio aluno)
        aluno_existente = Aluno.query.filter_by(matricula=matricula).first()
        if aluno_existente and aluno_existente.id != aluno_id:
            flash("Matrícula já existe!", "danger")
            return redirect(url_for('alunos.listar_alunos'))

        # Atualiza os dados
        aluno.nome = nome.strip()
        aluno.matricula = matricula.strip()
        aluno.turma_id = turma_id if turma_id else None

        db.session.commit()
        flash("Aluno atualizado com sucesso!", "success")
        
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao atualizar aluno: {str(e)}", "danger")
    
    return redirect(url_for('alunos.listar_alunos'))

@alunos_bp.route("/alunos/<int:aluno_id>/excluir", methods=["POST"])
def excluir_aluno(aluno_id):
    """Exclui um aluno (DESMATRICULAR)"""
    aluno = Aluno.query.get_or_404(aluno_id)
    
    try:
        # Remove todas as presenças do aluno
        Presenca.query.filter_by(aluno_id=aluno_id).delete()
        
        # Remove o aluno
        db.session.delete(aluno)
        db.session.commit()
        
        flash("Aluno desmatriculado com sucesso!", "success")
        
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao desmatricular aluno: {str(e)}", "danger")
    
    return redirect(url_for('alunos.listar_alunos'))

@alunos_bp.route("/alunos/<int:id>/remover", methods=["POST"])
def remover_aluno(id):
    """Remove aluno da turma (mas mantém no sistema)"""
    aluno = Aluno.query.get_or_404(id)
    turma_id = aluno.turma_id
    
    try:
        aluno.turma_id = None
        db.session.commit()
        flash("Aluno removido da turma!", "success")
        
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao remover aluno da turma: {str(e)}", "danger")
    
    return redirect(url_for('turmas.get_one', id=turma_id))
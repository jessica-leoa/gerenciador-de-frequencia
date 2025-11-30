import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.aluno import Aluno
from models.turma import Turma
from extensions import db

alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.get("/alunos")
def list_all():
    lista_alunos = Aluno.query.order_by(Aluno.nome).all()
    turmas = Turma.query.all()
    return render_template("alunos.html", lista_alunos=lista_alunos, turmas=turmas)

@alunos_bp.post("/aluno/criar")
def criar_aluno():
    nome = request.form.get("nome")
    matricula = request.form.get("matricula")
    turma_id = request.form.get("turma_id")
    
    # 1. Validação de Nome
    if not nome or len(nome) > 50 or not re.match(r"^[A-Za-z\s]{1,50}$", nome):
        flash("Nome inválido. Deve ter no máximo 50 caracteres e conter apenas letras e espaços.", "danger")
        return redirect(url_for("alunos.list_all"))

    # 2. Validação de Matrícula (Verifica se é puramente numérica)
    if not matricula or len(matricula) > 11 or not matricula.isdigit():
        flash("Matrícula inválida. Deve ter no máximo 11 dígitos e conter apenas números.", "danger")
        return redirect(url_for("alunos.list_all"))

    # 3. Validação de Unicidade da Matrícula
    if Aluno.query.filter_by(matricula=matricula).first():
        flash(f"Matrícula '{matricula}' já cadastrada.", "danger")
        return redirect(url_for("alunos.list_all"))

    # 4. Validação da Turma (Busca e tipagem correta)
    turma_obj = None
    if turma_id:
        try:
            turma_id_int = int(turma_id)
            turma_obj = Turma.query.get(turma_id_int)
        except ValueError:
             flash("ID da Turma inválido.", "danger")
             return redirect(url_for("alunos.list_all"))
             
        if not turma_obj:
            flash("Turma selecionada não existe.", "danger")
            return redirect(url_for("alunos.list_all"))
        
        turma_id = turma_id_int
    else:
        turma_id = None
        
    try:
        novo_aluno = Aluno(nome=nome.title(), matricula=matricula, turma_id=turma_id)
        db.session.add(novo_aluno)
        db.session.commit()
        flash(f"Aluno '{nome.title()}' matriculado com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao matricular aluno: {e}", "danger")

    return redirect(url_for("alunos.list_all"))

@alunos_bp.post("/aluno/adicionar")
def adicionar_aluno():
    nome = request.form.get("nome")
    matricula = request.form.get("matricula")
    turma_id = request.form.get("turma_id", type=int)

    # 1. Validação de Nome
    if not nome or len(nome) > 50 or not re.match(r"^[A-Za-z\s]{1,50}$", nome):
        flash("Nome inválido. Máximo 50 caracteres, apenas letras e espaços.", "danger")
        return redirect(url_for("turmas.get_one", id=turma_id))

    # 2. Validação de Matrícula
    if not matricula or len(matricula) > 11 or not matricula.isdigit():
        flash("Matrícula inválida. Máximo 11 dígitos, apenas números.", "danger")
        return redirect(url_for("turmas.get_one", id=turma_id))

    # 3. Validação de Unicidade (pode ser um aluno já cadastrado sem turma)
    aluno_existente = Aluno.query.filter_by(matricula=matricula).first()
    
    if aluno_existente:
        # Aluno existe, apenas o associa à turma se não estiver
        if aluno_existente.turma_id is None:
            aluno_existente.turma_id = turma_id
            db.session.commit()
            flash(f"Aluno '{aluno_existente.nome}' associado à turma com sucesso!", "success")
        else:
            flash(f"Aluno com matrícula '{matricula}' já existe e já está em outra turma.", "danger")
        return redirect(url_for("turmas.get_one", id=turma_id))
    
    # Cria novo aluno
    try:
        novo_aluno = Aluno(nome=nome.title(), matricula=matricula, turma_id=turma_id)
        db.session.add(novo_aluno)
        db.session.commit()
        flash(f"Aluno '{nome.title()}' criado e adicionado à turma com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao adicionar aluno: {e}", "danger")
    
    return redirect(url_for("turmas.get_one", id=turma_id))

@alunos_bp.post("/aluno/<int:aluno_id>/editar")
def editar_aluno(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    nome = request.form.get("nome")
    matricula = request.form.get("matricula")
    turma_id = request.form.get("turma_id")

    # 1. Validação de Nome
    if not nome or len(nome) > 50 or not re.match(r"^[A-Za-z\s]{1,50}$", nome):
        flash("Nome inválido. Máximo 50 caracteres, apenas letras e espaços.", "danger")
        return redirect(url_for("alunos.list_all"))

    # 2. Validação de Matrícula
    if not matricula or len(matricula) > 11 or not matricula.isdigit():
        flash("Matrícula inválida. Máximo 11 dígitos, apenas números.", "danger")
        return redirect(url_for("alunos.list_all"))

    # 3. Validação de Unicidade da Matrícula
    aluno_existente = Aluno.query.filter(Aluno.matricula == matricula, Aluno.id != aluno_id).first()
    if aluno_existente:
        flash(f"Matrícula '{matricula}' já está em uso por outro aluno.", "danger")
        return redirect(url_for("alunos.list_all"))

    aluno.nome = nome.title()
    aluno.matricula = matricula
    
    # 4. Atualização da Turma
    if turma_id:
        try:
            # Tenta converter para inteiro ANTES de consultar o DB
            turma_id = int(turma_id)
        except ValueError:
            flash("ID da Turma inválido.", "danger")
            return redirect(url_for("alunos.list_all"))
            
        turma = Turma.query.get(turma_id)
        if not turma:
            flash("Turma selecionada não existe.", "danger")
            return redirect(url_for("alunos.list_all"))
        # A linha 'turma_id = int(turma_id)' no final do bloco 4 foi removida/movida
    else:
        turma_id = None
        
    db.session.commit()
    flash(f"Dados do aluno '{aluno.nome}' atualizados com sucesso!", "success")
    return redirect(url_for("alunos.list_all"))

@alunos_bp.post("/aluno/<int:aluno_id>/excluir")
def excluir_aluno(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    nome_aluno = aluno.nome
    
    db.session.delete(aluno)
    db.session.commit()
    
    flash(f"Aluno '{nome_aluno}' excluído e seus registros de presença removidos com sucesso!", "success")
    return redirect(url_for("alunos.list_all"))

@alunos_bp.post("/aluno/<int:id>/remover")
def remover_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    turma_id = aluno.turma_id
    aluno.turma_id = None
    db.session.commit()
    flash(f"Aluno '{aluno.nome}' removido da turma com sucesso!", "warning")
    return redirect(url_for('turmas.get_one', id=turma_id))
# routes/turma_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.turma import Turma
from models.aula import Aula
from models.aluno import Aluno
from models.aluno import Presenca
from extensions import db
from datetime import date

turmas_bp = Blueprint('turmas', __name__)

@turmas_bp.route("/turmas")
def list_all():
    turmas = Turma.query.all()
    return render_template("index.html", turmas=turmas)

@turmas_bp.route("/turmas/nova", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        carga_horaria = request.form["carga_horaria"]

        # Validação 1: Nome da Disciplina (Max 30 caracteres)
        if not nome or len(nome) > 30:
            flash("Nome da Disciplina inválido. Máximo 30 caracteres.", "danger")
            return render_template("turma_form.html")

        # Validação 2: Carga Horária (Positiva e Max 120)
        try:
            carga_horaria = int(carga_horaria)
            if carga_horaria <= 0 or carga_horaria > 120:
                flash("Carga Horária deve ser positiva e no máximo 120 horas.", "danger")
                return render_template("turma_form.html")
        except ValueError:
            flash("Carga Horária deve ser um número inteiro válido.", "danger")
            return render_template("turma_form.html")

        nova_turma = Turma(nome=nome, carga_horaria=carga_horaria)
        db.session.add(nova_turma)
        db.session.commit()
        flash("Turma criada com sucesso!", "success")
        return redirect(url_for("turmas.list_all"))
    return render_template("turma_form.html")

@turmas_bp.route("/turmas/<int:id>")
def get_one(id):
    turma = Turma.query.get_or_404(id)
    aulas = Aula.query.filter_by(turma_id=id).order_by(Aula.data_aula.desc()).all()
    # Adicionando a data atual para o badge 'Hoje' no template
    now = date.today()
    return render_template("turma_detalhes.html", turma=turma, aulas=aulas, now=now)

# Rota para Criar Aula (POST dentro dos detalhes da turma)
@turmas_bp.post("/turmas/<int:id>/aula")
def criar_aula(id):
    turma = Turma.query.get_or_404(id)
    conteudo = request.form.get('conteudo', '').strip()
    
    # Validação simples
    if not conteudo:
        flash("O conteúdo da aula não pode estar vazio.", "danger")
        return redirect(url_for('turmas.get_one', id=turma.id))

    nova_aula = Aula(
        turma_id=turma.id,
        data_aula=date.today(),
        conteudo=conteudo
    )
    db.session.add(nova_aula)
    db.session.commit()
    flash("Aula criada com sucesso!", "success")
    return redirect(url_for('turmas.get_one', id=turma.id))

# Rota para Excluir Turma (DELETE/POST - Modal de confirmação no template)
@turmas_bp.post("/turmas/<int:id>/excluir")
def excluir_turma(id):
    turma = Turma.query.get_or_404(id)
    
    # Prevenção extra, embora o modal no template faça o trabalho
    if turma.alunos or turma.aulas:
        flash("Não é possível excluir a turma. Remova alunos e aulas primeiro.", "danger")
        return redirect(url_for('turmas.get_one', id=turma.id))
        
    db.session.delete(turma)
    db.session.commit()
    flash(f"Turma '{turma.nome}' excluída com sucesso!", "success")
    return redirect(url_for("turmas.list_all"))

# Rota para Editar Turma (NOVA)
@turmas_bp.post("/turmas/<int:id>/editar")
def editar_turma(id):
    turma = Turma.query.get_or_404(id)
    nome = request.form["nome"].strip()
    carga_horaria = request.form["carga_horaria"]

    # Validação 1: Nome da Disciplina (Max 30 caracteres)
    if not nome or len(nome) > 30:
        flash("Nome da Disciplina inválido. Máximo 30 caracteres.", "danger")
        return redirect(url_for('turmas.list_all'))

    # Validação 2: Carga Horária (Positiva e Max 120)
    try:
        carga_horaria = int(carga_horaria)
        if carga_horaria <= 0 or carga_horaria > 120:
            flash("Carga Horária deve ser positiva e no máximo 120 horas.", "danger")
            return redirect(url_for('turmas.list_all'))
    except ValueError:
        flash("Carga Horária deve ser um número inteiro válido.", "danger")
        return redirect(url_for('turmas.list_all'))

    turma.nome = nome
    turma.carga_horaria = carga_horaria
    db.session.commit()
    flash("Turma editada com sucesso!", "success")
    return redirect(url_for('turmas.list_all'))

# Rota para Excluir Aula
@turmas_bp.post("/aulas/<int:aula_id>/excluir")
def excluir_aula(aula_id):
    aula = Aula.query.get_or_404(aula_id)
    turma_id = aula.turma_id
    
    # Exclui todos os registros de presença relacionados antes de excluir a aulas
    Presenca.query.filter_by(aula_id=aula.id).delete()
    db.session.delete(aula)
    db.session.commit()
    flash("Aula e seus registros de presença foram excluídos com sucesso!", "success")
    return redirect(url_for('turmas.get_one', id=turma_id))
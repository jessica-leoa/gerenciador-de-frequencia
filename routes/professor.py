from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.aula import Aula
from models.turma import Turma
from models.aluno import Aluno
from models.presenca import Presenca
from extensions import db
from datetime import date

professor_bp = Blueprint('professor', __name__)

@professor_bp.post("/aula/<int:aula_id>/chamada")
def realizar_chamada(aula_id):
    aula = Aula.query.get_or_404(aula_id)
    alunos = Aluno.query.filter_by(turma_id=aula.turma_id).all()
    
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
    return redirect(url_for("turmas.get_one", id=aula.turma_id))

@professor_bp.get("/aula/<int:aula_id>/chamada")
def popular_chamadas(aula_id):
    aula = Aula.query.get_or_404(aula_id)
    turma = Turma.query.get(aula.turma_id)
    alunos = Aluno.query.filter_by(turma_id=aula.turma_id).order_by(Aluno.nome).all()
    lista_chamada = []
    for aluno in alunos:
        registro = Presenca.query.filter_by(aluno_id=aluno.id, aula_id=aula.id).first()
        presente = registro.presenca if registro else True
        lista_chamada.append({
            'aluno': aluno,
            'presente': presente
        })

    return render_template("chamada.html", aula=aula, turma=turma, lista_chamada=lista_chamada)

# --- ROTA ÚNICA DE RELATÓRIOS ---
@professor_bp.route("/relatorios")
def relatorios():
    # Parâmetros para abas
    aba = request.args.get('aba', 'geral')
    turma_id = request.args.get('turma_id', type=int)
    
    # Dados gerais para todas as abas
    turmas = Turma.query.all()
    total_alunos = Aluno.query.count()
    total_turmas = len(turmas)
    total_aulas = Aula.query.count()
    total_presencas = Presenca.query.filter_by(presenca=True).count()
    total_faltas = Presenca.query.filter_by(presenca=False).count()
    total_registros = total_presencas + total_faltas
    
    # Percentuais
    percentual_presenca = (total_presencas / total_registros * 100) if total_registros > 0 else 0
    percentual_falta = (total_faltas / total_registros * 100) if total_registros > 0 else 0
    
    # Dados para aba de frequência
    dados_frequencia = []
    turma_selecionada = None
    
    if turma_id:
        turma_selecionada = Turma.query.get_or_404(turma_id)
        alunos = Aluno.query.filter_by(turma_id=turma_id).all()
        aulas = Aula.query.filter_by(turma_id=turma_id).all()
        
        for aluno in alunos:
            total_presencas_aluno = Presenca.query.filter_by(
                aluno_id=aluno.id, 
                presenca=True
            ).join(Aula).filter(Aula.turma_id == turma_id).count()
            
            total_aulas_turma = len(aulas)
            frequencia = (total_presencas_aluno / total_aulas_turma * 100) if total_aulas_turma > 0 else 0
            
            status = "Aprovado" if frequencia >= 75 else "Atenção" if frequencia >= 50 else "Reprovado"
            
            dados_frequencia.append({
                'aluno': aluno,
                'total_presencas': total_presencas_aluno,
                'total_aulas': total_aulas_turma,
                'frequencia': round(frequencia, 1),
                'status': status
            })
    
    # Dados para aba de estatísticas
    turmas_com_estatisticas = []
    for turma in turmas:
        alunos_turma = Aluno.query.filter_by(turma_id=turma.id).count()
        aulas_turma = Aula.query.filter_by(turma_id=turma.id).count()
        
        if aulas_turma > 0 and alunos_turma > 0:
            presencas_turma = db.session.query(Presenca).join(Aula).filter(
                Aula.turma_id == turma.id, 
                Presenca.presenca == True
            ).count()
            
            frequencia_turma = (presencas_turma / (aulas_turma * alunos_turma) * 100) if (aulas_turma * alunos_turma) > 0 else 0
            
            turmas_com_estatisticas.append({
                'turma': turma,
                'alunos': alunos_turma,
                'aulas': aulas_turma,
                'frequencia': round(frequencia_turma, 1)
            })
    
    # Dados para aba geral (frequência por turma)
    frequencia_turmas = []
    for turma in turmas:
        aulas_turma = Aula.query.filter_by(turma_id=turma.id).count()
        alunos_turma = Aluno.query.filter_by(turma_id=turma.id).count()
        
        if aulas_turma > 0 and alunos_turma > 0:
            presencas_turma = db.session.query(Presenca).join(Aula).filter(
                Aula.turma_id == turma.id, 
                Presenca.presenca == True
            ).count()
            
            total_possivel_presencas = aulas_turma * alunos_turma
            frequencia_percentual = (presencas_turma / total_possivel_presencas * 100) if total_possivel_presencas > 0 else 0
            
            frequencia_turmas.append({
                'turma': turma,
                'aulas': aulas_turma,
                'alunos': alunos_turma,
                'presencas': presencas_turma,
                'frequencia': round(frequencia_percentual, 1)
            })
        else:
            frequencia_turmas.append({
                'turma': turma,
                'aulas': aulas_turma,
                'alunos': alunos_turma,
                'presencas': 0,
                'frequencia': 0
            })
    
    # Alunos com baixa frequência (< 75%)
    alunos_baixa_frequencia = []
    for turma in turmas:
        alunos_turma = Aluno.query.filter_by(turma_id=turma.id).all()
        aulas_turma = Aula.query.filter_by(turma_id=turma.id).count()
        
        if aulas_turma > 0:
            for aluno in alunos_turma:
                presencas_aluno = Presenca.query.filter_by(
                    aluno_id=aluno.id, 
                    presenca=True
                ).join(Aula).filter(Aula.turma_id == turma.id).count()
                
                frequencia_aluno = (presencas_aluno / aulas_turma * 100)
                if frequencia_aluno < 75:
                    alunos_baixa_frequencia.append({
                        'aluno': aluno,
                        'turma': turma,
                        'presencas': presencas_aluno,
                        'aulas': aulas_turma,
                        'frequencia': round(frequencia_aluno, 1)
                    })
    
    return render_template("relatorio.html",
                           aba=aba,
                           turma_id=turma_id,
                           turma_selecionada=turma_selecionada,
                           turmas=turmas,
                           total_alunos=total_alunos,
                           total_turmas=total_turmas,
                           total_aulas=total_aulas,
                           total_presencas=total_presencas,
                           total_faltas=total_faltas,
                           percentual_presenca=round(percentual_presenca, 1),
                           percentual_falta=round(percentual_falta, 1),
                           dados_frequencia=dados_frequencia,
                           turmas_com_estatisticas=turmas_com_estatisticas,
                           frequencia_turmas=frequencia_turmas,
                           alunos_baixa_frequencia=alunos_baixa_frequencia)
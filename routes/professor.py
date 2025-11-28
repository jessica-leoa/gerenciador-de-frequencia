from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.presenca_service import (
    find_by_aluno_e_aula, create_presenca, update_presenca
)
from services.aluno_service import (
    get_alunos_by_turma,
)
from services.aula_service import (
    get_aula_by_id
)
from services.turma_service import (
    get_turma
)

professor_bp = Blueprint('professor', __name__)

@professor_bp.post("/aula/<int:aula_id>/chamada")
def realizar_chamada(aula_id):
    aula = get_aula_by_id(aula_id)
    alunos = get_alunos_by_turma(aula.turma_id)
    
    for aluno in alunos:
        status_presenca = request.form.get(f"presenca_{aluno.id}") == "on"
        registro = find_by_aluno_e_aula(aluno_id=aluno.id, aula_id=aula.id)
        if registro:
            update_presenca(registro.id, status_presenca)
        else:
            data = { 
                "aluno_id" :aluno.id,
                "aula_id" : aula.id,
                "presenca" : status_presenca
            }
            create_presenca(data)
            
    flash("Chamada salva com sucesso!", "success")
    return redirect(url_for("turmas.get_one", id=aula.turma_id))

    
@professor_bp.get("/aula/<int:aula_id>/chamada")
def popular_chamadas(aula_id): 
    aula = get_aula_by_id(aula_id)
    turma = get_turma(aula.turma_id)
    alunos = get_alunos_by_turma(aula.turma_id)
    lista_chamada = []
    for aluno in alunos:
        registro = find_by_aluno_e_aula(aluno_id=aluno.id, aula_id=aula.id)
        presente = registro.presenca if registro else True 
        lista_chamada.append({
            'aluno': aluno,
            'presente': presente
        })

    return render_template("chamada.html", aula=aula, turma=turma, lista_chamada=lista_chamada)

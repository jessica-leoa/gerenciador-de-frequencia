from extensions import db
from models.aluno import Aluno

def create_aluno(data):
    aluno = Aluno(nome=data["nome"], matricula=data["matricula"], turma_id = data["turma_id"])
    db.session.add(aluno)
    db.session.commit()
    return aluno

def get_alunos():
    return Aluno.query.all()

def get_aluno(id):
    return Aluno.query.get(id)

def update_aluno(id, data):
    aluno = Aluno.query.get(id)
    if not aluno:
        return None
    aluno.nome = data.get("nome", aluno.nome)
    aluno.matricula = data.get("matricula", aluno.matricula)
    aluno.turma_id = data.get("turma_id",aluno.turma_id)
    db.session.commit()
    return aluno

def delete_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return None
    db.session.delete(aluno)
    db.session.commit()
    return True
from extensions import db
from models.turma import Turma

def create_turma(data):
    turma = Turma(nome=data["nome"], carga_horaria=data["carga_horaria"])
    db.session.add(turma)
    db.session.commit()
    return turma

def get_turmas():
    return Turma.query.all()

def get_turma(id):
    return Turma.query.get(id)

def update_turma(id, data):
    turma = Turma.query.get(id)
    if not turma:
        return None
    turma.nome = data.get("nome", turma.nome)
    turma.carga_horaria = data.get("carga_horaria", turma.carga_horaria)
    db.session.commit()
    return turma

def delete_turma(id):
    turma = Turma.query.get(id)
    if not turma:
        return None
    db.session.delete(turma)
    db.session.commit()
    return True
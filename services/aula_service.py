from extensions import db
from models import Aula, Turma

def create_aula(data):
    nova = Aula(
        turma_id=data["turma_id"],
        data_aula=data["data_aula"]
    )
    db.session.add(nova)
    db.session.commit()
    return nova


def get_all_aulas():
    return Aula.query.all()


def get_aula_by_id(id):
    aula = Aula.query.get_or_404(id)
    return aula


def update_aula(id, data):
    aula = Aula.query.get(id)
    if not aula:
        return None

    aula.turma_id = data.get("turma_id", aula.turma_id)
    aula.data_aula = data.get("data_aula", aula.data_aula)

    db.session.commit()
    return aula


def delete_aula(id):
    aula = Aula.query.get(id)
    if not aula:
        return False

    db.session.delete(aula)
    db.session.commit()
    return True

def aulas_by_turma(turma_id):
    return Aula.query.filter_by(turma_id=turma_id).order_by(Aula.data_aula.desc()).all()
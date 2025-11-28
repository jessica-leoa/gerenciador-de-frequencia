from extensions import db
from models import Presenca

def find_by_aluno_e_aula(aluno_id, aula_id):
    return Presenca.query.filter_by(aluno_id=aluno_id, aula_id=aula_id).first()

def create_presenca(data):
    nova = Presenca(aluno_id=data["aluno_id"], aula_id=data["aula_id"], presenca=data["presenca"])
    db.session.add(nova)
    db.session.commit()

def update_presenca(presenca_id, status_presenca):
    presenca = Presenca.query.get_or_404(presenca_id)
    presenca.presenca = status_presenca
    db.session.commit()
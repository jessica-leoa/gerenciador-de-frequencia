from extensions import db
from models.turma import Turma

def seed_turmas():
    if db.session.query(Turma).first():
        print("Seed de turmas já rodado, pulando.")
        return
    
    turmas_iniciais = [
        Turma(nome="Logica de Programacao", carga_horaria=80),
        Turma(nome="Sensores e afins", carga_horaria=120),
        Turma(nome="C para iniciantes", carga_horaria=100),
    ]

    db.session.add_all(turmas_iniciais)
    db.session.commit()

    print("Seed inicial de turmas aplicado com sucesso!")
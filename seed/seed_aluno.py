from extensions import db
from models.aluno import Aluno

def seed_alunos():
    if db.session.query(Aluno).first():
        print("Seed de alunos já rodado, pulando.")
        return
    
    alunos_iniciais = [
        Aluno(nome="Lucas Silvestre", matricula="2025001"),
        Aluno(nome="Tobias RXFX", matricula="2025002"),
        Aluno(nome="Jessica Leoa", matricula="2025003"),
    ]

    db.session.add_all(alunos_iniciais)
    db.session.commit()

    print("Seed inicial de alunos aplicado com sucesso!")
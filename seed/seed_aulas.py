from extensions import db
from models.aula import Aula
from models.turma import Turma
from datetime import date, timedelta


def seed_aulas():
    # Evita rodar duas vezes
    if db.session.query(Aula).first():
        print("Seed de aulas já rodado, pulando.")
        return

    turmas = Turma.query.all()

    if not turmas:
        print("Nenhuma turma encontrada. Execute o seed de turmas primeiro!")
        return

    aulas = []

    # Para cada turma, criar 3 aulas com datas sequenciais
    for turma in turmas:
        aulas.append(Aula(
            turma_id=turma.id,
            data_aula=date.today()
        ))
        aulas.append(Aula(
            turma_id=turma.id,
            data_aula=date.today() + timedelta(days=7)
        ))
        aulas.append(Aula(
            turma_id=turma.id,
            data_aula=date.today() + timedelta(days=14)
        ))

    db.session.add_all(aulas)
    db.session.commit()

    print("Seed inicial de aulas aplicado com sucesso!")
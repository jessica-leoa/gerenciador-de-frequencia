import pytest
from datetime import date
from models.aluno import Aluno
from models.turma import Turma
from models.aula import Aula
from models.presenca import Presenca

# Fixture específico para criar um cenário de aulas e presenças
@pytest.fixture
def cenario_frequencia(session):
    # 1. Cria Turma
    turma = Turma(nome='Matemática Avançada', carga_horaria=80)
    session.add(turma)
    session.commit() 


    aluno1 = Aluno(nome='Aluno Exemplar', matricula='1001', turma_id=turma.id)
    aluno2 = Aluno(nome='Alunofaltoso', matricula='1002', turma_id=turma.id)
    session.add_all([aluno1, aluno2])
    session.commit()


    aulas = []
    for i in range(1, 5):
        aula = Aula(turma_id=turma.id, data_aula=date(2025, 5, i), conteudo=f'Aula {i}')
        session.add(aula)
        aulas.append(aula)
    session.commit()


    
    presencas = []

    for aula in aulas:
        presencas.append(Presenca(aluno_id=aluno1.id, aula_id=aula.id, presenca=True))
    

    presencas.append(Presenca(aluno_id=aluno2.id, aula_id=aulas[0].id, presenca=True))
    presencas.append(Presenca(aluno_id=aluno2.id, aula_id=aulas[1].id, presenca=True))
    presencas.append(Presenca(aluno_id=aluno2.id, aula_id=aulas[2].id, presenca=False))
    presencas.append(Presenca(aluno_id=aluno2.id, aula_id=aulas[3].id, presenca=False))

    session.add_all(presencas)
    session.commit()

    return turma, aulas, aluno1, aluno2

def test_visualizar_relatorio_frequencia(client, cenario_frequencia):
    """Testa se o cálculo de % e status (Aprovado/Atenção) aparece corretamente no HTML."""
    turma, _, aluno1, aluno2 = cenario_frequencia

    response = client.get(f"/relatorios?aba=frequencia&turma_id={turma.id}")
    
    assert response.status_code == 200
    html = response.data.decode('utf-8')

    assert "Aluno Exemplar" in html
    assert "100.0%" in html
    assert "Aprovado" in html


    assert "Alunofaltoso" in html
    assert "50.0%" in html
    assert "Atenção" in html

def test_realizar_chamada_post(client, session, cenario_frequencia):
    """Testa o envio do formulário de chamada (POST)."""
    turma, aulas, aluno1, aluno2 = cenario_frequencia
    
    aula_alvo = aulas[0]

    dados_form = {
        f"presenca_{aluno1.id}": "on"
    }

    response = client.post(f"/aula/{aula_alvo.id}/chamada", data=dados_form, follow_redirects=True)

    assert response.status_code == 200
    assert b"Chamada salva com sucesso!" in response.data

    # Verifica no banco de dados se atualizou
    p1 = session.query(Presenca).filter_by(aluno_id=aluno1.id, aula_id=aula_alvo.id).first()
    p2 = session.query(Presenca).filter_by(aluno_id=aluno2.id, aula_id=aula_alvo.id).first()

    assert p1.presenca is True  
    assert p2.presenca is False
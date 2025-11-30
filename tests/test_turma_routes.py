from models.turma import Turma
from models.aluno import Aluno

def test_criar_turma(client, session):
    """Testa criar uma nova turma."""
    dados = {
        "nome": "Banco de Dados II",
        "carga_horaria": "60"
    }
    
    response = client.post("/turmas/nova", data=dados, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Turma criada com sucesso!" in response.data
    
    # Verifica no banco
    turma = session.query(Turma).filter_by(nome="Banco de Dados II").first()
    assert turma is not None
    assert turma.carga_horaria == 60

def test_editar_turma(client, session):
    """Testa editar uma turma existente."""
    # Cria uma turma para editar
    turma = Turma(nome="Algoritmos Antigos", carga_horaria=40)
    session.add(turma)
    session.commit()
    
    dados_editados = {
        "nome": "Algoritmos Avançados",
        "carga_horaria": "80"
    }
    
    response = client.post(f"/turmas/{turma.id}/editar", data=dados_editados, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Turma editada com sucesso!" in response.data
    
    # Verifica atualização 
    session.refresh(turma)
    assert turma.nome == "Algoritmos Avançados"
    assert turma.carga_horaria == 80

def test_excluir_turma_com_alunos_falha(client, session):
    """Testa a regra de negócio: Não pode excluir turma que tem alunos."""
    # Cria turma e aluno
    turma = Turma(nome="Turma Cheia", carga_horaria=40)
    session.add(turma)
    session.commit()
    
    aluno = Aluno(nome="Aluno Teste", matricula="99999", turma_id=turma.id)
    session.add(aluno)
    session.commit()
    
    # Tenta excluir
    response = client.post(f"/turmas/{turma.id}/excluir", follow_redirects=True)
    
    assert response.status_code == 200
    # Espera mensagem de erro (Flash Danger)
    assert b"N\xc3\xa3o \xc3\xa9 poss\xc3\xadvel excluir a turma." in response.data # "Não é possível..."
    
    # Garante que a turma ainda existe
    assert session.query(Turma).filter_by(id=turma.id).first() is not None

def test_excluir_turma_vazia_sucesso(client, session):
    """Testa excluir uma turma sem alunos."""
    turma = Turma(nome="Turma Vazia", carga_horaria=40)
    session.add(turma)
    session.commit()
    
    turma_id = turma.id
    
    response = client.post(f"/turmas/{turma_id}/excluir", follow_redirects=True)
    
    assert response.status_code == 200
    assert b"exclu\xc3\xadda com sucesso" in response.data
    
    assert session.query(Turma).filter_by(id=turma_id).first() is None
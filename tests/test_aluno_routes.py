from models.aluno import Aluno
from extensions import db

def test_listar_alunos_status_code(client, turma_ativa):
    """Testa se a rota /alunos retorna 200 (Sucesso)."""
    response = client.get("/alunos")
    # Verifica o código de status HTTP
    assert response.status_code == 200

def test_criar_aluno_sucesso(client, session, turma_ativa):
    """Testa a criação de um novo aluno com dados válidos."""
    dados = {
        'nome': 'Maria de Souza',
        'matricula': '987654321',
        'turma_id': str(turma_ativa.id)
    }

    # Faz o POST sem seguir o redirecionamento
    response = client.post("/aluno/criar", data=dados)

    # Verifica se houve o redirecionamento correto (Status 302)
    assert response.status_code == 302
    assert response.headers['Location'] == '/alunos'

    # Verifica se a mensagem flash foi salva na sessão
    with client.session_transaction() as sess:
        flashes = sess['_flashes']
        assert len(flashes) == 1
        assert flashes[0] == ('success', "Aluno 'Maria De Souza' matriculado com sucesso!")

    # Verifica o Banco de Dados
    aluno_criado = session.query(Aluno).filter_by(matricula='987654321').first()
    assert aluno_criado is not None
    assert aluno_criado.nome == 'Maria De Souza'
    assert aluno_criado.turma_id == turma_ativa.id

def test_criar_aluno_matricula_duplicada(client, session, aluno_teste):
    """Testa a validação de matrícula duplicada."""
    matricula_duplicada = aluno_teste.matricula

    dados_duplicados = {
        'nome': 'Outro Aluno',
        'matricula': matricula_duplicada, 
        'turma_id': ''
    }

    # Faz o POST sem seguir o redirecionamento
    response = client.post("/aluno/criar", data=dados_duplicados)
    
    # Verifica se houve o redirecionamento correto (Status 302)
    assert response.status_code == 302
    assert response.headers['Location'] == '/alunos'

    # Verifica se a mensagem flash de erro foi salva na sessão
    expected_message = f"Matrícula '{matricula_duplicada}' já cadastrada."
    
    with client.session_transaction() as sess:
        flashes = sess['_flashes']
        assert len(flashes) == 1
        assert flashes[0] == ('danger', expected_message)
    
    # Verifica se o número de alunos não mudou
    assert session.query(Aluno).count() == 1


def test_criar_aluno_nome_invalido(client, session):
    """Testa a validação de nome com caracteres inválidos."""
    
    session.rollback() 
    assert session.query(Aluno).count() == 0

    dados_invalidos = {
        'nome': 'Nome com 123',
        'matricula': '111',
        'turma_id': ''
    }

    response = client.post("/aluno/criar", data=dados_invalidos, follow_redirects=True)
    
    # Verifica a mensagem de erro
    assert response.status_code == 200
    assert b"Nome inv\xc3\xa1lido. Deve ter no m\xc3\xa1ximo 50 caracteres e conter apenas letras e espa\xc3\xa7os." in response.data

    # Verifica se o aluno não foi criado 
    assert session.query(Aluno).count() == 0
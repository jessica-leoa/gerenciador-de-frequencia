import pytest
from app import create_app
from extensions import db
from models.aluno import Aluno
from models.turma import Turma
from models.aula import Aula
from models.presenca import Presenca
import uuid
import random
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from app import create_app
except ImportError:
    print("ERRO: Não foi possível importar 'create_app' do módulo 'app'.")
    sys.exit(1)

@pytest.fixture(scope='session')
def app():
    # Configurações para o ambiente de teste
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False, 
        'SECRET_KEY': 'test_secret',
    })

    # Cria o contexto da aplicação
    with app.app_context():
        db.create_all()

        yield app

        db.drop_all()

# Define o fixture para o cliente de teste Flask
@pytest.fixture(scope='function')
def client(app):
    """Cliente de teste Flask para simular requisições HTTP."""
    return app.test_client()

# Define o fixture para a sessão do banco de dados
@pytest.fixture(scope='function')
def session(app):
    """
    Cria uma nova sessão para cada teste.
    Limpa o banco de dados COMPLETAMENTE após cada teste para evitar erros de contagem.
    """
    with app.app_context():
        # Garante que as tabelas existam
        db.create_all()
        
        yield db.session
        
        # LIMPEZA BRUTA: Remove tudo e recria o banco para o próximo teste
        db.session.remove()
        db.drop_all()

# Define fixtures de dados base
@pytest.fixture
def turma_ativa(session):
    """Cria e retorna uma Turma para uso nos testes."""
    unique_name = f'Programação Web {uuid.uuid4().hex[:6]}'
    turma = Turma(nome=unique_name, carga_horaria=60)
    session.add(turma)
    session.commit()
    return turma

@pytest.fixture
def aluno_teste(session, turma_ativa):
    """Cria e retorna um Aluno para uso nos testes (Matrícula VÁLIDA)."""
    matricula = str(random.randint(10000000000, 99999999999)) 
    aluno = Aluno(nome='João da Silva', matricula=matricula, turma_id=turma_ativa.id)
    session.add(aluno)
    session.commit()
    return aluno
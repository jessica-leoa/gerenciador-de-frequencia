from app import app
from extensions import db
import os

def init_database():
    """Inicializa o banco de dados com todas as tabelas"""
    print("🔄 Inicializando banco de dados...")
    
    # Garante que a pasta instance existe
    instance_path = os.path.join(os.path.dirname(__file__), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
        print("✅ Pasta 'instance' criada")
    
    # Cria todas as tabelas
    with app.app_context():
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")
        
        # Verifica se as tabelas foram criadas corretamente
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"✅ Tabelas criadas: {tables}")
        
        # Verifica a estrutura da tabela aulas
        if 'aulas' in tables:
            columns = [col['name'] for col in inspector.get_columns('aulas')]
            print(f"✅ Colunas da tabela 'aulas': {columns}")
        
        if 'turmas' in tables:
            columns = [col['name'] for col in inspector.get_columns('turmas')]
            print(f"✅ Colunas da tabela 'turmas': {columns}")

if __name__ == "__main__":
    init_database()
    print("🎉 Banco de dados inicializado com sucesso!")
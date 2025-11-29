from flask import Flask, redirect, url_for
from extensions import db, migrate
import os

# Importa todos os modelos para o db.create_all funcionar
from models.aluno import Aluno
from models.turma import Turma
from models.aula import Aula
from models.presenca import Presenca


def create_app():
    app = Flask(__name__)

    # Configurações do banco
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'instance', 'data.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "segredo_super_seguro"

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    from routes.professor import professor_bp
    from routes.turma_routes import turmas_bp
    from routes.aluno_routes import alunos_bp

    app.register_blueprint(professor_bp)
    app.register_blueprint(turmas_bp)
    app.register_blueprint(alunos_bp)

    return app

app = create_app()

@app.route("/")
def home():
    return redirect(url_for('turmas.list_all'))

if __name__ == "__main__":
    print("🚀 Servidor iniciando...")
    print("📊 Acesse: http://localhost:8080")
    with app.app_context():
        # --- CÓDIGO FINAL DE INICIALIZAÇÃO ---
        instance_path = os.path.join(os.path.dirname(__file__), 'instance')
        db_path = os.path.join(instance_path, 'data.db')

        # 1. Cria a pasta 'instance' se não existir
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
            print("✅ Pasta 'instance' criada")

        # 2. VERIFICA SE O BANCO JÁ FOI INICIALIZADO. SE NÃO, CRIA AS TABELAS.
        if not os.path.exists(db_path):
            # Cria todas as tabelas
            db.create_all()
            print("✅ Banco de dados inicializado com sucesso!")
        else:
            print("✅ Banco de dados encontrado, pulando a inicialização.")
        # -----------------------------------

    app.run(host="0.0.0.0", port=8080, debug=True)
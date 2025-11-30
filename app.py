from flask import Flask, redirect, url_for
from extensions import db, migrate
import os

# Importa todos os modelos para o db.create_all funcionar
from models.aluno import Aluno
from models.turma import Turma
from models.aula import Aula
from models.presenca import Presenca


def create_app(test_config=None):
    app = Flask(__name__)

    # Configurações do banco
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'instance', 'data.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "segredo_super_seguro"

    if test_config is not None:
        # Sobrescreve a config padrão
        app.config.from_mapping(test_config)

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
    print("Servidor iniciando...")
    print("Acesse: http://127.0.0.1:8080/turmas")
    with app.app_context():
        instance_path = os.path.join(os.path.dirname(__file__), 'instance')
        db_path = os.path.join(instance_path, 'data.db')

        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
            print("Pasta 'instance' criada")

        if not os.path.exists(db_path):
            # Cria todas as tabelas
            db.create_all()
            print("Banco de dados inicializado com sucesso!")
        else:
            print("Banco de dados encontrado, pulando a inicialização.")
        # -----------------------------------

    app.run(host="0.0.0.0", port=8080, debug=True)
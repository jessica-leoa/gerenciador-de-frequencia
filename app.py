from extensions import db, migrate
from flask import Flask
from routes.aluno_routes import aluno_bp
from routes.turma_routes import turma_bp
from routes.aula_routes import aula_bp
from seed.seed_aluno import seed_alunos
from seed.seed_aulas import seed_aulas
from seed.seed_turma import seed_turmas


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////app/instance/data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/seed")
    def seed():
        with app.app_context():
            seed_turmas()
            seed_alunos()
            seed_aulas()
        return "Seu banco foi populado com dados iniciais!"
    
    app.register_blueprint(aluno_bp, url_prefix="/alunos")
    app.register_blueprint(turma_bp, url_prefix="/turmas")
    app.register_blueprint(aula_bp, url_prefix="/aulas")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)



  

from extensions import db

class Turma(db.Model):
    __tablename__ = 'turmas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), unique=True, nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)
    
    # Relacionamento
    alunos = db.relationship('Aluno', backref=db.backref('turma', lazy=True), cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Turma {self.nome} - {self.carga_horaria}h>'
    
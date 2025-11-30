from extensions import db

class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    matricula = db.Column(db.String(11), unique=True, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id', ondelete='SET NULL'), nullable=True)
   
    # Relacionamento
    presencas = db.relationship('Presenca', backref='aluno', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Aluno {self.nome} - {self.matricula}>'
from extensions import db

class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    carga_horaria = db.Column(db.Integer(), nullable=False)
    
    # Relacionamento corrigido usando back_populates
    alunos = db.relationship("Aluno", back_populates="turma", lazy=True)
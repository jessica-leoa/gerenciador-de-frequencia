from extensions import db

class Presenca(db.Model):
    __tablename__ = "presencas"

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
    aula_id = db.Column(db.Integer, db.ForeignKey("aulas.id"), nullable=False)  # Nome corrigido
    presenca = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    aluno = db.relationship("Aluno", backref="presencas")
    aula = db.relationship("Aula", backref="presencas")
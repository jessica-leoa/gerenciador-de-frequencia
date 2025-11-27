from extensions import db

class Aula(db.Model):
    __tablename__ = "aulas"

    id = db.Column(db.Integer, primary_key=True)
    turma_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=False)
    data_aula = db.Column(db.Date, nullable=False)
    
    # Relacionamento com Turma
    turma = db.relationship("Turma", backref="aulas")
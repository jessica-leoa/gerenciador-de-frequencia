from extensions import db
from datetime import date

class Aula(db.Model):
    __tablename__ = "aulas"

    id = db.Column(db.Integer, primary_key=True)
    data_aula = db.Column(db.Date, default=date.today, nullable=False)
    conteudo = db.Column(db.String(100))
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id', ondelete='CASCADE'), nullable=False)
    
    # Relacionamentos
    turma = db.relationship('Turma', backref=db.backref('aulas', lazy=True, cascade="all, delete-orphan"))
    presencas = db.relationship('Presenca', backref='aula', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Aula {self.data_aula.strftime("%d/%m/%Y")} - {self.turma_id}>'
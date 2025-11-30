from extensions import db

class Presenca(db.Model):
    __tablename__ = 'presencas'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id', ondelete='CASCADE'), nullable=False)
    aula_id = db.Column(db.Integer, db.ForeignKey('aulas.id', ondelete='CASCADE'), nullable=False)
    presenca = db.Column(db.Boolean, default=False, nullable=False)
    
    __table_args__ = (db.UniqueConstraint('aluno_id', 'aula_id', name='_aluno_aula_uc'),)

    def __repr__(self):
        return f'<Presenca Aluno {self.aluno_id} / Aula {self.aula_id}: {self.presenca}>'
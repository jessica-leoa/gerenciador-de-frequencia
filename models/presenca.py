from extensions import db


class Presenca(db.Model):
    __tablename__ = "presencas"

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
    presenca_id = db.Column(db.Integer, db.ForeignKey("aulas.id"), nullable=False)
    presenca = db.Column(db.Boolean, default=True)
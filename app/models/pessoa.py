from app.database import db

class Pessoa(db.Model):
    __tablename__ = 'pessoas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    naturalidade = db.Column(db.String(50))
    nacionalidade = db.Column(db.String(50))

    #contatos = db.relationship('Contato', backref='pessoa', cascade='all, delete-orphan', lazy=True)

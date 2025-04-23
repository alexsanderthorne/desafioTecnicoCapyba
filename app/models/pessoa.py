from app.database import db
from datetime import datetime

class Pessoa(db.Model):
    __tablename__ = "pessoas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    ativo = db.Column(db.Boolean, default=True)
    email_verificado = db.Column(db.Boolean, default=False)
    token_verificacao = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('cpf', name='uq_pessoa_cpf'),
        db.UniqueConstraint('email', name='uq_pessoa_email'),
    )


    #contatos = db.relationship('Contato', backref='pessoa', cascade='all, delete-orphan', lazy=True)

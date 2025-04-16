from app.database import db

class Contato(db.Model):
    __tablename__ = 'contatos'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)  # Ex: telefone, email
    valor = db.Column(db.String(100), nullable=False)

    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)

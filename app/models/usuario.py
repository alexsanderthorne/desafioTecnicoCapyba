from app.database import db
from passlib.hash import bcrypt

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)

    def set_senha(self, senha):
        self.senha_hash = bcrypt.hash(senha)

    def verificar_senha(self, senha):
        return bcrypt.verify(senha, self.senha_hash)

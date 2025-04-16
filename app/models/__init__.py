from .pessoa import Pessoa
from .contato import Contato
from app import db

Pessoa.contatos = db.relationship('Contato', backref='pessoa', cascade='all, delete-orphan', lazy=True)

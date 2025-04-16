from flask import Blueprint, request, jsonify
from app.models.pessoa import Pessoa
from app.schemas.pessoa_schema import PessoaSchema
from app.database import db
from sqlalchemy.exc import IntegrityError

from datetime import datetime

bp = Blueprint('pessoa_routes', __name__, url_prefix='/pessoas')
pessoa_schema = PessoaSchema()
pessoas_schema = PessoaSchema(many=True)

# Criar uma nova pessoa
@bp.route('', methods=['POST'])
def criar_pessoa():
    try:
        data = request.get_json()
        pessoa = pessoa_schema.load(data)
        db.session.add(pessoa)
        db.session.commit()
        return pessoa_schema.jsonify(pessoa), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "CPF já existe"}), 400
    except Exception as e:
        return pessoa_schema.jsonify(pessoa)
    
@bp.route('', methods=['GET'])
def listar_contatos(id_pessoa):
    Pessoa.query.get_or_404(id_pessoa)
    pessoa = Pessoa.query.filter_by(pessoa_id=id_pessoa).all()
    return pessoa_schema.jsonify(pessoa)


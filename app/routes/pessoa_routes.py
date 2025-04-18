from flask import Blueprint, request, jsonify
from app.models.pessoa import Pessoa
from app.schemas.pessoa_schema import PessoaSchema
from app.database import db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required

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


# Buscar pessoa pelo CPF (usando query parameter)
@bp.route('', methods=['GET'])
def buscar_pessoa_por_cpf():
    cpf = request.args.get('cpf')  # Obtém o CPF do parâmetro de consulta
    if not cpf:
        return jsonify({"error": "CPF não fornecido"}), 400

    try:
        pessoa = Pessoa.query.filter_by(cpf=cpf).first()
        if pessoa:
            return pessoa_schema.jsonify(pessoa), 200
        else:
            return jsonify({"error": "Pessoa não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Atualizar uma pessoa existente
@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_pessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    data = request.get_json()

    try:
        # Atualiza apenas os campos que vierem no JSON
        for key, value in data.items():
            setattr(pessoa, key, value)

        # Validação dos dados atualizados
        pessoa_schema.load(data, partial=True)  # partial=True permite atualização parcial

        db.session.commit()
        return pessoa_schema.jsonify(pessoa), 200

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "CPF já existe"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/<int:id>', methods=['DELETE'])
def deletar_pessoa(id):
    pessoa = Pessoa.query.get_or_404(id)
    db.session.delete(pessoa)
    db.session.commit()
    return jsonify({"mensagem": "Pessoa deletada com sucesso."}), 200

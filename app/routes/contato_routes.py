from flask import Blueprint, request, jsonify
from app.models.contato import Contato
from app.models.pessoa import Pessoa
from app.schemas.contato_schema import ContatoSchema
from app.database import db

bp = Blueprint('contato_routes', __name__, url_prefix='/pessoas/<int:id_pessoa>/contatos')
contato_schema = ContatoSchema()
contatos_schema = ContatoSchema(many=True)

# Criar um contato para uma pessoa
@bp.route('', methods=['POST'])
def criar_contato(id_pessoa):
    pessoa = Pessoa.query.get_or_404(id_pessoa)
    data = request.get_json()
    data['pessoa_id'] = id_pessoa

    try:
        contato = contato_schema.load(data)
        db.session.add(contato)
        db.session.commit()
        return contato_schema.jsonify(contato), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Listar todos os contatos de uma pessoa
@bp.route('', methods=['GET'])
def listar_contatos(id_pessoa):
    Pessoa.query.get_or_404(id_pessoa)
    contatos = Contato.query.filter_by(pessoa_id=id_pessoa).all()
    return contatos_schema.jsonify(contatos)

# Obter um contato específico
@bp.route('/<int:id_contato>', methods=['GET'])
def obter_contato(id_pessoa, id_contato):
    Pessoa.query.get_or_404(id_pessoa)
    contato = Contato.query.filter_by(id=id_contato, pessoa_id=id_pessoa).first_or_404()
    return contato_schema.jsonify(contato)

# Atualizar um contato
@bp.route('/<int:id_contato>', methods=['PUT'])
def atualizar_contato(id_pessoa, id_contato):
    Pessoa.query.get_or_404(id_pessoa)
    contato = Contato.query.filter_by(id=id_contato, pessoa_id=id_pessoa).first_or_404()

    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(contato, key, value)

        contato_schema.load(data, partial=True)
        db.session.commit()
        return contato_schema.jsonify(contato)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Deletar um contato
@bp.route('/<int:id_contato>', methods=['DELETE'])
def deletar_contato(id_pessoa, id_contato):
    Pessoa.query.get_or_404(id_pessoa)
    contato = Contato.query.filter_by(id=id_contato, pessoa_id=id_pessoa).first_or_404()

    db.session.delete(contato)
    db.session.commit()
    return jsonify({"message": "Contato deletado com sucesso."}), 200

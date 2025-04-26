from flask import Blueprint, request, jsonify
from app.models.pessoa import Pessoa
from app.schemas.pessoa_schema import PessoaSchema
from app.database import db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from datetime import datetime
from sqlalchemy import or_, asc, desc


bp = Blueprint('pessoa_routes', __name__, url_prefix='/pessoas')
pessoa_schema = PessoaSchema()
pessoas_schema = PessoaSchema(many=True)

# Criar uma nova pessoa
@bp.route('', methods=['POST'])
#@jwt_required()
def criar_pessoa():
    try:
        data = request.get_json()
        pessoa = pessoa_schema.load(data)
        db.session.add(pessoa)
        db.session.commit()
        return pessoa_schema.jsonify(pessoa), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "CPF ou email já cadastrado"}), 400
    except Exception as e:
        return pessoa_schema.jsonify(pessoa)


# Buscar pessoa pelo CPF (usando query parameter)
@jwt_required()
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

@bp.route('/paginado', methods=['GET'])
@jwt_required()
def listar_pessoas_paginado():
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    search = request.args.get('search', default='', type=str)
    ordering = request.args.get('ordering', default='nome', type=str)
    ativo = request.args.get('ativo', type=str)

    query = Pessoa.query

    # Filtro textual
    if search:
        query = query.filter(
            or_(
                Pessoa.nome.ilike(f"%{search}%"),
                Pessoa.cpf.ilike(f"%{search}%")
            )
        )

    # Filtro por campo 'ativo' (se existir no model Pessoa)
    if ativo is not None:
        query = query.filter(Pessoa.ativo == (ativo.lower() == 'true'))

    # Ordenação (ascendente ou descendente)
    if ordering.startswith('-'):
        coluna = ordering[1:]
        if hasattr(Pessoa, coluna):
            query = query.order_by(desc(getattr(Pessoa, coluna)))
    else:
        if hasattr(Pessoa, ordering):
            query = query.order_by(asc(getattr(Pessoa, ordering)))

    total = query.count()
    pessoas_paginadas = query.offset((page - 1) * page_size).limit(page_size).all()

    return jsonify({
        "total": total,
        "page": page,
        "page_size": page_size,
        "resultados": pessoas_schema.dump(pessoas_paginadas)
    }), 200

@bp.route('/pessoas-restritas', methods=['GET'])
@jwt_required()
def listar_pessoas_restritas():
    # Obter o ID do usuário autenticado via token JWT
    usuario_id = get_jwt_identity()

    # Verificar se o usuário tem o e-mail confirmado
    usuario = Pessoa.query.get_or_404(usuario_id)
    if not usuario.email_verificado:
        return jsonify({"error": "E-mail não verificado. Acesso negado."}), 403

    # Exemplo de lista de pessoas restritas (substitua conforme necessário)
    pessoas_restritas = Pessoa.query.filter_by(email_verificado=True).all()

    # Serializar os resultados (Você pode ajustar o schema conforme necessário)
    pessoas_resultado = [{"id": p.id, "nome": p.nome, "email": p.email} for p in pessoas_restritas]

    return jsonify({"pessoas_restritas": pessoas_resultado}), 200

@bp.route('/filtro', methods=['GET'])
@jwt_required()
def filtrar_pessoas():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    search = request.args.get('search', '', type=str)
    email_verificado = request.args.get('email_verificado', type=str)
    ativo = request.args.get('ativo', type=str)
    ordering = request.args.get('ordering', 'nome', type=str)

    query = Pessoa.query

    # 🔍 Busca textual
    if search:
        query = query.filter(
            or_(
                Pessoa.nome.ilike(f"%{search}%"),
                Pessoa.cpf.ilike(f"%{search}%"),
                Pessoa.email.ilike(f"%{search}%")
            )
        )

    # ✅ Filtros booleanos
    if email_verificado is not None:
        query = query.filter(Pessoa.email_verificado == (email_verificado.lower() == 'true'))

    if ativo is not None:
        query = query.filter(Pessoa.ativo == (ativo.lower() == 'true'))

    # ↕️ Ordenação
    if ordering.startswith('-'):
        col = ordering[1:]
        if hasattr(Pessoa, col):
            query = query.order_by(desc(getattr(Pessoa, col)))
    else:
        if hasattr(Pessoa, ordering):
            query = query.order_by(asc(getattr(Pessoa, ordering)))

    # 📄 Paginação
    total = query.count()
    pessoas = query.offset((page - 1) * page_size).limit(page_size).all()
    pessoas_serializadas = pessoas_schema.dump(pessoas)

    return jsonify({
        "total": total,
        "page": page,
        "page_size": page_size,
        "resultados": pessoas_serializadas
    }), 200
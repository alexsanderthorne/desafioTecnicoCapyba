from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from app.database import db
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity


bp = Blueprint('auth_routes', __name__, url_prefix='/auth')

# Criação de usuário (só pra teste)
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"erro": "Email já cadastrado"}), 400

    usuario = Usuario(email=email)
    usuario.set_senha(senha)

    db.session.add(usuario)
    db.session.commit()
    return jsonify({"mensagem": "Usuário criado com sucesso"}), 201

# Login
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({"erro": "Credenciais inválidas"}), 401

    access_token = create_access_token(identity=str(usuario.id))
    return jsonify(access_token=access_token), 200


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    usuario_id = get_jwt_identity()
    return jsonify({"mensagem": f"Logout realizado com sucesso (usuário {usuario_id})"}), 200


@bp.route('/alterar-senha', methods=['PUT'])
@jwt_required()
def alterar_senha():
    usuario_id = int(get_jwt_identity())
    usuario = Usuario.query.get_or_404(usuario_id)

    data = request.get_json()
    senha_atual = data.get('senha_atual')
    nova_senha = data.get('nova_senha')

    if not senha_atual or not nova_senha:
        return jsonify({"erro": "Você deve fornecer senha atual e nova senha"}), 400

    if not usuario.verificar_senha(senha_atual):
        return jsonify({"erro": "Senha atual incorreta"}), 401

    usuario.set_senha(nova_senha)
    db.session.commit()

    return jsonify({"mensagem": "Senha atualizada com sucesso."}), 200

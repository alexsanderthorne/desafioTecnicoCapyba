from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from app.database import db
from flask_jwt_extended import create_access_token

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

    access_token = create_access_token(identity=usuario.id)
    return jsonify(access_token=access_token), 200

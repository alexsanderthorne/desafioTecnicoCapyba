import random
import string
from flask import Blueprint, request, jsonify
from app.models.pessoa import Pessoa
from app.database import db

email_bp = Blueprint('email_routes', __name__, url_prefix='/email')

def gerar_token(length=6):
    return ''.join(random.choices(string.digits, k=length))

@email_bp.route('/enviar-token', methods=['POST'])
def enviar_token():
    data = request.get_json()
    email = data.get('email')

    pessoa = Pessoa.query.filter_by(email=email).first()
    if not pessoa:
        return jsonify({"error": "Email não encontrado"}), 404

    token = gerar_token()
    pessoa.token_verificacao = token
    db.session.commit()

    # Simulação do envio
    print(f"Token enviado para {email}: {token}")

    return jsonify({"mensagem": "Token enviado com sucesso para o e-mail"}), 200

@email_bp.route('/validar-token', methods=['POST'])
def validar_token():
    data = request.get_json()
    email = data.get('email')
    token_digitado = data.get('token')

    pessoa = Pessoa.query.filter_by(email=email).first()
    if not pessoa:
        return jsonify({"error": "Email não encontrado"}), 404

    if pessoa.token_verificacao != token_digitado:
        return jsonify({"error": "Token inválido"}), 400

    pessoa.email_verificado = True
    pessoa.token_verificacao = None
    db.session.commit()

    return jsonify({"mensagem": "E-mail verificado com sucesso"}), 200

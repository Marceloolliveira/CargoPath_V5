from flask import Blueprint, request, jsonify, current_app
from ...data_base.db_classes.DatabaseConnection import DatabaseConnection
import bcrypt
import jwt
import datetime

# Criação do Blueprint
login_blueprint = Blueprint("login", __name__)

@login_blueprint.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Cria uma conexão com o banco de dados
    db = DatabaseConnection()
    db.connect()  # Conecta ao banco
    cursor = db.get_cursor()  # Obtém o cursor

    # Verifique se o cursor foi obtido
    if cursor is None:
        db.close()
        return jsonify({"message": "Erro ao conectar ao banco de dados"}), 500

    # Buscando usuário pelo email
    cursor.execute("SELECT user_id, name, password FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    # Verificando credenciais
    if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):  # user[2] é a senha
        # Gerando token JWT
        token = jwt.encode({
            'user_id': user[0],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")

        db.close()
        return jsonify({
            'token': token,
            'user_id': user[0],  # user[0] é o ID do usuário
            'name': user[1]  # user[1] é o nome do usuário
        }), 200
    else:
        db.close()
        return jsonify({'message': 'Credenciais inválidas'}), 401

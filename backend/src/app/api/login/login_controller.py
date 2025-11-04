from flask import Blueprint, request, jsonify
from .login_service import LoginService

class LoginController:
    # Criação do Blueprint
    blueprint = Blueprint("login", __name__)

    @staticmethod
    @blueprint.route('/api/login', methods=['POST'])
    def login():
        """
        Controller para autenticação de usuário
        """
        try:
            # Validação dos dados de entrada
            data = request.get_json()
            if not data:
                return jsonify({"message": "Dados não fornecidos"}), 400

            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return jsonify({"message": "Email e senha são obrigatórios"}), 400

            # Chamada para o service
            result = LoginService.authenticate_user(email, password)

            if result["success"]:
                return jsonify(result["data"]), 200
            else:
                return jsonify({"message": result["message"]}), 401

        except Exception as e:
            return jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500

# Exporta o blueprint para ser usado no app.py
login_blueprint = LoginController.blueprint
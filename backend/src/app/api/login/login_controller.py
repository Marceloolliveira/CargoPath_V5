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
        return LoginService.handle_login_request(request)

# Exporta o blueprint para ser usado no app.py
login_blueprint = LoginController.blueprint
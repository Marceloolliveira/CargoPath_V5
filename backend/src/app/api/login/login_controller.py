from flask import Blueprint, request, jsonify
from .login_service import LoginService

class LoginController:
    blueprint = Blueprint("login", __name__)

    @staticmethod
    @blueprint.route('/api/login', methods=['POST'])
    def login():
        """
        Controller para autenticação de usuário
        """
        return LoginService.handle_login_request(request)

login_blueprint = LoginController.blueprint
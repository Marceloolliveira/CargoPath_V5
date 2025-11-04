from ...data_base.db_classes.DatabaseConnection import DatabaseConnection
import bcrypt
import jwt
import datetime
from flask import current_app, jsonify

class LoginService:
    @staticmethod
    def handle_login_request(request):
        """
        Manipula toda a requisição de login
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

            # Autenticação do usuário
            result = LoginService.authenticate_user(email, password)

            if result["success"]:
                return jsonify(result["data"]), 200
            else:
                return jsonify({"message": result["message"]}), 401

        except Exception as e:
            return jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500

    @staticmethod
    def authenticate_user(email, password):
        """
        Autentica um usuário com email e senha
        Returns: dict com resultado da autenticação
        """
        try:
            # Cria uma conexão com o banco de dados
            db = DatabaseConnection()
            db.connect()
            cursor = db.get_cursor()

            if cursor is None:
                db.close()
                return {"success": False, "message": "Erro ao conectar ao banco de dados"}

            # Buscando usuário pelo email
            cursor.execute("SELECT user_id, name, password FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            db.close()

            if not user:
                return {"success": False, "message": "Usuário não encontrado"}

            # Verificando credenciais
            if bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
                # Gerando token JWT
                token = LoginService._generate_token(user[0])
                
                return {
                    "success": True,
                    "data": {
                        "token": token,
                        "user_id": user[0],
                        "name": user[1]
                    }
                }
            else:
                return {"success": False, "message": "Credenciais inválidas"}

        except Exception as e:
            return {"success": False, "message": f"Erro interno: {str(e)}"}

    @staticmethod
    def _generate_token(user_id):
        """
        Gera um token JWT para o usuário
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
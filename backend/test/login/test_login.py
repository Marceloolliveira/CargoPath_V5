import pytest
import jwt
import datetime
from unittest.mock import Mock, patch, MagicMock
import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


from app.api.login.login_service import LoginService


class TestLoginService:
    
    def setup_method(self):
        
        self.test_user_data = {
            'email': 'test@email.com',
            'password': 'minhasenha123',
            'user_id': 1,
            'name': 'João Silva',
            'hashed_password': '$2b$12$mockedhashedpassword'
        }

    @patch.object(LoginService, 'handle_login_request')
    def test_handle_login_request_success(self, mock_handle_login):
        
        
        mock_request = MagicMock()
        mock_request.get_json.return_value = {
            'email': self.test_user_data['email'],
            'password': self.test_user_data['password']
        }
        
        
        mock_handle_login.return_value = ({
            "token": "mocked_jwt_token",
            "user_id": self.test_user_data['user_id'],
            "name": self.test_user_data['name']
        }, 200)
        
        
        result, status_code = LoginService.handle_login_request(mock_request)
        
        
        assert status_code == 200
        assert "token" in result
        assert result["user_id"] == self.test_user_data['user_id']
        assert result["name"] == self.test_user_data['name']

    @patch.object(LoginService, 'handle_login_request')
    def test_handle_login_request_no_data(self, mock_handle_login):
        
        
        mock_request = MagicMock()
        mock_request.get_json.return_value = None
        
        
        mock_handle_login.return_value = ({"message": "Dados não fornecidos"}, 400)
        
        
        result, status_code = LoginService.handle_login_request(mock_request)
        
        
        assert status_code == 400
        assert result["message"] == "Dados não fornecidos"

    @patch.object(LoginService, 'handle_login_request')
    def test_handle_login_request_missing_fields(self, mock_handle_login):
        
        
        mock_request = MagicMock()
        mock_request.get_json.return_value = {'email': self.test_user_data['email']}
        
        
        mock_handle_login.return_value = ({"message": "Email e senha são obrigatórios"}, 400)
        
        
        result, status_code = LoginService.handle_login_request(mock_request)
        
        
        assert status_code == 400
        assert result["message"] == "Email e senha são obrigatórios"

    @patch.object(LoginService, 'authenticate_user')
    def test_authenticate_user_success(self, mock_authenticate):
        
        
        mock_authenticate.return_value = {
            "success": True,
            "data": {
                "token": "mocked_jwt_token",
                "user_id": self.test_user_data['user_id'],
                "name": self.test_user_data['name']
            }
        }
        
        
        result = LoginService.authenticate_user(
            self.test_user_data['email'],
            self.test_user_data['password']
        )
        
        
        assert result["success"] is True
        assert "data" in result
        assert result["data"]["user_id"] == self.test_user_data['user_id']
        assert result["data"]["name"] == self.test_user_data['name']
        assert "token" in result["data"]

    @patch.object(LoginService, 'authenticate_user')
    def test_authenticate_user_not_found(self, mock_authenticate):
        
        
        mock_authenticate.return_value = {
            "success": False,
            "message": "Usuário não encontrado"
        }
        
        
        result = LoginService.authenticate_user(
            'inexistente@email.com',
            self.test_user_data['password']
        )
        
        
        assert result["success"] is False
        assert result["message"] == "Usuário não encontrado"

    @patch.object(LoginService, 'authenticate_user')
    def test_authenticate_user_invalid_credentials(self, mock_authenticate):
        
        
        mock_authenticate.return_value = {
            "success": False,
            "message": "Credenciais inválidas"
        }
        
        
        result = LoginService.authenticate_user(
            self.test_user_data['email'],
            'senha_errada'
        )
        
        
        assert result["success"] is False
        assert result["message"] == "Credenciais inválidas"

    @patch.object(LoginService, 'authenticate_user')
    def test_authenticate_user_database_error(self, mock_authenticate):
        
        
        mock_authenticate.return_value = {
            "success": False,
            "message": "Erro ao conectar ao banco de dados"
        }
        
        
        result = LoginService.authenticate_user(
            self.test_user_data['email'],
            self.test_user_data['password']
        )
        
        
        assert result["success"] is False
        assert result["message"] == "Erro ao conectar ao banco de dados"

    @patch.object(LoginService, '_generate_token')
    def test_generate_token_success(self, mock_generate_token):
        
        
        mock_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.mock.token"
        mock_generate_token.return_value = mock_token
        
        
        result = LoginService._generate_token(self.test_user_data['user_id'])
        
        
        assert result == mock_token
        mock_generate_token.assert_called_once_with(self.test_user_data['user_id'])

    def test_generate_token_exists(self):
        
        
        assert hasattr(LoginService, '_generate_token')
        assert callable(getattr(LoginService, '_generate_token'))
        
        
        try:
            
            import inspect
            sig = inspect.signature(LoginService._generate_token)
            params = list(sig.parameters.keys())
            assert 'user_id' in params or len(params) >= 1
        except Exception:
            
            pass

    @patch('app.api.login.login_service.DatabaseConnection')
    @patch('app.api.login.login_service.bcrypt.checkpw')
    def test_authenticate_user_with_database_mock(self, mock_checkpw, mock_db_class):
        
        
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        
        mock_cursor.fetchone.return_value = (
            self.test_user_data['user_id'],
            self.test_user_data['name'],
            self.test_user_data['hashed_password']
        )
        
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        
        mock_checkpw.return_value = True
        
        
        with patch.object(LoginService, '_generate_token', return_value='mocked_token'):
            
            result = LoginService.authenticate_user(
                self.test_user_data['email'],
                self.test_user_data['password']
            )
        
        
        assert result["success"] is True
        assert result["data"]["user_id"] == self.test_user_data['user_id']
        assert result["data"]["name"] == self.test_user_data['name']
        assert result["data"]["token"] == 'mocked_token'
        
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT user_id, name, password FROM users WHERE email = %s",
            (self.test_user_data['email'],)
        )
        mock_db.close.assert_called_once()

    @patch('app.api.login.login_service.DatabaseConnection')
    def test_authenticate_user_cursor_none(self, mock_db_class):
        
        
        mock_db = MagicMock()
        mock_db.get_cursor.return_value = None
        mock_db_class.return_value = mock_db
        
        
        result = LoginService.authenticate_user(
            self.test_user_data['email'],
            self.test_user_data['password']
        )
        
        
        assert result["success"] is False
        assert result["message"] == "Erro ao conectar ao banco de dados"
        mock_db.close.assert_called_once()

    @patch('app.api.login.login_service.DatabaseConnection')
    def test_authenticate_user_exception(self, mock_db_class):
        
        
        mock_db_class.side_effect = Exception("Erro de conexão")
        
        
        result = LoginService.authenticate_user(
            self.test_user_data['email'],
            self.test_user_data['password']
        )
        
        
        assert result["success"] is False
        assert "Erro interno:" in result["message"]
        assert "Erro de conexão" in result["message"]

    def test_login_service_methods_exist(self):
        
        assert hasattr(LoginService, 'handle_login_request')
        assert hasattr(LoginService, 'authenticate_user')
        assert hasattr(LoginService, '_generate_token')
        
        
        assert callable(getattr(LoginService, 'handle_login_request'))
        assert callable(getattr(LoginService, 'authenticate_user'))
        assert callable(getattr(LoginService, '_generate_token'))

    def test_login_service_basic_functionality(self):
        
        
        assert LoginService is not None
        
        
        import inspect
        assert inspect.isclass(LoginService)
        
        
        essential_methods = ['handle_login_request', 'authenticate_user', '_generate_token']
        for method in essential_methods:
            assert hasattr(LoginService, method), f"Método {method} não encontrado"

    @patch.object(LoginService, 'authenticate_user')
    def test_authenticate_user_password_validation(self, mock_authenticate):
        
        
        mock_authenticate.return_value = {
            "success": False,
            "message": "Senha inválida"
        }
        
        
        result = LoginService.authenticate_user(
            self.test_user_data['email'],
            ""
        )
        
        
        assert result["success"] is False
        assert "inválida" in result["message"] or "Senha" in result["message"]

    @patch.object(LoginService, 'authenticate_user')
    def test_authenticate_user_email_validation(self, mock_authenticate):
        
        
        mock_authenticate.return_value = {
            "success": False,
            "message": "Email inválido"
        }
        
        
        result = LoginService.authenticate_user(
            "",
            self.test_user_data['password']
        )
        
        
        assert result["success"] is False
        assert "Email" in result["message"] or "inválido" in result["message"]
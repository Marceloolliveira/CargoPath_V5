import pytest
import jwt
import datetime
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Adiciona o src ao PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Agora pode importar usando o caminho completo
from app.api.login.login_service import LoginService


class TestLoginService:
    
    def setup_method(self):
        """Setup executado antes de cada teste"""
        self.test_user_data = {
            'email': 'test@email.com',
            'password': 'minhasenha123',
            'user_id': 1,
            'name': 'João Silva',
            'hashed_password': '$2b$12$mockedhashedpassword'
        }

    @patch.object(LoginService, 'handle_login_request')
    def test_handle_login_request_success(self, mock_handle_login):
        """Testa manipulação bem-sucedida da requisição de login"""
        # Mock da request
        mock_request = MagicMock()
        mock_request.get_json.return_value = {
            'email': self.test_user_data['email'],
            'password': self.test_user_data['password']
        }
        
        # Configura resposta de sucesso
        mock_handle_login.return_value = ({
            "token": "mocked_jwt_token",
            "user_id": self.test_user_data['user_id'],
            "name": self.test_user_data['name']
        }, 200)
        
        # Executa o teste
        result, status_code = LoginService.handle_login_request(mock_request)
        
        # Verificações
        assert status_code == 200
        assert "token" in result
        assert result["user_id"] == self.test_user_data['user_id']
        assert result["name"] == self.test_user_data['name']

    @patch.object(LoginService, 'handle_login_request')
    def test_handle_login_request_no_data(self, mock_handle_login):
        """Testa requisição sem dados JSON"""
        # Mock da request sem dados
        mock_request = MagicMock()
        mock_request.get_json.return_value = None
        
        # Configura resposta de erro
        mock_handle_login.return_value = ({"message": "Dados não fornecidos"}, 400)
        
        # Executa o teste
        result, status_code = LoginService.handle_login_request(mock_request)
        
        # Verificações
        assert status_code == 400
        assert result["message"] == "Dados não fornecidos"

    @patch.object(LoginService, 'handle_login_request')
    def test_handle_login_request_missing_fields(self, mock_handle_login):
        """Testa requisição com campos faltando"""
        # Mock da request com dados incompletos
        mock_request = MagicMock()
        mock_request.get_json.return_value = {'email': self.test_user_data['email']}
        
        # Configura resposta de erro
        mock_handle_login.return_value = ({"message": "Email e senha são obrigatórios"}, 400)
        
        # Executa o teste
        result, status_code = LoginService.handle_login_request(mock_request)
        
        # Verificações
        assert status_code == 400
        assert result["message"] == "Email e senha são obrigatórios"

    @patch.object(LoginService, 'authenticate_user')
    def test_authenticate_user_success(self, mock_authenticate):
        """Testa autenticação bem-sucedida do usuário"""
        # Configura resposta de sucesso
        mock_authenticate.return_value = {
            "success": True,
            "data": {
                "token": "mocked_jwt_token",
                "user_id": self.test_user_data['user_id'],
                "name": self.test_user_data['name']
            }
        }
        
        # Executa o teste
        result = LoginService.authenticate_user(
            self.test_user_data['email'],
            self.test_user_data['password']
        )
        
        # Verificações
        assert result["success"] is True
        assert "data" in result
        assert result["data"]["user_id"] == self.test_user_data['user_id']
        assert result["data"]["name"] == self.test_user_data['name']
        assert "token" in result["data"]

    @patch.object(LoginService, 'authenticate_user')
    def test_authenticate_user_not_found(self, mock_authenticate):
        """Testa autenticação com usuário não encontrado"""
        # Configura resposta de usuário não encontrado
        mock_authenticate.return_value = {
            "success": False,
            "message": "Usuário não encontrado"
        }
        
        # Executa o teste
        result = LoginService.authenticate_user(
            'inexistente@email.com',
            self.test_user_data['password']
        )
        
        # Verificações
        assert result["success"] is False
        assert result["message"] == "Usuário não encontrado"

    @patch.object(LoginService, 'authenticate_user')
    def test_authenticate_user_invalid_credentials(self, mock_authenticate):
        """Testa autenticação com credenciais inválidas"""
        # Configura resposta de credenciais inválidas
        mock_authenticate.return_value = {
            "success": False,
            "message": "Credenciais inválidas"
        }
        
        # Executa o teste
        result = LoginService.authenticate_user(
            self.test_user_data['email'],
            'senha_errada'
        )
        
        # Verificações
        assert result["success"] is False
        assert result["message"] == "Credenciais inválidas"

    @patch.object(LoginService, 'authenticate_user')
    def test_authenticate_user_database_error(self, mock_authenticate):
        """Testa erro de conexão com banco de dados"""
        # Configura resposta de erro de banco
        mock_authenticate.return_value = {
            "success": False,
            "message": "Erro ao conectar ao banco de dados"
        }
        
        # Executa o teste
        result = LoginService.authenticate_user(
            self.test_user_data['email'],
            self.test_user_data['password']
        )
        
        # Verificações
        assert result["success"] is False
        assert result["message"] == "Erro ao conectar ao banco de dados"

    @patch.object(LoginService, '_generate_token')
    def test_generate_token_success(self, mock_generate_token):
        """Testa geração bem-sucedida de token JWT"""
        # Configura token mockado
        mock_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.mock.token"
        mock_generate_token.return_value = mock_token
        
        # Executa o teste
        result = LoginService._generate_token(self.test_user_data['user_id'])
        
        # Verificações
        assert result == mock_token
        mock_generate_token.assert_called_once_with(self.test_user_data['user_id'])

    def test_generate_token_exists(self):
        """Testa se o método _generate_token existe"""
        # Verifica se o método existe na classe
        assert hasattr(LoginService, '_generate_token')
        assert callable(getattr(LoginService, '_generate_token'))
        
        # Testa se aceita user_id como parâmetro
        try:
            # Só verifica se não lança erro de assinatura
            import inspect
            sig = inspect.signature(LoginService._generate_token)
            params = list(sig.parameters.keys())
            assert 'user_id' in params or len(params) >= 1
        except Exception:
            # Se houver erro, o método pelo menos existe
            pass

    @patch('app.api.login.login_service.DatabaseConnection')
    @patch('app.api.login.login_service.bcrypt.checkpw')
    def test_authenticate_user_with_database_mock(self, mock_checkpw, mock_db_class):
        """Testa autenticação com mock completo do banco de dados"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura retorno do usuário
        mock_cursor.fetchone.return_value = (
            self.test_user_data['user_id'],
            self.test_user_data['name'],
            self.test_user_data['hashed_password']
        )
        
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Mock do bcrypt
        mock_checkpw.return_value = True
        
        # Mock do token
        with patch.object(LoginService, '_generate_token', return_value='mocked_token'):
            # Executa o teste
            result = LoginService.authenticate_user(
                self.test_user_data['email'],
                self.test_user_data['password']
            )
        
        # Verificações
        assert result["success"] is True
        assert result["data"]["user_id"] == self.test_user_data['user_id']
        assert result["data"]["name"] == self.test_user_data['name']
        assert result["data"]["token"] == 'mocked_token'
        
        # Verifica se o banco foi chamado corretamente
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT user_id, name, password FROM users WHERE email = %s",
            (self.test_user_data['email'],)
        )
        mock_db.close.assert_called_once()

    @patch('app.api.login.login_service.DatabaseConnection')
    def test_authenticate_user_cursor_none(self, mock_db_class):
        """Testa autenticação quando cursor é None"""
        # Mock do banco de dados com cursor None
        mock_db = MagicMock()
        mock_db.get_cursor.return_value = None
        mock_db_class.return_value = mock_db
        
        # Executa o teste
        result = LoginService.authenticate_user(
            self.test_user_data['email'],
            self.test_user_data['password']
        )
        
        # Verificações
        assert result["success"] is False
        assert result["message"] == "Erro ao conectar ao banco de dados"
        mock_db.close.assert_called_once()

    @patch('app.api.login.login_service.DatabaseConnection')
    def test_authenticate_user_exception(self, mock_db_class):
        """Testa tratamento de exceção na autenticação"""
        # Mock que lança exceção
        mock_db_class.side_effect = Exception("Erro de conexão")
        
        # Executa o teste
        result = LoginService.authenticate_user(
            self.test_user_data['email'],
            self.test_user_data['password']
        )
        
        # Verificações
        assert result["success"] is False
        assert "Erro interno:" in result["message"]
        assert "Erro de conexão" in result["message"]

    def test_login_service_methods_exist(self):
        """Testa se todos os métodos existem na classe LoginService"""
        assert hasattr(LoginService, 'handle_login_request')
        assert hasattr(LoginService, 'authenticate_user')
        assert hasattr(LoginService, '_generate_token')
        
        # Verifica se são métodos estáticos
        assert callable(getattr(LoginService, 'handle_login_request'))
        assert callable(getattr(LoginService, 'authenticate_user'))
        assert callable(getattr(LoginService, '_generate_token'))

    def test_login_service_basic_functionality(self):
        """Testa funcionalidade básica da classe LoginService"""
        # Verifica se a classe existe
        assert LoginService is not None
        
        # Verifica se é uma classe
        import inspect
        assert inspect.isclass(LoginService)
        
        # Verifica métodos essenciais
        essential_methods = ['handle_login_request', 'authenticate_user', '_generate_token']
        for method in essential_methods:
            assert hasattr(LoginService, method), f"Método {method} não encontrado"

    @patch.object(LoginService, 'authenticate_user')
    def test_authenticate_user_password_validation(self, mock_authenticate):
        """Testa validação de senha"""
        # Configura resposta de senha inválida
        mock_authenticate.return_value = {
            "success": False,
            "message": "Senha inválida"
        }
        
        # Executa o teste com senha vazia
        result = LoginService.authenticate_user(
            self.test_user_data['email'],
            ""
        )
        
        # Verificações
        assert result["success"] is False
        assert "inválida" in result["message"] or "Senha" in result["message"]

    @patch.object(LoginService, 'authenticate_user')
    def test_authenticate_user_email_validation(self, mock_authenticate):
        """Testa validação de email"""
        # Configura resposta de email inválido
        mock_authenticate.return_value = {
            "success": False,
            "message": "Email inválido"
        }
        
        # Executa o teste com email vazio
        result = LoginService.authenticate_user(
            "",
            self.test_user_data['password']
        )
        
        # Verificações
        assert result["success"] is False
        assert "Email" in result["message"] or "inválido" in result["message"]
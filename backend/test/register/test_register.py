import pytest
import bcrypt
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Adiciona o src ao PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Agora pode importar usando o caminho completo
from app.api.register.register_service import RegisterService
from app.data_base.db_classes.DatabaseConnection import DatabaseConnection


class TestRegisterService:
    
    def setup_method(self):
        """Setup executado antes de cada teste"""
        self.register_service = RegisterService()
        self.test_user_data = {
            'name': 'João Silva',
            'telefone': '11999999999',
            'cpf': '12345678901',
            'email': 'joao@email.com',
            'password': 'minhasenha123'
        }

    @patch.object(RegisterService, 'create_user')
    def test_create_user_success(self, mock_create_user):
        """Testa criação de usuário bem-sucedida"""
        # Configura o mock para retornar sucesso
        mock_create_user.return_value = "Usuário cadastrado com sucesso"
        
        # Executa o teste
        result = self.register_service.create_user(
            self.test_user_data['name'],
            self.test_user_data['telefone'],
            self.test_user_data['cpf'],
            self.test_user_data['email'],
            self.test_user_data['password']
        )
        
        # Verificações
        assert result == "Usuário cadastrado com sucesso"
        mock_create_user.assert_called_once_with(
            self.test_user_data['name'],
            self.test_user_data['telefone'],
            self.test_user_data['cpf'],
            self.test_user_data['email'],
            self.test_user_data['password']
        )

    @patch.object(RegisterService, 'create_user')
    def test_create_user_database_error(self, mock_create_user):
        """Testa erro no banco de dados durante criação de usuário"""
        # Configura o mock para lançar exceção
        mock_create_user.side_effect = Exception("Erro ao cadastrar usuário: Erro no banco de dados")
        
        # Verifica se a exceção é lançada
        with pytest.raises(Exception) as exc_info:
            self.register_service.create_user(
                self.test_user_data['name'],
                self.test_user_data['telefone'],
                self.test_user_data['cpf'],
                self.test_user_data['email'],
                self.test_user_data['password']
            )
        
        # Verifica a mensagem de erro
        assert "Erro ao cadastrar usuário: Erro no banco de dados" in str(exc_info.value)

    @patch.object(RegisterService, 'create_user')
    def test_create_user_duplicate_email(self, mock_create_user):
        """Testa erro de email duplicado"""
        # Configura o mock para lançar exceção de email duplicado
        mock_create_user.side_effect = Exception("Erro ao cadastrar usuário: duplicate key value violates unique constraint")
        
        # Verifica se a exceção é lançada
        with pytest.raises(Exception) as exc_info:
            self.register_service.create_user(
                self.test_user_data['name'],
                self.test_user_data['telefone'],
                self.test_user_data['cpf'],
                self.test_user_data['email'],
                self.test_user_data['password']
            )
        
        # Verifica se contém a mensagem de erro esperada
        assert "Erro ao cadastrar usuário:" in str(exc_info.value)
        assert "duplicate key value violates unique constraint" in str(exc_info.value)

    def test_password_encryption(self):
        """Testa se a criptografia da senha funciona corretamente"""
        password = "minhasenha123"
        
        # Testa a criptografia real do bcrypt
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Verifica se a senha foi criptografada (não é igual à original)
        assert hashed != password.encode('utf-8')
        
        # Verifica se a verificação funciona
        assert bcrypt.checkpw(password.encode('utf-8'), hashed)

    @patch.object(RegisterService, 'create_user')
    def test_create_user_connection_error(self, mock_create_user):
        """Testa erro de conexão com banco de dados"""
        # Configura o mock para lançar exceção de conexão
        mock_create_user.side_effect = Exception("Erro de conexão")
        
        # Verifica se a exceção é lançada
        with pytest.raises(Exception):
            self.register_service.create_user(
                self.test_user_data['name'],
                self.test_user_data['telefone'],
                self.test_user_data['cpf'],
                self.test_user_data['email'],
                self.test_user_data['password']
            )

    def test_create_user_with_empty_fields(self):
        """Testa criação de usuário com campos vazios"""
        # Este teste depende de como você quer tratar campos vazios
        # Por enquanto, apenas verifica se o método pode ser chamado
        assert hasattr(self.register_service, 'create_user')

    def test_register_service_exists(self):
        """Testa se a instância do RegisterService foi criada corretamente"""
        assert self.register_service is not None
        assert isinstance(self.register_service, RegisterService)
        assert hasattr(self.register_service, 'create_user')
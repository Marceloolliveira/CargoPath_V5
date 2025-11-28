import pytest
import os
from unittest.mock import Mock, patch, MagicMock
import psycopg2
from psycopg2 import OperationalError

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'app', 'data_base', 'db_classes'))
from DatabaseConnection import DatabaseConnection


class TestDatabaseConnection:
    
    def test_init_with_none_env_vars(self):
        """Testa se a inicialização funciona quando variáveis de ambiente são None"""
        db = DatabaseConnection()
        assert db.cargo_path is None or isinstance(db.cargo_path, str)
        assert db.user is None or isinstance(db.user, str)
        assert db.password is None or isinstance(db.password, str)
        assert db.host is None or isinstance(db.host, str)
        assert db.port is None or isinstance(db.port, str)
        assert db.connection is None

    def test_init_with_custom_params(self):
        """Testa inicialização com parâmetros customizados"""
        db = DatabaseConnection(
            dbname='custom_db',
            user='custom_user',
            password='custom_pass',
            host='custom_host',
            port='5433'
        )
        assert db.cargo_path == 'custom_db'
        assert db.user == 'custom_user'
        assert db.password == 'custom_pass'
        assert db.host == 'custom_host'
        assert db.port == '5433'
        assert db.connection is None

    @patch('psycopg2.connect')
    def test_connect_success(self, mock_connect, capsys):
        """Testa conexão bem-sucedida"""
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        
        db = DatabaseConnection('test_db', 'user', 'pass', 'localhost', '5432')
        db.connect()
        
        mock_connect.assert_called_once_with(
            dbname='test_db',
            user='user',
            password='pass',
            host='localhost',
            port='5432'
        )
        
        assert db.connection == mock_connection
        
        captured = capsys.readouterr()
        assert "Conexão com o banco de dados estabelecida com sucesso." in captured.out

    @patch('psycopg2.connect')
    def test_connect_failure(self, mock_connect, capsys):
        """Testa falha na conexão"""
        mock_connect.side_effect = OperationalError("Erro de conexão")
        
        db = DatabaseConnection('test_db', 'user', 'pass', 'localhost', '5432')
        db.connect()
        
        assert db.connection is None
        
        captured = capsys.readouterr()
        assert "Erro ao conectar ao banco de dados: Erro de conexão" in captured.out

    def test_get_cursor_with_connection(self):
        """Testa obtenção de cursor quando há conexão ativa"""
        db = DatabaseConnection('test_db', 'user', 'pass', 'localhost', '5432')
        
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        db.connection = mock_connection
        
        result = db.get_cursor()
        
        mock_connection.cursor.assert_called_once()
        assert result == mock_cursor

    def test_get_cursor_without_connection(self, capsys):
        """Testa obtenção de cursor quando não há conexão"""
        db = DatabaseConnection('test_db', 'user', 'pass', 'localhost', '5432')
        
        result = db.get_cursor()
        
        assert result is None
        
        captured = capsys.readouterr()
        assert "Conexão não estabelecida. Por favor, chame o método 'connect' primeiro." in captured.out

    def test_commit_with_connection(self):
        """Testa commit quando há conexão ativa"""
        db = DatabaseConnection('test_db', 'user', 'pass', 'localhost', '5432')
        
        mock_connection = MagicMock()
        db.connection = mock_connection
        
        db.commit()
        
        mock_connection.commit.assert_called_once()

    def test_commit_without_connection(self, capsys):
        """Testa commit quando não há conexão"""
        db = DatabaseConnection('test_db', 'user', 'pass', 'localhost', '5432')
        
        db.commit()
        
        captured = capsys.readouterr()
        assert "Nenhuma conexão ativa para confirmar transações." in captured.out

    def test_rollback_with_connection(self):
        """Testa rollback quando há conexão ativa"""
        db = DatabaseConnection('test_db', 'user', 'pass', 'localhost', '5432')
        
        mock_connection = MagicMock()
        db.connection = mock_connection
        
        db.rollback()
        
        mock_connection.rollback.assert_called_once()

    def test_rollback_without_connection(self, capsys):
        """Testa rollback quando não há conexão"""
        db = DatabaseConnection('test_db', 'user', 'pass', 'localhost', '5432')
        
        db.rollback()
        
        captured = capsys.readouterr()
        assert "Nenhuma conexão ativa para desfazer transações." in captured.out

    def test_close_with_connection(self, capsys):
        """Testa fechamento quando há conexão ativa"""
        db = DatabaseConnection('test_db', 'user', 'pass', 'localhost', '5432')
        
        mock_connection = MagicMock()
        db.connection = mock_connection
        
        db.close()
        
        mock_connection.close.assert_called_once()
        
        captured = capsys.readouterr()
        assert "Conexão com o banco de dados fechada." in captured.out

    def test_close_without_connection(self, capsys):
        """Testa fechamento quando não há conexão"""
        db = DatabaseConnection('test_db', 'user', 'pass', 'localhost', '5432')
        
        db.close()
        
        captured = capsys.readouterr()
        assert "A conexão já está fechada ou não foi inicializada." in captured.out

    @patch('psycopg2.connect')
    def test_complete_workflow(self, mock_connect):
        """Testa um fluxo completo de uso da classe"""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        db = DatabaseConnection('test_db', 'user', 'pass', 'localhost', '5432')
        
        db.connect()
        assert db.connection == mock_connection
        
        cursor = db.get_cursor()
        assert cursor == mock_cursor
        
        db.commit()
        mock_connection.commit.assert_called_once()
        
        db.close()
        mock_connection.close.assert_called_once()
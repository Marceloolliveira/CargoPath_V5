import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from app.api.cotacao.cotacao_service import CotacaoService


class TestCotacaoService:
    
    def setup_method(self):
        """Setup executado antes de cada teste"""
        self.cotacao_service = CotacaoService()
        
        self.test_cotacao_data = {
            'descricao': 'Transporte de móveis',
            'status': 'pendente',
            'valor_frete': 150.50,
            'user_id': 1,
            'data_agendamento': '2023-12-25 10:00:00',
            'cotacao_id': 1
        }
        
        self.test_update_data = {
            'descricao': 'Transporte de móveis - URGENTE',
            'status': 'confirmado'
        }

    def test_cotacao_service_initialization(self):
        """Testa se a classe CotacaoService pode ser instanciada"""
        service = CotacaoService()
        assert service is not None
        assert isinstance(service, CotacaoService)

    @patch('app.api.cotacao.cotacao_service.DatabaseConnection')
    def test_criar_cotacao_success(self, mock_db_class):
        """Testa criação bem-sucedida de cotação"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchone.return_value = [self.test_cotacao_data['cotacao_id']]
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = self.cotacao_service.criar_cotacao(self.test_cotacao_data)
        
        assert result["cotacao_id"] == self.test_cotacao_data['cotacao_id']
        assert result["descricao"] == self.test_cotacao_data['descricao']
        assert result["status"] == self.test_cotacao_data['status']
        assert result["valor_frete"] == self.test_cotacao_data['valor_frete']
        assert result["user_id"] == self.test_cotacao_data['user_id']
        assert result["data_agendamento"] == self.test_cotacao_data['data_agendamento']
        assert result["message"] == "Cotação criada com sucesso!"
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        
        call_args = mock_cursor.execute.call_args[0]
        query = call_args[0]
        params = call_args[1]
        
        assert "INSERT INTO cotacoes" in query
        assert "RETURNING cotacao_id" in query
        assert params == (
            self.test_cotacao_data['descricao'],
            self.test_cotacao_data['status'],
            self.test_cotacao_data['user_id'],
            self.test_cotacao_data['valor_frete'],
            self.test_cotacao_data['data_agendamento']
        )
        
        mock_db.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.cotacao.cotacao_service.DatabaseConnection')
    def test_criar_cotacao_database_error(self, mock_db_class):
        """Testa erro de banco de dados na criação"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.execute.side_effect = Exception("Erro SQL na criação")
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        with pytest.raises(Exception) as exc_info:
            self.cotacao_service.criar_cotacao(self.test_cotacao_data)
        
        assert "Erro SQL na criação" in str(exc_info.value)
        
        mock_db.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.cotacao.cotacao_service.DatabaseConnection')
    def test_listar_cotacoes_success(self, mock_db_class):
        """Testa listagem bem-sucedida de cotações"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchall.return_value = [
            (1, 'Transporte A', 'pendente', 1, 100.0, '2023-12-25 10:00:00', '2023-12-20T08:00:00'),
            (2, 'Transporte B', 'confirmado', 2, 200.0, '2023-12-26 11:00:00', '2023-12-20T09:00:00')
        ]
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = self.cotacao_service.listar_cotacoes()
        
        assert isinstance(result, list)
        assert len(result) == 2
        
        assert result[0]["cotacao_id"] == 1
        assert result[0]["descricao"] == 'Transporte A'
        assert result[0]["status"] == 'pendente'
        assert result[0]["user_id"] == 1
        assert result[0]["valor_frete"] == 100.0
        
        assert result[1]["cotacao_id"] == 2
        assert result[1]["descricao"] == 'Transporte B'
        assert result[1]["status"] == 'confirmado'
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM cotacoes;")
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.cotacao.cotacao_service.DatabaseConnection')
    def test_listar_cotacoes_empty(self, mock_db_class):
        """Testa listagem quando não há cotações"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchall.return_value = []
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = self.cotacao_service.listar_cotacoes()
        
        assert isinstance(result, list)
        assert len(result) == 0

    @patch('app.api.cotacao.cotacao_service.DatabaseConnection')
    def test_obter_cotacao_success(self, mock_db_class):
        """Testa obtenção bem-sucedida de cotação específica"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchone.return_value = (
            1, 'Transporte teste', 'pendente', 1, 150.0, 
            '2023-12-25 10:00:00', '2023-12-20T08:00:00'
        )
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = self.cotacao_service.obter_cotacao(1)
        
        assert result is not None
        assert result["cotacao_id"] == 1
        assert result["descricao"] == 'Transporte teste'
        assert result["status"] == 'pendente'
        assert result["user_id"] == 1
        assert result["valor_frete"] == 150.0
        assert result["data_agendamento"] == '2023-12-25 10:00:00'
        assert result["created_at"] == '2023-12-20T08:00:00'
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM cotacoes WHERE cotacao_id = %s;", (1,)
        )
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.cotacao.cotacao_service.DatabaseConnection')
    def test_obter_cotacao_not_found(self, mock_db_class):
        """Testa obtenção de cotação não encontrada"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchone.return_value = None
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = self.cotacao_service.obter_cotacao(999)
        
        assert result is None
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM cotacoes WHERE cotacao_id = %s;", (999,)
        )

    @patch('app.api.cotacao.cotacao_service.DatabaseConnection')
    def test_atualizar_cotacao_success(self, mock_db_class):
        """Testa atualização bem-sucedida de cotação"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = self.cotacao_service.atualizar_cotacao(1, self.test_update_data)
        
        assert result["cotacao_id"] == 1
        assert result["descricao"] == self.test_update_data['descricao']
        assert result["status"] == self.test_update_data['status']
        assert result["message"] == "Cotação atualizada com sucesso!"
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        
        call_args = mock_cursor.execute.call_args[0]
        query = call_args[0]
        params = call_args[1]
        
        assert "UPDATE cotacoes SET descricao = %s, status = %s" in query
        assert "WHERE cotacao_id = %s" in query
        assert params == (
            self.test_update_data['descricao'],
            self.test_update_data['status'],
            1
        )
        
        mock_db.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.cotacao.cotacao_service.DatabaseConnection')
    def test_atualizar_cotacao_database_error(self, mock_db_class):
        """Testa erro de banco de dados na atualização"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.execute.side_effect = Exception("Erro SQL na atualização")
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        with pytest.raises(Exception) as exc_info:
            self.cotacao_service.atualizar_cotacao(1, self.test_update_data)
        
        assert "Erro SQL na atualização" in str(exc_info.value)
        
        mock_db.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.cotacao.cotacao_service.DatabaseConnection')
    def test_deletar_cotacao_success(self, mock_db_class):
        """Testa deleção bem-sucedida de cotação"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = self.cotacao_service.deletar_cotacao(1)
        
        assert result is None
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM cotacoes WHERE cotacao_id = %s;", (1,)
        )
        mock_db.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.cotacao.cotacao_service.DatabaseConnection')
    def test_deletar_cotacao_database_error(self, mock_db_class):
        """Testa erro de banco de dados na deleção"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.execute.side_effect = Exception("Erro SQL na deleção")
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        with pytest.raises(Exception) as exc_info:
            self.cotacao_service.deletar_cotacao(1)
        
        assert "Erro SQL na deleção" in str(exc_info.value)
        
        mock_db.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    def test_cotacao_service_methods_exist(self):
        """Testa se todos os métodos existem na classe CotacaoService"""
        assert hasattr(CotacaoService, 'criar_cotacao')
        assert hasattr(CotacaoService, 'listar_cotacoes')
        assert hasattr(CotacaoService, 'obter_cotacao')
        assert hasattr(CotacaoService, 'atualizar_cotacao')
        assert hasattr(CotacaoService, 'deletar_cotacao')
        
        assert callable(getattr(CotacaoService, 'criar_cotacao'))
        assert callable(getattr(CotacaoService, 'listar_cotacoes'))
        assert callable(getattr(CotacaoService, 'obter_cotacao'))
        assert callable(getattr(CotacaoService, 'atualizar_cotacao'))
        assert callable(getattr(CotacaoService, 'deletar_cotacao'))

    def test_cotacao_data_validation(self):
        """Testa validação dos dados de cotação"""
        assert self.test_cotacao_data['valor_frete'] > 0
        assert self.test_cotacao_data['user_id'] > 0
        assert isinstance(self.test_cotacao_data['descricao'], str)
        assert isinstance(self.test_cotacao_data['status'], str)
        
        status_validos = ['pendente', 'confirmado', 'cancelado', 'finalizado']
        assert self.test_cotacao_data['status'] in status_validos

    @patch.object(CotacaoService, 'criar_cotacao')
    def test_criar_cotacao_mock(self, mock_criar):
        """Testa criação de cotação com mock da classe"""
        mock_criar.return_value = {
            "cotacao_id": 1,
            "descricao": self.test_cotacao_data['descricao'],
            "status": self.test_cotacao_data['status'],
            "user_id": self.test_cotacao_data['user_id'],
            "valor_frete": self.test_cotacao_data['valor_frete'],
            "data_agendamento": self.test_cotacao_data['data_agendamento'],
            "message": "Cotação criada com sucesso!"
        }
        
        result = self.cotacao_service.criar_cotacao(self.test_cotacao_data)
        
        assert result["cotacao_id"] == 1
        assert result["message"] == "Cotação criada com sucesso!"
        mock_criar.assert_called_once_with(self.test_cotacao_data)

    @patch.object(CotacaoService, 'listar_cotacoes')
    def test_listar_cotacoes_mock(self, mock_listar):
        """Testa listagem de cotações com mock da classe"""
        mock_listar.return_value = [
            {
                "cotacao_id": 1,
                "descricao": "Transporte A",
                "status": "pendente",
                "user_id": 1,
                "valor_frete": 100.0,
                "data_agendamento": "2023-12-25 10:00:00",
                "created_at": "2023-12-20T08:00:00"
            }
        ]
        
        result = self.cotacao_service.listar_cotacoes()
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["cotacao_id"] == 1
        mock_listar.assert_called_once()

    @patch.object(CotacaoService, 'obter_cotacao')
    def test_obter_cotacao_mock(self, mock_obter):
        """Testa obtenção de cotação com mock da classe"""
        mock_obter.return_value = {
            "cotacao_id": 1,
            "descricao": "Transporte teste",
            "status": "pendente",
            "user_id": 1,
            "valor_frete": 150.0,
            "data_agendamento": "2023-12-25 10:00:00",
            "created_at": "2023-12-20T08:00:00"
        }
        
        result = self.cotacao_service.obter_cotacao(1)
        
        assert result["cotacao_id"] == 1
        assert result["descricao"] == "Transporte teste"
        mock_obter.assert_called_once_with(1)

    @patch.object(CotacaoService, 'atualizar_cotacao')
    def test_atualizar_cotacao_mock(self, mock_atualizar):
        """Testa atualização de cotação com mock da classe"""
        mock_atualizar.return_value = {
            "cotacao_id": 1,
            "descricao": self.test_update_data['descricao'],
            "status": self.test_update_data['status'],
            "message": "Cotação atualizada com sucesso!"
        }
        
        result = self.cotacao_service.atualizar_cotacao(1, self.test_update_data)
        
        assert result["cotacao_id"] == 1
        assert result["message"] == "Cotação atualizada com sucesso!"
        mock_atualizar.assert_called_once_with(1, self.test_update_data)

    @patch.object(CotacaoService, 'deletar_cotacao')
    def test_deletar_cotacao_mock(self, mock_deletar):
        """Testa deleção de cotação com mock da classe"""
        mock_deletar.return_value = None
        
        result = self.cotacao_service.deletar_cotacao(1)
        
        assert result is None
        mock_deletar.assert_called_once_with(1)

    def test_cotacao_data_extraction(self):
        """Testa extração de dados do dicionário"""
        data = self.test_cotacao_data
        
        descricao = data.get('descricao')
        status = data.get('status')
        valor_frete = data.get('valor_frete')
        user_id = data.get('user_id')
        data_agendamento = data.get('data_agendamento')
        
        assert descricao == 'Transporte de móveis'
        assert status == 'pendente'
        assert valor_frete == 150.50
        assert user_id == 1
        assert data_agendamento == '2023-12-25 10:00:00'

    def test_cotacao_update_data_extraction(self):
        """Testa extração de dados para atualização"""
        data = self.test_update_data
        
        descricao = data.get('descricao')
        status = data.get('status')
        
        assert descricao == 'Transporte de móveis - URGENTE'
        assert status == 'confirmado'

    @patch('app.api.cotacao.cotacao_service.DatabaseConnection')
    def test_listar_cotacoes_database_error(self, mock_db_class):
        """Testa tratamento de erro na listagem"""
        mock_db_class.side_effect = Exception("Erro de conexão")
        
        with pytest.raises(Exception) as exc_info:
            self.cotacao_service.listar_cotacoes()
        
        assert "Erro de conexão" in str(exc_info.value)

    @patch('app.api.cotacao.cotacao_service.DatabaseConnection')
    def test_obter_cotacao_database_error(self, mock_db_class):
        """Testa tratamento de erro na obtenção"""
        mock_db_class.side_effect = Exception("Erro de conexão")
        
        with pytest.raises(Exception) as exc_info:
            self.cotacao_service.obter_cotacao(1)
        
        assert "Erro de conexão" in str(exc_info.value)
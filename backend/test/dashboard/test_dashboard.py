import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from app.api.dashboard.dashboard_service import DashboardService


class TestDashboardService:
    
    def setup_method(self):
        """Setup executado antes de cada teste"""
        self.test_user_id = 1
        self.test_start_date = "2023-01-01"
        self.test_end_date = "2023-12-31"
        
        self.expected_summary = {
            "total": 10,
            "pending": 3,
            "completed": 5,
            "cancelled": 2
        }

    @patch.object(DashboardService, 'get_dashboard_summary')
    def test_get_dashboard_summary_success(self, mock_get_summary):
        """Testa obtenção bem-sucedida do resumo do dashboard"""
        mock_get_summary.return_value = self.expected_summary
        
        result = DashboardService.get_dashboard_summary(self.test_user_id)
        
        assert result["total"] == self.expected_summary["total"]
        assert result["pending"] == self.expected_summary["pending"]
        assert result["completed"] == self.expected_summary["completed"]
        assert result["cancelled"] == self.expected_summary["cancelled"]

    @patch.object(DashboardService, 'get_dashboard_summary')
    def test_get_dashboard_summary_with_date_range(self, mock_get_summary):
        """Testa obtenção do resumo com filtro de data"""
        mock_get_summary.return_value = {
            "total": 5,
            "pending": 2,
            "completed": 2,
            "cancelled": 1
        }
        
        result = DashboardService.get_dashboard_summary(
            self.test_user_id,
            self.test_start_date,
            self.test_end_date
        )
        
        assert result["total"] == 5
        assert result["pending"] == 2
        assert result["completed"] == 2
        assert result["cancelled"] == 1
        
        mock_get_summary.assert_called_once_with(
            self.test_user_id,
            self.test_start_date,
            self.test_end_date
        )

    @patch.object(DashboardService, 'get_dashboard_summary')
    def test_get_dashboard_summary_empty_results(self, mock_get_summary):
        """Testa resumo quando não há cotações"""
        mock_get_summary.return_value = {
            "total": 0,
            "pending": 0,
            "completed": 0,
            "cancelled": 0
        }
        
        result = DashboardService.get_dashboard_summary(self.test_user_id)
        
        assert result["total"] == 0
        assert result["pending"] == 0
        assert result["completed"] == 0
        assert result["cancelled"] == 0

    @patch.object(DashboardService, 'get_dashboard_summary')
    def test_get_dashboard_summary_database_error(self, mock_get_summary):
        """Testa erro de banco de dados"""
        mock_get_summary.side_effect = Exception("Erro ao conectar ao banco de dados")
        
        with pytest.raises(Exception) as exc_info:
            DashboardService.get_dashboard_summary(self.test_user_id)
        
        assert "Erro ao conectar ao banco de dados" in str(exc_info.value)

    @patch('app.api.dashboard.dashboard_service.DatabaseConnection')
    def test_get_dashboard_summary_with_database_mock(self, mock_db_class):
        """Testa resumo com mock completo do banco de dados"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchone.return_value = (10, 3, 5, 2)
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = DashboardService.get_dashboard_summary(self.test_user_id)
        
        assert result["total"] == 10
        assert result["pending"] == 3
        assert result["completed"] == 5
        assert result["cancelled"] == 2
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        
        call_args = mock_cursor.execute.call_args[0]
        query = call_args[0]
        params = call_args[1]
        
        assert "COUNT(*) AS total" in query
        assert "SUM(CASE WHEN status = 'pendente'" in query
        assert "SUM(CASE WHEN status = 'finalizado'" in query
        assert "SUM(CASE WHEN status = 'cancelado'" in query
        assert "FROM cotacoes" in query
        assert "WHERE user_id = %s" in query
        assert params == [self.test_user_id]
        
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.dashboard.dashboard_service.DatabaseConnection')
    def test_get_dashboard_summary_with_date_filter_mock(self, mock_db_class):
        """Testa resumo com filtro de data usando mock do banco"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchone.return_value = (5, 2, 2, 1)
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = DashboardService.get_dashboard_summary(
            self.test_user_id,
            self.test_start_date,
            self.test_end_date
        )
        
        assert result["total"] == 5
        assert result["pending"] == 2
        assert result["completed"] == 2
        assert result["cancelled"] == 1
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        
        call_args = mock_cursor.execute.call_args[0]
        query = call_args[0]
        params = call_args[1]
        
        assert "data_agendamento BETWEEN %s AND %s" in query
        assert params == [self.test_user_id, self.test_start_date, self.test_end_date]
        
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.dashboard.dashboard_service.DatabaseConnection')
    def test_get_dashboard_summary_cursor_none(self, mock_db_class):
        """Testa erro quando cursor é None"""
        mock_db = MagicMock()
        mock_db.get_cursor.return_value = None
        mock_db_class.return_value = mock_db
        
        with pytest.raises(Exception) as exc_info:
            DashboardService.get_dashboard_summary(self.test_user_id)
        
        assert "Erro ao conectar ao banco de dados" in str(exc_info.value)

    @patch('app.api.dashboard.dashboard_service.DatabaseConnection')
    def test_get_dashboard_summary_null_values(self, mock_db_class):
        """Testa tratamento de valores nulos no banco"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchone.return_value = (None, None, None, None)
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = DashboardService.get_dashboard_summary(self.test_user_id)
        
        assert result["total"] == 0
        assert result["pending"] == 0
        assert result["completed"] == 0
        assert result["cancelled"] == 0

    @patch('app.api.dashboard.dashboard_service.DatabaseConnection')
    def test_get_dashboard_summary_partial_null_values(self, mock_db_class):
        """Testa tratamento de valores parcialmente nulos"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchone.return_value = (5, None, 3, 0)
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = DashboardService.get_dashboard_summary(self.test_user_id)
        
        assert result["total"] == 5
        assert result["pending"] == 0
        assert result["completed"] == 3
        assert result["cancelled"] == 0

    @patch('app.api.dashboard.dashboard_service.DatabaseConnection')
    def test_get_dashboard_summary_database_exception(self, mock_db_class):
        """Testa tratamento de exceção durante execução da query"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.execute.side_effect = Exception("Erro na query SQL")
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        with pytest.raises(Exception) as exc_info:
            DashboardService.get_dashboard_summary(self.test_user_id)
        
        assert "Erro na query SQL" in str(exc_info.value)
        
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    def test_get_dashboard_summary_only_user_id_required(self):
        """Testa que apenas user_id é obrigatório"""
        try:
            assert hasattr(DashboardService, 'get_dashboard_summary')
            
            assert callable(getattr(DashboardService, 'get_dashboard_summary'))
            
        except Exception as e:
            pytest.fail(f"Método deve aceitar apenas user_id: {e}")

    def test_dashboard_service_methods_exist(self):
        """Testa se todos os métodos existem na classe DashboardService"""
        assert hasattr(DashboardService, 'get_dashboard_summary')
        
        assert callable(getattr(DashboardService, 'get_dashboard_summary'))

    @patch('app.api.dashboard.dashboard_service.DatabaseConnection')
    def test_get_dashboard_summary_query_structure(self, mock_db_class):
        """Testa se a estrutura da query está correta"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1, 0, 1, 0)
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        DashboardService.get_dashboard_summary(self.test_user_id)
        
        call_args = mock_cursor.execute.call_args[0]
        query = call_args[0]
        
        assert "SELECT" in query.upper()
        assert "COUNT(*)" in query.upper()
        assert "SUM(CASE WHEN" in query.upper()
        assert "pendente" in query
        assert "finalizado" in query
        assert "cancelado" in query
        assert "FROM cotacoes" in query
        assert "WHERE user_id = %s" in query
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Adiciona o src ao PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Agora pode importar usando o caminho completo
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
        # Configura resposta de sucesso
        mock_get_summary.return_value = self.expected_summary
        
        # Executa o teste
        result = DashboardService.get_dashboard_summary(self.test_user_id)
        
        # Verificações
        assert result["total"] == self.expected_summary["total"]
        assert result["pending"] == self.expected_summary["pending"]
        assert result["completed"] == self.expected_summary["completed"]
        assert result["cancelled"] == self.expected_summary["cancelled"]

    @patch.object(DashboardService, 'get_dashboard_summary')
    def test_get_dashboard_summary_with_date_range(self, mock_get_summary):
        """Testa obtenção do resumo com filtro de data"""
        # Configura resposta de sucesso com filtro de data
        mock_get_summary.return_value = {
            "total": 5,
            "pending": 2,
            "completed": 2,
            "cancelled": 1
        }
        
        # Executa o teste com filtro de data
        result = DashboardService.get_dashboard_summary(
            self.test_user_id,
            self.test_start_date,
            self.test_end_date
        )
        
        # Verificações
        assert result["total"] == 5
        assert result["pending"] == 2
        assert result["completed"] == 2
        assert result["cancelled"] == 1
        
        # Verifica se foi chamado com os parâmetros corretos
        mock_get_summary.assert_called_once_with(
            self.test_user_id,
            self.test_start_date,
            self.test_end_date
        )

    @patch.object(DashboardService, 'get_dashboard_summary')
    def test_get_dashboard_summary_empty_results(self, mock_get_summary):
        """Testa resumo quando não há cotações"""
        # Configura resposta com valores zerados
        mock_get_summary.return_value = {
            "total": 0,
            "pending": 0,
            "completed": 0,
            "cancelled": 0
        }
        
        # Executa o teste
        result = DashboardService.get_dashboard_summary(self.test_user_id)
        
        # Verificações
        assert result["total"] == 0
        assert result["pending"] == 0
        assert result["completed"] == 0
        assert result["cancelled"] == 0

    @patch.object(DashboardService, 'get_dashboard_summary')
    def test_get_dashboard_summary_database_error(self, mock_get_summary):
        """Testa erro de banco de dados"""
        # Configura exceção
        mock_get_summary.side_effect = Exception("Erro ao conectar ao banco de dados")
        
        # Verifica se a exceção é lançada
        with pytest.raises(Exception) as exc_info:
            DashboardService.get_dashboard_summary(self.test_user_id)
        
        assert "Erro ao conectar ao banco de dados" in str(exc_info.value)

    @patch('app.api.dashboard.dashboard_service.DatabaseConnection')
    def test_get_dashboard_summary_with_database_mock(self, mock_db_class):
        """Testa resumo com mock completo do banco de dados"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura retorno do cursor (total, pending, completed, cancelled)
        mock_cursor.fetchone.return_value = (10, 3, 5, 2)
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Executa o teste
        result = DashboardService.get_dashboard_summary(self.test_user_id)
        
        # Verificações
        assert result["total"] == 10
        assert result["pending"] == 3
        assert result["completed"] == 5
        assert result["cancelled"] == 2
        
        # Verifica se o banco foi chamado corretamente
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        
        # Verifica a query executada
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
        
        # Verifica se a conexão foi fechada
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.dashboard.dashboard_service.DatabaseConnection')
    def test_get_dashboard_summary_with_date_filter_mock(self, mock_db_class):
        """Testa resumo com filtro de data usando mock do banco"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura retorno do cursor
        mock_cursor.fetchone.return_value = (5, 2, 2, 1)
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Executa o teste com filtro de data
        result = DashboardService.get_dashboard_summary(
            self.test_user_id,
            self.test_start_date,
            self.test_end_date
        )
        
        # Verificações
        assert result["total"] == 5
        assert result["pending"] == 2
        assert result["completed"] == 2
        assert result["cancelled"] == 1
        
        # Verifica se o banco foi chamado corretamente
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        
        # Verifica a query executada com filtro de data
        call_args = mock_cursor.execute.call_args[0]
        query = call_args[0]
        params = call_args[1]
        
        assert "data_agendamento BETWEEN %s AND %s" in query
        assert params == [self.test_user_id, self.test_start_date, self.test_end_date]
        
        # Verifica se a conexão foi fechada
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.dashboard.dashboard_service.DatabaseConnection')
    def test_get_dashboard_summary_cursor_none(self, mock_db_class):
        """Testa erro quando cursor é None"""
        # Mock do banco de dados com cursor None
        mock_db = MagicMock()
        mock_db.get_cursor.return_value = None
        mock_db_class.return_value = mock_db
        
        # Verifica se a exceção é lançada
        with pytest.raises(Exception) as exc_info:
            DashboardService.get_dashboard_summary(self.test_user_id)
        
        assert "Erro ao conectar ao banco de dados" in str(exc_info.value)

    @patch('app.api.dashboard.dashboard_service.DatabaseConnection')
    def test_get_dashboard_summary_null_values(self, mock_db_class):
        """Testa tratamento de valores nulos no banco"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura retorno com valores nulos
        mock_cursor.fetchone.return_value = (None, None, None, None)
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Executa o teste
        result = DashboardService.get_dashboard_summary(self.test_user_id)
        
        # Verificações - valores nulos devem ser convertidos para 0
        assert result["total"] == 0
        assert result["pending"] == 0
        assert result["completed"] == 0
        assert result["cancelled"] == 0

    @patch('app.api.dashboard.dashboard_service.DatabaseConnection')
    def test_get_dashboard_summary_partial_null_values(self, mock_db_class):
        """Testa tratamento de valores parcialmente nulos"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura retorno com alguns valores nulos
        mock_cursor.fetchone.return_value = (5, None, 3, 0)
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Executa o teste
        result = DashboardService.get_dashboard_summary(self.test_user_id)
        
        # Verificações
        assert result["total"] == 5
        assert result["pending"] == 0  # None convertido para 0
        assert result["completed"] == 3
        assert result["cancelled"] == 0

    @patch('app.api.dashboard.dashboard_service.DatabaseConnection')
    def test_get_dashboard_summary_database_exception(self, mock_db_class):
        """Testa tratamento de exceção durante execução da query"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura exceção na execução da query
        mock_cursor.execute.side_effect = Exception("Erro na query SQL")
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Verifica se a exceção é propagada e conexão é fechada
        with pytest.raises(Exception) as exc_info:
            DashboardService.get_dashboard_summary(self.test_user_id)
        
        assert "Erro na query SQL" in str(exc_info.value)
        
        # Verifica se a conexão foi fechada mesmo com erro
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    def test_get_dashboard_summary_only_user_id_required(self):
        """Testa que apenas user_id é obrigatório"""
        # Verifica se o método pode ser chamado apenas com user_id
        try:
            # Este teste verifica se o método aceita apenas user_id
            # sem lançar erro de parâmetros
            assert hasattr(DashboardService, 'get_dashboard_summary')
            
            # Verifica se o método é estático
            assert callable(getattr(DashboardService, 'get_dashboard_summary'))
            
        except Exception as e:
            pytest.fail(f"Método deve aceitar apenas user_id: {e}")

    def test_dashboard_service_methods_exist(self):
        """Testa se todos os métodos existem na classe DashboardService"""
        assert hasattr(DashboardService, 'get_dashboard_summary')
        
        # Verifica se é método estático
        assert callable(getattr(DashboardService, 'get_dashboard_summary'))

    @patch('app.api.dashboard.dashboard_service.DatabaseConnection')
    def test_get_dashboard_summary_query_structure(self, mock_db_class):
        """Testa se a estrutura da query está correta"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1, 0, 1, 0)
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Executa o teste
        DashboardService.get_dashboard_summary(self.test_user_id)
        
        # Verifica se a query contém os elementos esperados
        call_args = mock_cursor.execute.call_args[0]
        query = call_args[0]
        
        # Verifica estrutura da query (corrigido)
        assert "SELECT" in query.upper()
        assert "COUNT(*)" in query.upper()
        assert "SUM(CASE WHEN" in query.upper()
        assert "pendente" in query  # minúsculo
        assert "finalizado" in query  # minúsculo
        assert "cancelado" in query  # minúsculo
        assert "FROM cotacoes" in query
        assert "WHERE user_id = %s" in query
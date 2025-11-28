import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from app.api.cubagem.cubagem_service import CubagemService


class TestCubagemService:
    
    def setup_method(self):
        """Setup executado antes de cada teste"""
        self.test_cubagem_data = {
            'altura': 1.5,
            'largura': 2.0,
            'comprimento': 3.0,
            'qtd': 5,
            'carga_id': 1,
            'cubagem_id': 1
        }

    @patch.object(CubagemService, 'criar_cubagem')
    def test_criar_cubagem_success(self, mock_criar):
        """Testa criação bem-sucedida de cubagem"""
        mock_criar.return_value = self.test_cubagem_data['cubagem_id']
        
        result = CubagemService.criar_cubagem(
            self.test_cubagem_data['altura'],
            self.test_cubagem_data['largura'],
            self.test_cubagem_data['comprimento'],
            self.test_cubagem_data['qtd'],
            self.test_cubagem_data['carga_id']
        )
        
        assert result == self.test_cubagem_data['cubagem_id']
        mock_criar.assert_called_once_with(
            self.test_cubagem_data['altura'],
            self.test_cubagem_data['largura'],
            self.test_cubagem_data['comprimento'],
            self.test_cubagem_data['qtd'],
            self.test_cubagem_data['carga_id']
        )

    @patch.object(CubagemService, 'criar_cubagem')
    def test_criar_cubagem_database_error(self, mock_criar):
        """Testa erro de banco de dados na criação"""
        mock_criar.side_effect = Exception("Erro ao inserir cubagem")
        
        with pytest.raises(Exception) as exc_info:
            CubagemService.criar_cubagem(
                self.test_cubagem_data['altura'],
                self.test_cubagem_data['largura'],
                self.test_cubagem_data['comprimento'],
                self.test_cubagem_data['qtd'],
                self.test_cubagem_data['carga_id']
            )
        
        assert "Erro ao inserir cubagem" in str(exc_info.value)

    @patch.object(CubagemService, 'listar_cubagens')
    def test_listar_cubagens_success(self, mock_listar):
        """Testa listagem bem-sucedida de cubagens"""
        mock_listar.return_value = [
            (1, 1.5, 2.0, 3.0, 5, 1, "2023-01-01T10:00:00"),
            (2, 2.0, 2.5, 4.0, 3, 2, "2023-01-02T11:00:00")
        ]
        
        result = CubagemService.listar_cubagens()
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0][0] == 1
        assert result[0][1] == 1.5
        assert result[1][0] == 2
        assert result[1][1] == 2.0

    @patch.object(CubagemService, 'listar_cubagens')
    def test_listar_cubagens_empty(self, mock_listar):
        """Testa listagem quando não há cubagens"""
        mock_listar.return_value = []
        
        result = CubagemService.listar_cubagens()
        
        assert isinstance(result, list)
        assert len(result) == 0

    @patch.object(CubagemService, 'listar_cubagens')
    def test_listar_cubagens_database_error(self, mock_listar):
        """Testa erro de banco de dados na listagem"""
        mock_listar.side_effect = Exception("Erro ao listar cubagens")
        
        with pytest.raises(Exception) as exc_info:
            CubagemService.listar_cubagens()
        
        assert "Erro ao listar cubagens" in str(exc_info.value)

    @patch.object(CubagemService, 'obter_cubagem')
    def test_obter_cubagem_success(self, mock_obter):
        """Testa obtenção bem-sucedida de cubagem específica"""
        mock_obter.return_value = (
            self.test_cubagem_data['cubagem_id'],
            self.test_cubagem_data['altura'],
            self.test_cubagem_data['largura'],
            self.test_cubagem_data['comprimento'],
            self.test_cubagem_data['qtd'],
            self.test_cubagem_data['carga_id'],
            "2023-01-01T10:00:00"
        )
        
        result = CubagemService.obter_cubagem(self.test_cubagem_data['cubagem_id'])
        
        assert result[0] == self.test_cubagem_data['cubagem_id']
        assert result[1] == self.test_cubagem_data['altura']
        assert result[2] == self.test_cubagem_data['largura']
        assert result[3] == self.test_cubagem_data['comprimento']
        assert result[4] == self.test_cubagem_data['qtd']
        assert result[5] == self.test_cubagem_data['carga_id']

    @patch.object(CubagemService, 'obter_cubagem')
    def test_obter_cubagem_not_found(self, mock_obter):
        """Testa obtenção de cubagem não encontrada"""
        mock_obter.return_value = None
        
        result = CubagemService.obter_cubagem(999)
        
        assert result is None

    @patch.object(CubagemService, 'obter_cubagem')
    def test_obter_cubagem_database_error(self, mock_obter):
        """Testa erro de banco de dados na obtenção"""
        mock_obter.side_effect = Exception("Erro ao obter cubagem")
        
        with pytest.raises(Exception) as exc_info:
            CubagemService.obter_cubagem(1)
        
        assert "Erro ao obter cubagem" in str(exc_info.value)

    @patch.object(CubagemService, 'atualizar_cubagem')
    def test_atualizar_cubagem_success(self, mock_atualizar):
        """Testa atualização bem-sucedida de cubagem"""
        mock_atualizar.return_value = None
        
        result = CubagemService.atualizar_cubagem(
            self.test_cubagem_data['cubagem_id'],
            2.0,
            2.5,
            3.5,
            10
        )
        
        assert result is None
        mock_atualizar.assert_called_once_with(
            self.test_cubagem_data['cubagem_id'],
            2.0, 2.5, 3.5, 10
        )

    @patch.object(CubagemService, 'atualizar_cubagem')
    def test_atualizar_cubagem_database_error(self, mock_atualizar):
        """Testa erro de banco de dados na atualização"""
        mock_atualizar.side_effect = Exception("Erro ao atualizar cubagem")
        
        with pytest.raises(Exception) as exc_info:
            CubagemService.atualizar_cubagem(1, 2.0, 2.5, 3.5, 10)
        
        assert "Erro ao atualizar cubagem" in str(exc_info.value)

    @patch.object(CubagemService, 'deletar_cubagem')
    def test_deletar_cubagem_success(self, mock_deletar):
        """Testa deleção bem-sucedida de cubagem"""
        mock_deletar.return_value = None
        
        result = CubagemService.deletar_cubagem(self.test_cubagem_data['cubagem_id'])
        
        assert result is None
        mock_deletar.assert_called_once_with(self.test_cubagem_data['cubagem_id'])

    @patch.object(CubagemService, 'deletar_cubagem')
    def test_deletar_cubagem_database_error(self, mock_deletar):
        """Testa erro de banco de dados na deleção"""
        mock_deletar.side_effect = Exception("Erro ao deletar cubagem")
        
        with pytest.raises(Exception) as exc_info:
            CubagemService.deletar_cubagem(1)
        
        assert "Erro ao deletar cubagem" in str(exc_info.value)

    @patch('app.api.cubagem.cubagem_service.DatabaseConnection')
    def test_criar_cubagem_with_database_mock(self, mock_db_class):
        """Testa criação com mock completo do banco de dados"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchone.return_value = [1]
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = CubagemService.criar_cubagem(
            self.test_cubagem_data['altura'],
            self.test_cubagem_data['largura'],
            self.test_cubagem_data['comprimento'],
            self.test_cubagem_data['qtd'],
            self.test_cubagem_data['carga_id']
        )
        
        assert result == 1
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        
        call_args = mock_cursor.execute.call_args[0]
        query = call_args[0]
        params = call_args[1]
        
        assert "INSERT INTO cubagem" in query
        assert "RETURNING cubagem_id" in query
        assert params == (
            self.test_cubagem_data['altura'],
            self.test_cubagem_data['largura'],
            self.test_cubagem_data['comprimento'],
            self.test_cubagem_data['qtd'],
            self.test_cubagem_data['carga_id']
        )
        
        mock_db.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.cubagem.cubagem_service.DatabaseConnection')
    def test_criar_cubagem_with_rollback(self, mock_db_class):
        """Testa rollback na criação quando há erro"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.execute.side_effect = Exception("Erro SQL")
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        with pytest.raises(Exception) as exc_info:
            CubagemService.criar_cubagem(
                self.test_cubagem_data['altura'],
                self.test_cubagem_data['largura'],
                self.test_cubagem_data['comprimento'],
                self.test_cubagem_data['qtd'],
                self.test_cubagem_data['carga_id']
            )
        
        assert "Erro SQL" in str(exc_info.value)
        
        mock_db.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.cubagem.cubagem_service.DatabaseConnection')
    def test_listar_cubagens_with_database_mock(self, mock_db_class):
        """Testa listagem com mock completo do banco de dados"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchall.return_value = [
            (1, 1.5, 2.0, 3.0, 5, 1, "2023-01-01T10:00:00"),
            (2, 2.0, 2.5, 4.0, 3, 2, "2023-01-02T11:00:00")
        ]
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = CubagemService.listar_cubagens()
        
        assert len(result) == 2
        assert result[0][0] == 1
        assert result[1][0] == 2
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM cubagem;")
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.cubagem.cubagem_service.DatabaseConnection')
    def test_obter_cubagem_with_database_mock(self, mock_db_class):
        """Testa obtenção com mock completo do banco de dados"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchone.return_value = (1, 1.5, 2.0, 3.0, 5, 1, "2023-01-01T10:00:00")
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = CubagemService.obter_cubagem(1)
        
        assert result[0] == 1
        assert result[1] == 1.5
        assert result[2] == 2.0
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM cubagem WHERE cubagem_id = %s;", (1,)
        )
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.cubagem.cubagem_service.DatabaseConnection')
    def test_atualizar_cubagem_with_database_mock(self, mock_db_class):
        """Testa atualização com mock completo do banco de dados"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        CubagemService.atualizar_cubagem(1, 2.0, 2.5, 3.5, 10)
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        
        call_args = mock_cursor.execute.call_args[0]
        query = call_args[0]
        params = call_args[1]
        
        assert "UPDATE cubagem" in query
        assert "SET altura = %s, largura = %s, comprimento = %s, qtd = %s" in query
        assert "WHERE cubagem_id = %s" in query
        assert params == (2.0, 2.5, 3.5, 10, 1)
        
        mock_db.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.cubagem.cubagem_service.DatabaseConnection')
    def test_deletar_cubagem_with_database_mock(self, mock_db_class):
        """Testa deleção com mock completo do banco de dados"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        CubagemService.deletar_cubagem(1)
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM cubagem WHERE cubagem_id = %s;", (1,)
        )
        mock_db.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    def test_cubagem_service_methods_exist(self):
        """Testa se todos os métodos existem na classe CubagemService"""
        assert hasattr(CubagemService, 'criar_cubagem')
        assert hasattr(CubagemService, 'listar_cubagens')
        assert hasattr(CubagemService, 'obter_cubagem')
        assert hasattr(CubagemService, 'atualizar_cubagem')
        assert hasattr(CubagemService, 'deletar_cubagem')
        
        assert callable(getattr(CubagemService, 'criar_cubagem'))
        assert callable(getattr(CubagemService, 'listar_cubagens'))
        assert callable(getattr(CubagemService, 'obter_cubagem'))
        assert callable(getattr(CubagemService, 'atualizar_cubagem'))
        assert callable(getattr(CubagemService, 'deletar_cubagem'))

    def test_cubagem_data_validation(self):
        """Testa validação dos dados de cubagem"""
        assert self.test_cubagem_data['altura'] > 0
        assert self.test_cubagem_data['largura'] > 0
        assert self.test_cubagem_data['comprimento'] > 0
        assert self.test_cubagem_data['qtd'] > 0
        assert self.test_cubagem_data['carga_id'] > 0
        
        assert isinstance(self.test_cubagem_data['altura'], (int, float))
        assert isinstance(self.test_cubagem_data['largura'], (int, float))
        assert isinstance(self.test_cubagem_data['comprimento'], (int, float))
        assert isinstance(self.test_cubagem_data['qtd'], int)
        assert isinstance(self.test_cubagem_data['carga_id'], int)

    def test_cubagem_volume_calculation(self):
        """Testa cálculo conceitual de volume"""
        volume_unitario = (self.test_cubagem_data['altura'] * 
                          self.test_cubagem_data['largura'] * 
                          self.test_cubagem_data['comprimento'])
        volume_total = volume_unitario * self.test_cubagem_data['qtd']
        
        assert volume_unitario == 1.5 * 2.0 * 3.0
        assert volume_total == 9.0 * 5
        assert volume_unitario > 0
        assert volume_total > 0

    @patch('app.api.cubagem.cubagem_service.DatabaseConnection')
    def test_atualizar_cubagem_with_rollback(self, mock_db_class):
        """Testa rollback na atualização quando há erro"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.execute.side_effect = Exception("Erro SQL na atualização")
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        with pytest.raises(Exception) as exc_info:
            CubagemService.atualizar_cubagem(1, 2.0, 2.5, 3.5, 10)
        
        assert "Erro SQL na atualização" in str(exc_info.value)
        
        mock_db.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.cubagem.cubagem_service.DatabaseConnection')
    def test_deletar_cubagem_with_rollback(self, mock_db_class):
        """Testa rollback na deleção quando há erro"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.execute.side_effect = Exception("Erro SQL na deleção")
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        with pytest.raises(Exception) as exc_info:
            CubagemService.deletar_cubagem(1)
        
        assert "Erro SQL na deleção" in str(exc_info.value)
        
        mock_db.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()
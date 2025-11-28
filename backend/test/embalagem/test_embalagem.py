import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from app.api.embalagem.embalagem_service import EmbalagemService


class TestEmbalagemService:
    
    def setup_method(self):
        """Setup executado antes de cada teste"""
        self.test_embalagem_data = {
            'caixa': 10,
            'palet': 5,
            'grade': 3,
            'cubagem_id': 1,
            'embalagem_id': 1
        }

    @patch.object(EmbalagemService, 'criar_embalagem')
    def test_criar_embalagem_success(self, mock_criar):
        """Testa criação bem-sucedida de embalagem"""
        mock_criar.return_value = {
            "embalagem_id": self.test_embalagem_data['embalagem_id'],
            "caixa": self.test_embalagem_data['caixa'],
            "palet": self.test_embalagem_data['palet'],
            "grade": self.test_embalagem_data['grade'],
            "cubagem_id": self.test_embalagem_data['cubagem_id'],
            "message": "Embalagem criada com sucesso!"
        }
        
        result = EmbalagemService.criar_embalagem(self.test_embalagem_data)
        
        assert result["embalagem_id"] == self.test_embalagem_data['embalagem_id']
        assert result["caixa"] == self.test_embalagem_data['caixa']
        assert result["palet"] == self.test_embalagem_data['palet']
        assert result["grade"] == self.test_embalagem_data['grade']
        assert result["cubagem_id"] == self.test_embalagem_data['cubagem_id']
        assert result["message"] == "Embalagem criada com sucesso!"

    @patch.object(EmbalagemService, 'criar_embalagem')
    def test_criar_embalagem_database_error(self, mock_criar):
        """Testa erro de banco de dados na criação"""
        mock_criar.side_effect = Exception("Erro ao conectar ao banco de dados")
        
        with pytest.raises(Exception) as exc_info:
            EmbalagemService.criar_embalagem(self.test_embalagem_data)
        
        assert "Erro ao conectar ao banco de dados" in str(exc_info.value)

    @patch.object(EmbalagemService, 'listar_embalagens')
    def test_listar_embalagens_success(self, mock_listar):
        """Testa listagem bem-sucedida de embalagens"""
        mock_listar.return_value = [
            {
                "embalagem_id": 1,
                "caixa": 10,
                "palet": 5,
                "grade": 3,
                "cubagem_id": 1,
                "created_at": "2023-01-01T10:00:00"
            },
            {
                "embalagem_id": 2,
                "caixa": 20,
                "palet": 8,
                "grade": 6,
                "cubagem_id": 2,
                "created_at": "2023-01-02T11:00:00"
            }
        ]
        
        result = EmbalagemService.listar_embalagens()
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["embalagem_id"] == 1
        assert result[0]["caixa"] == 10
        assert result[1]["embalagem_id"] == 2
        assert result[1]["caixa"] == 20

    @patch.object(EmbalagemService, 'listar_embalagens')
    def test_listar_embalagens_empty(self, mock_listar):
        """Testa listagem quando não há embalagens"""
        mock_listar.return_value = []
        
        result = EmbalagemService.listar_embalagens()
        
        assert isinstance(result, list)
        assert len(result) == 0

    @patch.object(EmbalagemService, 'listar_embalagens')
    def test_listar_embalagens_database_error(self, mock_listar):
        """Testa erro de banco de dados na listagem"""
        mock_listar.side_effect = Exception("Erro ao conectar ao banco de dados")
        
        with pytest.raises(Exception) as exc_info:
            EmbalagemService.listar_embalagens()
        
        assert "Erro ao conectar ao banco de dados" in str(exc_info.value)

    @patch.object(EmbalagemService, 'obter_embalagem')
    def test_obter_embalagem_success(self, mock_obter):
        """Testa obtenção bem-sucedida de embalagem específica"""
        mock_obter.return_value = {
            "embalagem_id": self.test_embalagem_data['embalagem_id'],
            "caixa": self.test_embalagem_data['caixa'],
            "palet": self.test_embalagem_data['palet'],
            "grade": self.test_embalagem_data['grade'],
            "cubagem_id": self.test_embalagem_data['cubagem_id'],
            "created_at": "2023-01-01T10:00:00"
        }
        
        result = EmbalagemService.obter_embalagem(self.test_embalagem_data['embalagem_id'])
        
        assert result["embalagem_id"] == self.test_embalagem_data['embalagem_id']
        assert result["caixa"] == self.test_embalagem_data['caixa']
        assert result["palet"] == self.test_embalagem_data['palet']
        assert result["grade"] == self.test_embalagem_data['grade']
        assert result["cubagem_id"] == self.test_embalagem_data['cubagem_id']

    @patch.object(EmbalagemService, 'obter_embalagem')
    def test_obter_embalagem_not_found(self, mock_obter):
        """Testa obtenção de embalagem não encontrada"""
        mock_obter.return_value = None
        
        result = EmbalagemService.obter_embalagem(999)
        
        assert result is None

    @patch.object(EmbalagemService, 'obter_embalagem')
    def test_obter_embalagem_database_error(self, mock_obter):
        """Testa erro de banco de dados na obtenção"""
        mock_obter.side_effect = Exception("Erro ao conectar ao banco de dados")
        
        with pytest.raises(Exception) as exc_info:
            EmbalagemService.obter_embalagem(1)
        
        assert "Erro ao conectar ao banco de dados" in str(exc_info.value)

    @patch.object(EmbalagemService, 'atualizar_embalagem')
    def test_atualizar_embalagem_success(self, mock_atualizar):
        """Testa atualização bem-sucedida de embalagem"""
        update_data = {
            'caixa': 15,
            'palet': 7,
            'grade': 4
        }
        
        mock_atualizar.return_value = {
            "embalagem_id": self.test_embalagem_data['embalagem_id'],
            "caixa": update_data['caixa'],
            "palet": update_data['palet'],
            "grade": update_data['grade'],
            "message": "Embalagem atualizada com sucesso!"
        }
        
        result = EmbalagemService.atualizar_embalagem(
            self.test_embalagem_data['embalagem_id'],
            update_data
        )
        
        assert result["embalagem_id"] == self.test_embalagem_data['embalagem_id']
        assert result["caixa"] == update_data['caixa']
        assert result["palet"] == update_data['palet']
        assert result["grade"] == update_data['grade']
        assert result["message"] == "Embalagem atualizada com sucesso!"

    @patch.object(EmbalagemService, 'atualizar_embalagem')
    def test_atualizar_embalagem_database_error(self, mock_atualizar):
        """Testa erro de banco de dados na atualização"""
        mock_atualizar.side_effect = Exception("Erro ao conectar ao banco de dados")
        
        with pytest.raises(Exception) as exc_info:
            EmbalagemService.atualizar_embalagem(1, self.test_embalagem_data)
        
        assert "Erro ao conectar ao banco de dados" in str(exc_info.value)

    @patch.object(EmbalagemService, 'deletar_embalagem')
    def test_deletar_embalagem_success(self, mock_deletar):
        """Testa deleção bem-sucedida de embalagem"""
        mock_deletar.return_value = {
            "embalagem_id": self.test_embalagem_data['embalagem_id'],
            "message": "Embalagem deletada com sucesso!"
        }
        
        result = EmbalagemService.deletar_embalagem(self.test_embalagem_data['embalagem_id'])
        
        assert result["embalagem_id"] == self.test_embalagem_data['embalagem_id']
        assert result["message"] == "Embalagem deletada com sucesso!"

    @patch.object(EmbalagemService, 'deletar_embalagem')
    def test_deletar_embalagem_database_error(self, mock_deletar):
        """Testa erro de banco de dados na deleção"""
        mock_deletar.side_effect = Exception("Erro ao conectar ao banco de dados")
        
        with pytest.raises(Exception) as exc_info:
            EmbalagemService.deletar_embalagem(1)
        
        assert "Erro ao conectar ao banco de dados" in str(exc_info.value)

    @patch('app.api.embalagem.embalagem_service.DatabaseConnection')
    def test_criar_embalagem_with_database_mock(self, mock_db_class):
        """Testa criação com mock completo do banco de dados"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchone.return_value = [1]
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = EmbalagemService.criar_embalagem(self.test_embalagem_data)
        
        assert result["embalagem_id"] == 1
        assert result["caixa"] == self.test_embalagem_data['caixa']
        assert result["palet"] == self.test_embalagem_data['palet']
        assert result["grade"] == self.test_embalagem_data['grade']
        assert result["cubagem_id"] == self.test_embalagem_data['cubagem_id']
        assert result["message"] == "Embalagem criada com sucesso!"
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.embalagem.embalagem_service.DatabaseConnection')
    def test_criar_embalagem_cursor_none(self, mock_db_class):
        """Testa criação quando cursor é None"""
        mock_db = MagicMock()
        mock_db.get_cursor.return_value = None
        mock_db_class.return_value = mock_db
        
        with pytest.raises(Exception) as exc_info:
            EmbalagemService.criar_embalagem(self.test_embalagem_data)
        
        assert "Erro ao conectar ao banco de dados" in str(exc_info.value)

    @patch('app.api.embalagem.embalagem_service.DatabaseConnection')
    def test_listar_embalagens_with_database_mock(self, mock_db_class):
        """Testa listagem com mock completo do banco de dados"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchall.return_value = [
            (1, 10, 5, 3, 1, "2023-01-01T10:00:00"),
            (2, 20, 8, 6, 2, "2023-01-02T11:00:00")
        ]
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = EmbalagemService.listar_embalagens()
        
        assert len(result) == 2
        assert result[0]["embalagem_id"] == 1
        assert result[0]["caixa"] == 10
        assert result[1]["embalagem_id"] == 2
        assert result[1]["caixa"] == 20
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM embalagem;")
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.embalagem.embalagem_service.DatabaseConnection')
    def test_obter_embalagem_with_database_mock(self, mock_db_class):
        """Testa obtenção com mock completo do banco de dados"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        mock_cursor.fetchone.return_value = (1, 10, 5, 3, 1, "2023-01-01T10:00:00")
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = EmbalagemService.obter_embalagem(1)
        
        assert result["embalagem_id"] == 1
        assert result["caixa"] == 10
        assert result["palet"] == 5
        assert result["grade"] == 3
        assert result["cubagem_id"] == 1
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM embalagem WHERE embalagem_id = %s;", (1,)
        )
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.embalagem.embalagem_service.DatabaseConnection')
    def test_atualizar_embalagem_with_database_mock(self, mock_db_class):
        """Testa atualização com mock completo do banco de dados"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        update_data = {'caixa': 15, 'palet': 7, 'grade': 4}
        
        result = EmbalagemService.atualizar_embalagem(1, update_data)
        
        assert result["embalagem_id"] == 1
        assert result["caixa"] == 15
        assert result["palet"] == 7
        assert result["grade"] == 4
        assert result["message"] == "Embalagem atualizada com sucesso!"
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.embalagem.embalagem_service.DatabaseConnection')
    def test_deletar_embalagem_with_database_mock(self, mock_db_class):
        """Testa deleção com mock completo do banco de dados"""
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        result = EmbalagemService.deletar_embalagem(1)
        
        assert result["embalagem_id"] == 1
        assert result["message"] == "Embalagem deletada com sucesso!"
        
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM embalagem WHERE embalagem_id = %s;", (1,)
        )
        mock_db.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    def test_embalagem_service_methods_exist(self):
        """Testa se todos os métodos existem na classe EmbalagemService"""
        assert hasattr(EmbalagemService, 'criar_embalagem')
        assert hasattr(EmbalagemService, 'listar_embalagens')
        assert hasattr(EmbalagemService, 'obter_embalagem')
        assert hasattr(EmbalagemService, 'atualizar_embalagem')
        assert hasattr(EmbalagemService, 'deletar_embalagem')
        
        assert callable(getattr(EmbalagemService, 'criar_embalagem'))
        assert callable(getattr(EmbalagemService, 'listar_embalagens'))
        assert callable(getattr(EmbalagemService, 'obter_embalagem'))
        assert callable(getattr(EmbalagemService, 'atualizar_embalagem'))
        assert callable(getattr(EmbalagemService, 'deletar_embalagem'))
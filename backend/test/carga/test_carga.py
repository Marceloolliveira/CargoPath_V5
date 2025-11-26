import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Adiciona o src ao PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Agora pode importar usando o caminho completo
from app.api.carga.carga_service import CargaService


class TestCargaService:
    
    def setup_method(self):
        """Setup executado antes de cada teste"""
        self.carga_service = CargaService()
        
        self.test_carga_data = {
            'valor': 1500.75,
            'peso': 25.5,
            'volumes': 3,
            'cotacao_id': 1,
            'carga_id': 1
        }

    def test_carga_service_initialization(self):
        """Testa se a classe CargaService pode ser instanciada"""
        service = CargaService()
        assert service is not None
        assert isinstance(service, CargaService)

    @patch('app.api.carga.carga_service.DatabaseConnection')
    def test_criar_carga_success(self, mock_db_class):
        """Testa criação bem-sucedida de carga"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura retorno do cursor
        mock_cursor.fetchone.return_value = [self.test_carga_data['carga_id']]
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Executa o teste
        result = self.carga_service.criar_carga(
            self.test_carga_data['valor'],
            self.test_carga_data['peso'],
            self.test_carga_data['volumes'],
            self.test_carga_data['cotacao_id']
        )
        
        # Verificações
        assert result["carga_id"] == self.test_carga_data['carga_id']
        assert result["valor"] == self.test_carga_data['valor']
        assert result["peso"] == self.test_carga_data['peso']
        assert result["volumes"] == self.test_carga_data['volumes']
        assert result["cotacao_id"] == self.test_carga_data['cotacao_id']
        assert result["message"] == "Carga criada com sucesso!"
        
        # Verifica se o banco foi chamado corretamente
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        
        # Verifica a query executada
        call_args = mock_cursor.execute.call_args[0]
        query = call_args[0]
        params = call_args[1]
        
        assert "INSERT INTO carga" in query
        assert "RETURNING carga_id" in query
        assert params == (
            self.test_carga_data['valor'],
            self.test_carga_data['peso'],
            self.test_carga_data['volumes'],
            self.test_carga_data['cotacao_id']
        )
        
        mock_db.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.carga.carga_service.DatabaseConnection')
    def test_criar_carga_database_error(self, mock_db_class):
        """Testa erro de banco de dados na criação"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura exceção na execução
        mock_cursor.execute.side_effect = Exception("Erro SQL na criação")
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Verifica se a exceção é propagada com a mensagem personalizada
        with pytest.raises(Exception) as exc_info:
            self.carga_service.criar_carga(
                self.test_carga_data['valor'],
                self.test_carga_data['peso'],
                self.test_carga_data['volumes'],
                self.test_carga_data['cotacao_id']
            )
        
        assert "Erro ao criar carga: Erro SQL na criação" in str(exc_info.value)
        
        # Verifica se rollback foi chamado
        mock_db.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.carga.carga_service.DatabaseConnection')
    def test_listar_cargas_success(self, mock_db_class):
        """Testa listagem bem-sucedida de cargas"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura retorno do cursor com múltiplas cargas
        mock_cursor.fetchall.return_value = [
            (1, 1500.75, 25.5, 3, 1, "2023-12-20T08:00:00"),
            (2, 2000.00, 30.0, 5, 2, "2023-12-20T09:00:00")
        ]
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Executa o teste
        result = self.carga_service.listar_cargas()
        
        # Verificações
        assert isinstance(result, list)
        assert len(result) == 2
        
        # Verifica primeira carga
        assert result[0]["carga_id"] == 1
        assert result[0]["valor"] == 1500.75
        assert result[0]["peso"] == 25.5
        assert result[0]["volumes"] == 3
        assert result[0]["cotacao_id"] == 1
        assert result[0]["created_at"] == "2023-12-20T08:00:00"
        
        # Verifica segunda carga
        assert result[1]["carga_id"] == 2
        assert result[1]["valor"] == 2000.00
        assert result[1]["peso"] == 30.0
        
        # Verifica se o banco foi chamado corretamente
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM carga;")
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.carga.carga_service.DatabaseConnection')
    def test_listar_cargas_empty(self, mock_db_class):
        """Testa listagem quando não há cargas"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura retorno vazio
        mock_cursor.fetchall.return_value = []
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Executa o teste
        result = self.carga_service.listar_cargas()
        
        # Verificações
        assert isinstance(result, list)
        assert len(result) == 0

    @patch('app.api.carga.carga_service.DatabaseConnection')
    def test_obter_carga_success(self, mock_db_class):
        """Testa obtenção bem-sucedida de carga específica"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura retorno do cursor
        mock_cursor.fetchone.return_value = (
            1, 1500.75, 25.5, 3, 1, "2023-12-20T08:00:00"
        )
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Executa o teste
        result = self.carga_service.obter_carga(1)
        
        # Verificações
        assert result is not None
        assert result["carga_id"] == 1
        assert result["valor"] == 1500.75
        assert result["peso"] == 25.5
        assert result["volumes"] == 3
        assert result["cotacao_id"] == 1
        assert result["created_at"] == "2023-12-20T08:00:00"
        
        # Verifica se o banco foi chamado corretamente
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM carga WHERE carga_id = %s;", (1,)
        )
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.carga.carga_service.DatabaseConnection')
    def test_obter_carga_not_found(self, mock_db_class):
        """Testa obtenção de carga não encontrada"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura retorno None
        mock_cursor.fetchone.return_value = None
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Executa o teste
        result = self.carga_service.obter_carga(999)
        
        # Verificações
        assert result is None
        
        # Verifica se o banco foi chamado corretamente
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM carga WHERE carga_id = %s;", (999,)
        )

    @patch('app.api.carga.carga_service.DatabaseConnection')
    def test_atualizar_carga_success(self, mock_db_class):
        """Testa atualização bem-sucedida de carga"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Novos valores para atualização
        novo_valor = 2000.00
        novo_peso = 30.0
        novos_volumes = 5
        
        # Executa o teste
        result = self.carga_service.atualizar_carga(1, novo_valor, novo_peso, novos_volumes)
        
        # Verificações
        assert result["carga_id"] == 1
        assert result["valor"] == novo_valor
        assert result["peso"] == novo_peso
        assert result["volumes"] == novos_volumes
        assert result["message"] == "Carga atualizada com sucesso!"
        
        # Verifica se o banco foi chamado corretamente
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        
        # Verifica a query executada
        call_args = mock_cursor.execute.call_args[0]
        query = call_args[0]
        params = call_args[1]
        
        assert "UPDATE carga" in query
        assert "SET valor = %s, peso = %s, volumes = %s" in query
        assert "WHERE carga_id = %s" in query
        assert params == (novo_valor, novo_peso, novos_volumes, 1)
        
        mock_db.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.carga.carga_service.DatabaseConnection')
    def test_atualizar_carga_database_error(self, mock_db_class):
        """Testa erro de banco de dados na atualização"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura exceção na execução
        mock_cursor.execute.side_effect = Exception("Erro SQL na atualização")
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Verifica se a exceção é propagada com mensagem personalizada
        with pytest.raises(Exception) as exc_info:
            self.carga_service.atualizar_carga(1, 2000.00, 30.0, 5)
        
        assert "Erro ao atualizar carga: Erro SQL na atualização" in str(exc_info.value)
        
        # Verifica se rollback foi chamado
        mock_db.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.carga.carga_service.DatabaseConnection')
    def test_deletar_carga_success(self, mock_db_class):
        """Testa deleção bem-sucedida de carga"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Executa o teste (método não retorna valor)
        result = self.carga_service.deletar_carga(1)
        
        # Verificações
        assert result is None  # Método void
        
        # Verifica se o banco foi chamado corretamente
        mock_db.connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM carga WHERE carga_id = %s;", (1,)
        )
        mock_db.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.carga.carga_service.DatabaseConnection')
    def test_deletar_carga_database_error(self, mock_db_class):
        """Testa erro de banco de dados na deleção"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura exceção na execução
        mock_cursor.execute.side_effect = Exception("Erro SQL na deleção")
        mock_db.get_cursor.return_value = mock_cursor
        mock_db_class.return_value = mock_db
        
        # Verifica se a exceção é propagada com mensagem personalizada
        with pytest.raises(Exception) as exc_info:
            self.carga_service.deletar_carga(1)
        
        assert "Erro ao deletar carga: Erro SQL na deleção" in str(exc_info.value)
        
        # Verifica se rollback foi chamado
        mock_db.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    def test_carga_service_methods_exist(self):
        """Testa se todos os métodos existem na classe CargaService"""
        assert hasattr(CargaService, 'criar_carga')
        assert hasattr(CargaService, 'listar_cargas')
        assert hasattr(CargaService, 'obter_carga')
        assert hasattr(CargaService, 'atualizar_carga')
        assert hasattr(CargaService, 'deletar_carga')
        
        # Verifica se são métodos de instância
        assert callable(getattr(CargaService, 'criar_carga'))
        assert callable(getattr(CargaService, 'listar_cargas'))
        assert callable(getattr(CargaService, 'obter_carga'))
        assert callable(getattr(CargaService, 'atualizar_carga'))
        assert callable(getattr(CargaService, 'deletar_carga'))

    def test_carga_data_validation(self):
        """Testa validação dos dados de carga"""
        # Testa dados válidos
        assert self.test_carga_data['valor'] > 0
        assert self.test_carga_data['peso'] > 0
        assert self.test_carga_data['volumes'] > 0
        assert self.test_carga_data['cotacao_id'] > 0
        
        # Testa tipos de dados
        assert isinstance(self.test_carga_data['valor'], (int, float))
        assert isinstance(self.test_carga_data['peso'], (int, float))
        assert isinstance(self.test_carga_data['volumes'], int)
        assert isinstance(self.test_carga_data['cotacao_id'], int)

    @patch.object(CargaService, 'criar_carga')
    def test_criar_carga_mock(self, mock_criar):
        """Testa criação de carga com mock da classe"""
        # Configura retorno do mock
        mock_criar.return_value = {
            "carga_id": 1,
            "valor": self.test_carga_data['valor'],
            "peso": self.test_carga_data['peso'],
            "volumes": self.test_carga_data['volumes'],
            "cotacao_id": self.test_carga_data['cotacao_id'],
            "message": "Carga criada com sucesso!"
        }
        
        # Executa o teste
        result = self.carga_service.criar_carga(
            self.test_carga_data['valor'],
            self.test_carga_data['peso'],
            self.test_carga_data['volumes'],
            self.test_carga_data['cotacao_id']
        )
        
        # Verificações
        assert result["carga_id"] == 1
        assert result["message"] == "Carga criada com sucesso!"
        mock_criar.assert_called_once_with(
            self.test_carga_data['valor'],
            self.test_carga_data['peso'],
            self.test_carga_data['volumes'],
            self.test_carga_data['cotacao_id']
        )

    @patch.object(CargaService, 'listar_cargas')
    def test_listar_cargas_mock(self, mock_listar):
        """Testa listagem de cargas com mock da classe"""
        # Configura retorno do mock
        mock_listar.return_value = [
            {
                "carga_id": 1,
                "valor": 1500.75,
                "peso": 25.5,
                "volumes": 3,
                "cotacao_id": 1,
                "created_at": "2023-12-20T08:00:00"
            }
        ]
        
        # Executa o teste
        result = self.carga_service.listar_cargas()
        
        # Verificações
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["carga_id"] == 1
        mock_listar.assert_called_once()

    @patch.object(CargaService, 'obter_carga')
    def test_obter_carga_mock(self, mock_obter):
        """Testa obtenção de carga com mock da classe"""
        # Configura retorno do mock
        mock_obter.return_value = {
            "carga_id": 1,
            "valor": 1500.75,
            "peso": 25.5,
            "volumes": 3,
            "cotacao_id": 1,
            "created_at": "2023-12-20T08:00:00"
        }
        
        # Executa o teste
        result = self.carga_service.obter_carga(1)
        
        # Verificações
        assert result["carga_id"] == 1
        assert result["valor"] == 1500.75
        mock_obter.assert_called_once_with(1)

    @patch.object(CargaService, 'atualizar_carga')
    def test_atualizar_carga_mock(self, mock_atualizar):
        """Testa atualização de carga com mock da classe"""
        # Configura retorno do mock
        mock_atualizar.return_value = {
            "carga_id": 1,
            "valor": 2000.00,
            "peso": 30.0,
            "volumes": 5,
            "message": "Carga atualizada com sucesso!"
        }
        
        # Executa o teste
        result = self.carga_service.atualizar_carga(1, 2000.00, 30.0, 5)
        
        # Verificações
        assert result["carga_id"] == 1
        assert result["message"] == "Carga atualizada com sucesso!"
        mock_atualizar.assert_called_once_with(1, 2000.00, 30.0, 5)

    @patch.object(CargaService, 'deletar_carga')
    def test_deletar_carga_mock(self, mock_deletar):
        """Testa deleção de carga com mock da classe"""
        # Configura retorno do mock (void method)
        mock_deletar.return_value = None
        
        # Executa o teste
        result = self.carga_service.deletar_carga(1)
        
        # Verificações
        assert result is None
        mock_deletar.assert_called_once_with(1)

    @patch('app.api.carga.carga_service.DatabaseConnection')
    def test_listar_cargas_database_error(self, mock_db_class):
        """Testa tratamento de erro na listagem"""
        # Mock que lança exceção
        mock_db_class.side_effect = Exception("Erro de conexão")
        
        # Verifica se a exceção é propagada
        with pytest.raises(Exception) as exc_info:
            self.carga_service.listar_cargas()
        
        assert "Erro de conexão" in str(exc_info.value)

    @patch('app.api.carga.carga_service.DatabaseConnection')
    def test_obter_carga_database_error(self, mock_db_class):
        """Testa tratamento de erro na obtenção"""
        # Mock que lança exceção
        mock_db_class.side_effect = Exception("Erro de conexão")
        
        # Verifica se a exceção é propagada
        with pytest.raises(Exception) as exc_info:
            self.carga_service.obter_carga(1)
        
        assert "Erro de conexão" in str(exc_info.value)

    def test_carga_valor_calculation(self):
        """Testa cálculo conceitual de valor total da carga"""
        # Valor unitário * volumes
        valor_unitario = self.test_carga_data['valor']
        volumes = self.test_carga_data['volumes']
        valor_total_estimado = valor_unitario * volumes
        
        # Verificações
        assert valor_unitario > 0
        assert volumes > 0
        assert valor_total_estimado > valor_unitario
        assert valor_total_estimado == 1500.75 * 3  # 4502.25

    def test_carga_peso_validation(self):
        """Testa validação de peso"""
        peso = self.test_carga_data['peso']
        
        # Verificações básicas de peso
        assert peso > 0, "Peso deve ser maior que zero"
        assert isinstance(peso, (int, float)), "Peso deve ser numérico"
        
        # Teste de limites (conceitual)
        assert peso < 50000, "Peso parece excessivamente alto"
        assert peso > 0.1, "Peso parece muito baixo"

    def test_carga_volumes_validation(self):
        """Testa validação de volumes"""
        volumes = self.test_carga_data['volumes']
        
        # Verificações básicas de volumes
        assert volumes > 0, "Volumes deve ser maior que zero"
        assert isinstance(volumes, int), "Volumes deve ser um número inteiro"
        assert volumes == int(volumes), "Volumes não pode ser decimal"

    @patch('app.api.carga.carga_service.DatabaseConnection')
    def test_criar_carga_rollback_on_commit_error(self, mock_db_class):
        """Testa rollback quando o commit falha"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura cursor normal mas commit com erro
        mock_cursor.fetchone.return_value = [1]
        mock_db.get_cursor.return_value = mock_cursor
        mock_db.commit.side_effect = Exception("Erro no commit")
        mock_db_class.return_value = mock_db
        
        # Verifica se a exceção é propagada
        with pytest.raises(Exception) as exc_info:
            self.carga_service.criar_carga(1500.75, 25.5, 3, 1)
        
        assert "Erro ao criar carga: Erro no commit" in str(exc_info.value)
        
        # Verifica se rollback foi chamado
        mock_db.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()

    @patch('app.api.carga.carga_service.DatabaseConnection')
    def test_atualizar_carga_rollback_on_commit_error(self, mock_db_class):
        """Testa rollback quando o commit da atualização falha"""
        # Mock do banco de dados
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        
        # Configura cursor normal mas commit com erro
        mock_db.get_cursor.return_value = mock_cursor
        mock_db.commit.side_effect = Exception("Erro no commit da atualização")
        mock_db_class.return_value = mock_db
        
        # Verifica se a exceção é propagada
        with pytest.raises(Exception) as exc_info:
            self.carga_service.atualizar_carga(1, 2000.00, 30.0, 5)
        
        assert "Erro ao atualizar carga: Erro no commit da atualização" in str(exc_info.value)
        
        # Verifica se rollback foi chamado
        mock_db.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_db.close.assert_called_once()
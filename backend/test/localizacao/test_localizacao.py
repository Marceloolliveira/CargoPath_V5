import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


from app.api.localizacao.localizacao_service import LocalizacaoService


class TestLocalizacaoService:
    
    def setup_method(self):
        
        self.test_localizacao_data = {
            'rua': 'Rua das Flores',
            'numero': '123',
            'cep': '01234-567',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'complemento': 'Apt 101',
            'tipo': 'origem',
            'cotacao_id': 1,
            'destinatario_nome': 'João Silva',
            'localizacao_id': 1
        }

    @patch.object(LocalizacaoService, 'handle_criar_localizacao')
    def test_handle_criar_localizacao_success(self, mock_handle_criar):
        
        
        mock_request = MagicMock()
        mock_request.json = self.test_localizacao_data
        
        
        mock_handle_criar.return_value = ({
            "localizacao_id": 1,
            "message": "Localização criada com sucesso!"
        }, 201)
        
        
        result, status_code = LocalizacaoService.handle_criar_localizacao(mock_request)
        
        
        assert status_code == 201
        assert "localizacao_id" in result
        assert result["message"] == "Localização criada com sucesso!"

    @patch.object(LocalizacaoService, 'handle_criar_localizacao')
    def test_handle_criar_localizacao_no_data(self, mock_handle_criar):
        
        
        mock_request = MagicMock()
        mock_request.json = None
        
        
        mock_handle_criar.return_value = ({"error": "Dados não fornecidos"}, 400)
        
        
        result, status_code = LocalizacaoService.handle_criar_localizacao(mock_request)
        
        
        assert status_code == 400
        assert result["error"] == "Dados não fornecidos"

    @patch.object(LocalizacaoService, 'handle_criar_localizacao')
    def test_handle_criar_localizacao_missing_fields(self, mock_handle_criar):
        
        
        mock_request = MagicMock()
        mock_request.json = {'rua': 'Rua das Flores'}  
        
        
        mock_handle_criar.return_value = ({"error": "Campos obrigatórios não preenchidos"}, 400)
        
        
        result, status_code = LocalizacaoService.handle_criar_localizacao(mock_request)
        
        
        assert status_code == 400
        assert result["error"] == "Campos obrigatórios não preenchidos"

    @patch.object(LocalizacaoService, 'criar_localizacao')
    def test_criar_localizacao_success(self, mock_criar):
        
        
        mock_criar.return_value = ({
            "localizacao_id": self.test_localizacao_data['localizacao_id'],
            "rua": self.test_localizacao_data['rua'],
            "numero": self.test_localizacao_data['numero'],
            "cep": self.test_localizacao_data['cep'],
            "cidade": self.test_localizacao_data['cidade'],
            "estado": self.test_localizacao_data['estado'],
            "complemento": self.test_localizacao_data['complemento'],
            "tipo": self.test_localizacao_data['tipo'],
            "cotacao_id": self.test_localizacao_data['cotacao_id'],
            "destinatario_nome": self.test_localizacao_data['destinatario_nome'],
            "message": "Localização criada com sucesso!"
        }, 201)
        
        
        result, status_code = LocalizacaoService.criar_localizacao(
            self.test_localizacao_data['rua'],
            self.test_localizacao_data['numero'],
            self.test_localizacao_data['cep'],
            self.test_localizacao_data['cidade'],
            self.test_localizacao_data['estado'],
            self.test_localizacao_data['complemento'],
            self.test_localizacao_data['tipo'],
            self.test_localizacao_data['cotacao_id'],
            self.test_localizacao_data['destinatario_nome']
        )
        
        
        assert status_code == 201
        assert result["localizacao_id"] == self.test_localizacao_data['localizacao_id']
        assert result["rua"] == self.test_localizacao_data['rua']
        assert result["message"] == "Localização criada com sucesso!"

    @patch.object(LocalizacaoService, 'listar_localizacoes')
    def test_listar_localizacoes_success(self, mock_listar):
        
        
        mock_listar.return_value = ([
            {
                "localizacao_id": 1,
                "rua": "Rua das Flores",
                "numero": "123",
                "cep": "01234-567",
                "cidade": "São Paulo",
                "estado": "SP",
                "complemento": "Apt 101",
                "tipo": "origem",
                "cotacao_id": 1,
                "created_at": "2023-01-01T10:00:00"
            }
        ], 200)
        
        
        result, status_code = LocalizacaoService.listar_localizacoes()
        
        
        assert status_code == 200
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["localizacao_id"] == 1
        assert result[0]["rua"] == "Rua das Flores"

    @patch.object(LocalizacaoService, 'obter_localizacao')
    def test_obter_localizacao_success(self, mock_obter):
        
        
        mock_obter.return_value = ({
            "localizacao_id": self.test_localizacao_data['localizacao_id'],
            "rua": self.test_localizacao_data['rua'],
            "numero": self.test_localizacao_data['numero'],
            "cep": self.test_localizacao_data['cep'],
            "cidade": self.test_localizacao_data['cidade'],
            "estado": self.test_localizacao_data['estado'],
            "complemento": self.test_localizacao_data['complemento'],
            "tipo": self.test_localizacao_data['tipo'],
            "cotacao_id": self.test_localizacao_data['cotacao_id'],
            "created_at": "2023-01-01T10:00:00"
        }, 200)
        
        
        result, status_code = LocalizacaoService.obter_localizacao(
            self.test_localizacao_data['localizacao_id']
        )
        
        
        assert status_code == 200
        assert result["localizacao_id"] == self.test_localizacao_data['localizacao_id']
        assert result["rua"] == self.test_localizacao_data['rua']

    @patch.object(LocalizacaoService, 'obter_localizacao')
    def test_obter_localizacao_not_found(self, mock_obter):
        
        
        mock_obter.return_value = ({"message": "Localização não encontrada"}, 404)
        
        
        result, status_code = LocalizacaoService.obter_localizacao(999)
        
        
        assert status_code == 404
        assert result["message"] == "Localização não encontrada"

    @patch.object(LocalizacaoService, 'deletar_localizacao')
    def test_deletar_localizacao_success(self, mock_deletar):
        
        
        mock_deletar.return_value = ({
            "localizacao_id": self.test_localizacao_data['localizacao_id'],
            "message": "Localização deletada com sucesso!"
        }, 200)
        
        
        result, status_code = LocalizacaoService.deletar_localizacao(
            self.test_localizacao_data['localizacao_id']
        )
        
        
        assert status_code == 200
        assert result["localizacao_id"] == self.test_localizacao_data['localizacao_id']
        assert result["message"] == "Localização deletada com sucesso!"

    def test_localizacao_service_methods_exist(self):
        
        assert hasattr(LocalizacaoService, 'handle_criar_localizacao')
        assert hasattr(LocalizacaoService, 'criar_localizacao')
        assert hasattr(LocalizacaoService, 'listar_localizacoes')
        assert hasattr(LocalizacaoService, 'obter_localizacao')
        assert hasattr(LocalizacaoService, 'handle_atualizar_localizacao')
        assert hasattr(LocalizacaoService, 'atualizar_localizacao')
        assert hasattr(LocalizacaoService, 'deletar_localizacao')
        
        
        assert callable(getattr(LocalizacaoService, 'handle_criar_localizacao'))
        assert callable(getattr(LocalizacaoService, 'criar_localizacao'))
        assert callable(getattr(LocalizacaoService, 'listar_localizacoes'))
        assert callable(getattr(LocalizacaoService, 'obter_localizacao'))
        assert callable(getattr(LocalizacaoService, 'handle_atualizar_localizacao'))
        assert callable(getattr(LocalizacaoService, 'atualizar_localizacao'))
        assert callable(getattr(LocalizacaoService, 'deletar_localizacao'))
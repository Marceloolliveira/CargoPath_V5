import pytest
import os
from unittest.mock import Mock, patch, MagicMock
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from app.api.mercadopago.mercadopago_service import PaymentService


class TestPaymentService:
    
    def setup_method(self):
        """Setup executado antes de cada teste"""
        with patch.dict(os.environ, {'SDK_TESTE': 'TEST_TOKEN_123'}):
            self.payment_service = PaymentService()
        
        self.test_data = {
            'cotacao_id': 12345,
            'valor': 250.75
        }
        
        self.expected_preference_data = {
            "items": [
                {
                    "title": "Cotação 12345",
                    "quantity": 1,
                    "unit_price": 250.75,
                }
            ],
            "payment_methods": {
                "excluded_payment_types": [],
                "excluded_payment_methods": [],
                "installments": 12,
                "default_payment_method_id": None
            },
            "back_urls": {
                "success": "http://127.0.0.1:5501/src/app/pages/dashboard/dashboard.html",
                "failure": "http://127.0.0.1:5501/src/app/pages/price/pagamento/pagamento.html",
                "pending": "http://127.0.0.1:5501/src/app/pages/price/pagamento/pagamento.html"
            },
            "auto_return": "approved",
        }

    @patch('app.api.mercadopago.mercadopago_service.mercadopago.SDK')
    def test_payment_service_initialization(self, mock_sdk_class):
        """Testa se o PaymentService é inicializado corretamente"""
        mock_sdk = MagicMock()
        mock_sdk_class.return_value = mock_sdk
        
        with patch.dict(os.environ, {'SDK_TESTE': 'TEST_TOKEN_123'}):
            service = PaymentService()
        
        mock_sdk_class.assert_called_once_with('TEST_TOKEN_123')
        assert service.sdk == mock_sdk

    @patch.object(PaymentService, '__init__', lambda x: None)
    def test_create_preference_success(self):
        """Testa criação bem-sucedida de preferência de pagamento"""
        mock_sdk = MagicMock()
        mock_preference = MagicMock()
        mock_sdk.preference.return_value = mock_preference
        
        mock_preference.create.return_value = {
            "response": {
                "id": "preference_id_123",
                "init_point": "https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=preference_id_123"
            }
        }
        
        self.payment_service.sdk = mock_sdk
        
        result = self.payment_service.create_preference(
            self.test_data['cotacao_id'],
            self.test_data['valor']
        )
        
        assert result == "preference_id_123"
        
        mock_preference.create.assert_called_once_with(self.expected_preference_data)

    @patch.object(PaymentService, '__init__', lambda x: None)
    def test_create_preference_no_response(self):
        """Testa erro quando não há resposta do Mercado Pago"""
        mock_sdk = MagicMock()
        mock_preference = MagicMock()
        mock_sdk.preference.return_value = mock_preference
        
        mock_preference.create.return_value = {
            "response": None
        }
        
        self.payment_service.sdk = mock_sdk
        
        with pytest.raises(Exception) as exc_info:
            self.payment_service.create_preference(
                self.test_data['cotacao_id'],
                self.test_data['valor']
            )
        
        assert "Erro ao criar preferência no Mercado Pago." in str(exc_info.value)

    @patch.object(PaymentService, '__init__', lambda x: None)
    def test_create_preference_no_id(self):
        """Testa erro quando resposta não contém ID"""
        mock_sdk = MagicMock()
        mock_preference = MagicMock()
        mock_sdk.preference.return_value = mock_preference
        
        mock_preference.create.return_value = {
            "response": {
                "status": "created",
            }
        }
        
        self.payment_service.sdk = mock_sdk
        
        with pytest.raises(Exception) as exc_info:
            self.payment_service.create_preference(
                self.test_data['cotacao_id'],
                self.test_data['valor']
            )
        
        assert "Erro ao criar preferência no Mercado Pago." in str(exc_info.value)

    @patch.object(PaymentService, '__init__', lambda x: None)
    def test_create_preference_api_error(self):
        """Testa erro na API do Mercado Pago"""
        mock_sdk = MagicMock()
        mock_preference = MagicMock()
        mock_sdk.preference.return_value = mock_preference
        
        mock_preference.create.side_effect = Exception("Erro na API do Mercado Pago")
        
        self.payment_service.sdk = mock_sdk
        
        with pytest.raises(Exception) as exc_info:
            self.payment_service.create_preference(
                self.test_data['cotacao_id'],
                self.test_data['valor']
            )
        
        assert "Erro na API do Mercado Pago" in str(exc_info.value)

    @patch.object(PaymentService, '__init__', lambda x: None)
    def test_create_preference_with_different_values(self):
        """Testa criação de preferência com diferentes valores"""
        mock_sdk = MagicMock()
        mock_preference = MagicMock()
        mock_sdk.preference.return_value = mock_preference
        
        mock_preference.create.return_value = {
            "response": {
                "id": "preference_id_456",
            }
        }
        
        self.payment_service.sdk = mock_sdk
        
        cotacao_id = 98765
        valor = 1000.50
        
        result = self.payment_service.create_preference(cotacao_id, valor)
        
        assert result == "preference_id_456"
        
        call_args = mock_preference.create.call_args[0][0]
        assert call_args["items"][0]["title"] == "Cotação 98765"
        assert call_args["items"][0]["unit_price"] == 1000.50
        assert call_args["items"][0]["quantity"] == 1

    @patch.object(PaymentService, '__init__', lambda x: None)
    def test_create_preference_urls_configuration(self):
        """Testa se as URLs estão configuradas corretamente"""
        mock_sdk = MagicMock()
        mock_preference = MagicMock()
        mock_sdk.preference.return_value = mock_preference
        
        mock_preference.create.return_value = {
            "response": {
                "id": "preference_id_789",
            }
        }
        
        self.payment_service.sdk = mock_sdk
        
        self.payment_service.create_preference(
            self.test_data['cotacao_id'],
            self.test_data['valor']
        )
        
        call_args = mock_preference.create.call_args[0][0]
        back_urls = call_args["back_urls"]
        
        assert back_urls["success"] == "http://127.0.0.1:5501/src/app/pages/dashboard/dashboard.html"
        assert back_urls["failure"] == "http://127.0.0.1:5501/src/app/pages/price/pagamento/pagamento.html"
        assert back_urls["pending"] == "http://127.0.0.1:5501/src/app/pages/price/pagamento/pagamento.html"
        assert call_args["auto_return"] == "approved"

    @patch.object(PaymentService, '__init__', lambda x: None)
    def test_create_preference_payment_methods_configuration(self):
        """Testa se os métodos de pagamento estão configurados corretamente"""
        mock_sdk = MagicMock()
        mock_preference = MagicMock()
        mock_sdk.preference.return_value = mock_preference
        
        mock_preference.create.return_value = {
            "response": {
                "id": "preference_id_abc",
            }
        }
        
        self.payment_service.sdk = mock_sdk
        
        self.payment_service.create_preference(
            self.test_data['cotacao_id'],
            self.test_data['valor']
        )
        
        call_args = mock_preference.create.call_args[0][0]
        payment_methods = call_args["payment_methods"]
        
        assert payment_methods["excluded_payment_types"] == []
        assert payment_methods["excluded_payment_methods"] == []
        assert payment_methods["installments"] == 12
        assert payment_methods["default_payment_method_id"] is None

    def test_payment_service_exists(self):
        """Testa se a instância do PaymentService foi criada corretamente"""
        assert self.payment_service is not None
        assert isinstance(self.payment_service, PaymentService)
        assert hasattr(self.payment_service, 'create_preference')
        assert hasattr(self.payment_service, 'sdk')

    @patch('app.api.mercadopago.mercadopago_service.os.getenv')
    def test_environment_variable_loading(self, mock_getenv):
        """Testa se as variáveis de ambiente são carregadas corretamente"""
        mock_getenv.return_value = 'MOCKED_SDK_TOKEN'
        
        with patch('app.api.mercadopago.mercadopago_service.mercadopago.SDK') as mock_sdk_class:
            PaymentService()
            mock_sdk_class.assert_called_once_with('MOCKED_SDK_TOKEN')
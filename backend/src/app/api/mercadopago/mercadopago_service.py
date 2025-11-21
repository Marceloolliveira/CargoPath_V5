import os
from dotenv import load_dotenv
import mercadopago


load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))

class PaymentService:
    def __init__(self):
        self.sdk = mercadopago.SDK(os.getenv("SDK_TESTE"))

    def create_preference(self, cotacao_id, valor):
        descricao = f"Cotação 

        preference_data = {
            "items": [
                {
                    "title": descricao,
                    "quantity": 1,
                    "unit_price": float(valor),
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

        
        preference_response = self.sdk.preference().create(preference_data)
        preference = preference_response.get("response")

        if not preference or "id" not in preference:
            raise Exception("Erro ao criar preferência no Mercado Pago.")

        print(f"Preference criada com sucesso: {preference['id']}")
        return preference["id"]

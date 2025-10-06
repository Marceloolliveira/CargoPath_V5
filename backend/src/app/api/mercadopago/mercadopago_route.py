import os
from flask import Blueprint, jsonify, request
import mercadopago

payment_blueprint = Blueprint('payment', __name__, url_prefix='/api/payment')

# Configurar o SDK do Mercado Pago com a chave de acesso
sdk = mercadopago.SDK(os.getenv("SDK_TESTE"))  # Substitua pela sua chave de acesso

@payment_blueprint.route('/create_preference', methods=['POST'])
def create_preference():
    try:
        data = request.json
        cotacao_id = data.get("cotacaoId")
        valor = data.get("amount")
        descricao = f"Cotação #{cotacao_id}"

        # Configuração explícita de métodos de pagamento
        preference_data = {
            "items": [
                {
                    "title": descricao,
                    "quantity": 1,
                    "unit_price": float(valor),
                }
            ],
            "payment_methods": {
                "excluded_payment_types": [],  # Permitir todos os tipos de pagamento
                "excluded_payment_methods": [],  # Não excluir métodos específicos
                "installments": 12,  # Número máximo de parcelas permitidas
                "default_payment_method_id": None  # Não definir método padrão (opcional)
            },
            "back_urls": {
                "success": "http://127.0.0.1:5501/src/app/pages/dashboard/dashboard.html",
                "failure": "http://127.0.0.1:5501/src/app/pages/price/pagamento/pagamento.html",
                "pending": "http://127.0.0.1:5501/src/app/pages/price/pagamento/pagamento.html"
            },
            "auto_return": "approved",
        }

        # Criar a preferência de pagamento no Mercado Pago
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        print(f"Preference criada com sucesso: {preference['id']}")

        return jsonify({"preferenceId": preference["id"]}), 200

    except Exception as e:
        print(f"Erro ao criar preferência: {e}")
        return jsonify({"error": str(e)}), 500

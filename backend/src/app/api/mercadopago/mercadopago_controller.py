from flask import Blueprint, jsonify, request
from .mercadopago_service import PaymentService

payment_blueprint = Blueprint('payment', __name__, url_prefix='/api/payment')

payment_service = PaymentService()

@payment_blueprint.route('/create_preference', methods=['POST'])
def create_preference():
    try:
        data = request.json
        cotacao_id = data.get("cotacaoId")
        valor = data.get("amount")

        if not cotacao_id or not valor:
            return jsonify({"error": "Campos 'cotacaoId' e 'amount' são obrigatórios."}), 400

        preference_id = payment_service.create_preference(cotacao_id, valor)
        return jsonify({"preferenceId": preference_id}), 200

    except Exception as e:
        print(f"Erro ao criar preferência: {e}")
        return jsonify({"error": str(e)}), 500

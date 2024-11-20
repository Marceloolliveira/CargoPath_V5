import mercadopago

sdk = mercadopago.SDK("YOUR_ACCESS_TOKEN")

request_options = mercadopago.config.RequestOptions()
request_options.custom_headers = {
    'x-idempotency-key': '<SOME_UNIQUE_VALUE>'
}

payment_data = {
    "transaction_amount": 100,
    "token": "CARD_TOKEN",
    "description": "Payment description",
    "payment_method_id": 'visa',
    "installments": 1,
    "payer": {
        "email": 'test_user_123456@testuser.com'
    }
}
result = sdk.payment().create(payment_data, request_options)
payment = result["response"]

print(payment)
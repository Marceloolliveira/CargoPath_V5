from flask import Blueprint, request, jsonify
from services.register_service import RegisterService

register_blueprint = Blueprint("register", __name__)
register_service = RegisterService()

@register_blueprint.route("/api/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        name = data.get("name")
        telefone = data.get("telefone")
        cpf = data.get("cpf")
        email = data.get("email")
        password = data.get("password")

        # Validação simples
        if not all([name, telefone, cpf, email, password]):
            return jsonify({"error": "Todos os campos são obrigatórios"}), 400

        message = register_service.create_user(name, telefone, cpf, email, password)
        return jsonify({"message": message}), 201

    except Exception as e:
        print(f"Erro ao registrar usuário: {e}")
        return jsonify({"error": str(e)}), 500

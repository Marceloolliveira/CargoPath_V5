from flask import Blueprint, request, jsonify
from ...data_base.db_classes.DatabaseConnection import DatabaseConnection
import bcrypt

register_blueprint = Blueprint("register", __name__)

@register_blueprint.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    telefone = data.get("telefone")
    cpf = data.get("cpf")
    email = data.get("email")
    password = data.get("password")

    # Criptografa a senha
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insere o novo usuário no banco de dados
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    try:
        cursor.execute(
            "INSERT INTO users (email, password, name, telefone, cpf) VALUES (%s, %s, %s, %s, %s)",
            (email, hashed_password.decode('utf-8'), name, telefone, cpf)
        )
        db.connection.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso"}), 201
    except Exception as e:
        db.connection.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

from flask import Blueprint, request, jsonify
from ...data_base.db_classes.DatabaseConnection import DatabaseConnection

embalagem_blueprint = Blueprint('embalagem', __name__)

# Endpoint para criar uma nova embalagem
@embalagem_blueprint.route('/api/embalagem', methods=['POST'])
def criar_embalagem():
    data = request.json
    caixa = data.get('caixa')
    palet = data.get('palet')
    grade = data.get('grade')
    cubagem_id = data.get('cubagem_id')

    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("""
            INSERT INTO embalagem (caixa, palet, grade, cubagem_id)
            VALUES (%s, %s, %s, %s)
            RETURNING embalagem_id;
        """, (caixa, palet, grade, cubagem_id))
        
        embalagem_id = cursor.fetchone()[0]
        db.commit()
        
        return jsonify({
            "embalagem_id": embalagem_id,
            "caixa": caixa,
            "palet": palet,
            "grade": grade,
            "cubagem_id": cubagem_id,
            "message": "Embalagem criada com sucesso!"
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Endpoint para listar todas as embalagens
@embalagem_blueprint.route('/api/embalagens', methods=['GET'])
def listar_embalagens():
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("SELECT * FROM embalagem;")
        embalagens = cursor.fetchall()
        
        # Converte os resultados em uma lista de dicionários com rótulos
        embalagens_list = []
        for emb in embalagens:
            embalagens_list.append({
                "embalagem_id": emb[0],
                "caixa": emb[1],
                "palet": emb[2],
                "grade": emb[3],
                "cubagem_id": emb[4],
                "created_at": emb[5]
            })
        
        return jsonify(embalagens_list), 200
    finally:
        cursor.close()
        db.close()

# Endpoint para obter uma embalagem específica
@embalagem_blueprint.route('/api/embalagem/<int:embalagem_id>', methods=['GET'])
def obter_embalagem(embalagem_id):
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("SELECT * FROM embalagem WHERE embalagem_id = %s;", (embalagem_id,))
        emb = cursor.fetchone()
        
        if emb:
            embalagem = {
                "embalagem_id": emb[0],
                "caixa": emb[1],
                "palet": emb[2],
                "grade": emb[3],
                "cubagem_id": emb[4],
                "created_at": emb[5]
            }
            return jsonify(embalagem), 200
        else:
            return jsonify({"message": "Embalagem não encontrada"}), 404
    finally:
        cursor.close()
        db.close()

# Endpoint para atualizar uma embalagem
@embalagem_blueprint.route('/api/embalagem/<int:embalagem_id>', methods=['PUT'])
def atualizar_embalagem(embalagem_id):
    data = request.json
    caixa = data.get('caixa')
    palet = data.get('palet')
    grade = data.get('grade')

    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("""
            UPDATE embalagem SET caixa = %s, palet = %s, grade = %s
            WHERE embalagem_id = %s;
        """, (caixa, palet, grade, embalagem_id))
        
        db.commit()
        return jsonify({
            "embalagem_id": embalagem_id,
            "caixa": caixa,
            "palet": palet,
            "grade": grade,
            "message": "Embalagem atualizada com sucesso!"
        }), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Endpoint para deletar uma embalagem
@embalagem_blueprint.route('/api/embalagem/<int:embalagem_id>', methods=['DELETE'])
def deletar_embalagem(embalagem_id):
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("DELETE FROM embalagem WHERE embalagem_id = %s;", (embalagem_id,))
        db.commit()
        
        return jsonify({"embalagem_id": embalagem_id, "message": "Embalagem deletada com sucesso!"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

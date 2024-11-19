from flask import Blueprint, request, jsonify
from ...data_base.db_classes.DatabaseConnection import DatabaseConnection

carga_blueprint = Blueprint('carga', __name__)

# Endpoint para criar uma nova carga
@carga_blueprint.route('/api/carga', methods=['POST'])
def criar_carga():
    data = request.json
    valor = data.get('valor')
    peso = data.get('peso')
    volumes = data.get('volumes')
    cotacao_id = data.get('cotacao_id')

    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("""
            INSERT INTO carga (valor, peso, volumes, cotacao_id)
            VALUES (%s, %s, %s, %s)
            RETURNING carga_id;
        """, (valor, peso, volumes, cotacao_id))
        
        carga_id = cursor.fetchone()[0]
        db.commit()
        
        return jsonify({
            "carga_id": carga_id,
            "valor": valor,
            "peso": peso,
            "volumes": volumes,
            "cotacao_id": cotacao_id,
            "message": "Carga criada com sucesso!"
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Endpoint para listar todas as cargas
@carga_blueprint.route('/api/cargas', methods=['GET'])
def listar_cargas():
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("SELECT * FROM carga;")
        cargas = cursor.fetchall()
        
        # Adiciona rótulos aos dados retornados
        cargas_list = []
        for carga in cargas:
            cargas_list.append({
                "carga_id": carga[0],
                "valor": carga[1],
                "peso": carga[2],
                "volumes": carga[3],
                "cotacao_id": carga[4],
                "created_at": carga[5]
            })
        
        return jsonify(cargas_list), 200
    finally:
        cursor.close()
        db.close()

# Endpoint para obter uma carga específica
@carga_blueprint.route('/api/carga/<int:carga_id>', methods=['GET'])
def obter_carga(carga_id):
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("SELECT * FROM carga WHERE carga_id = %s;", (carga_id,))
        carga = cursor.fetchone()
        
        if carga:
            carga_detalhe = {
                "carga_id": carga[0],
                "valor": carga[1],
                "peso": carga[2],
                "volumes": carga[3],
                "cotacao_id": carga[4],
                "created_at": carga[5]
            }
            return jsonify(carga_detalhe), 200
        else:
            return jsonify({"message": "Carga não encontrada"}), 404
    finally:
        cursor.close()
        db.close()

# Endpoint para atualizar uma carga
@carga_blueprint.route('/api/carga/<int:carga_id>', methods=['PUT'])
def atualizar_carga(carga_id):
    data = request.json
    valor = data.get('valor')
    peso = data.get('peso')
    volumes = data.get('volumes')

    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("""
            UPDATE carga SET valor = %s, peso = %s, volumes = %s
            WHERE carga_id = %s;
        """, (valor, peso, volumes, carga_id))
        
        db.commit()
        return jsonify({
            "carga_id": carga_id,
            "valor": valor,
            "peso": peso,
            "volumes": volumes,
            "message": "Carga atualizada com sucesso!"
        }), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Endpoint para deletar uma carga
@carga_blueprint.route('/api/carga/<int:carga_id>', methods=['DELETE'])
def deletar_carga(carga_id):
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("DELETE FROM carga WHERE carga_id = %s;", (carga_id,))
        db.commit()
        
        return jsonify({"carga_id": carga_id, "message": "Carga deletada com sucesso!"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

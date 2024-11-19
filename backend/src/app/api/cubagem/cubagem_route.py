from flask import Blueprint, request, jsonify
from ...data_base.db_classes.DatabaseConnection import DatabaseConnection

cubagem_blueprint = Blueprint('cubagem', __name__)

# Endpoint para criar uma nova cubagem
@cubagem_blueprint.route('/api/cubagem', methods=['POST'])
def criar_cubagem():
    data = request.json
    altura = data.get('altura')
    largura = data.get('largura')
    comprimento = data.get('comprimento')
    qtd = data.get('qtd')
    carga_id = data.get('carga_id')

    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("""
            INSERT INTO cubagem (altura, largura, comprimento, qtd, carga_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING cubagem_id;
        """, (altura, largura, comprimento, qtd, carga_id))
        
        cubagem_id = cursor.fetchone()[0]
        db.commit()
        
        return jsonify({
            "cubagem_id": cubagem_id,
            "altura": altura,
            "largura": largura,
            "comprimento": comprimento,
            "qtd": qtd,
            "carga_id": carga_id,
            "message": "Cubagem criada com sucesso!"
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Endpoint para listar todas as cubagens
@cubagem_blueprint.route('/api/cubagens', methods=['GET'])
def listar_cubagens():
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("SELECT * FROM cubagem;")
        cubagens = cursor.fetchall()
        
        # Adiciona rótulos aos dados retornados
        cubagens_list = []
        for cubagem in cubagens:
            cubagens_list.append({
                "cubagem_id": cubagem[0],
                "altura": cubagem[1],
                "largura": cubagem[2],
                "comprimento": cubagem[3],
                "qtd": cubagem[4],
                "carga_id": cubagem[5],
                "created_at": cubagem[6]
            })
        
        return jsonify(cubagens_list), 200
    finally:
        cursor.close()
        db.close()

# Endpoint para obter uma cubagem específica
@cubagem_blueprint.route('/api/cubagem/<int:cubagem_id>', methods=['GET'])
def obter_cubagem(cubagem_id):
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("SELECT * FROM cubagem WHERE cubagem_id = %s;", (cubagem_id,))
        cubagem = cursor.fetchone()
        
        if cubagem:
            cubagem_detalhe = {
                "cubagem_id": cubagem[0],
                "altura": cubagem[1],
                "largura": cubagem[2],
                "comprimento": cubagem[3],
                "qtd": cubagem[4],
                "carga_id": cubagem[5],
                "created_at": cubagem[6]
            }
            return jsonify(cubagem_detalhe), 200
        else:
            return jsonify({"message": "Cubagem não encontrada"}), 404
    finally:
        cursor.close()
        db.close()

# Endpoint para atualizar uma cubagem
@cubagem_blueprint.route('/api/cubagem/<int:cubagem_id>', methods=['PUT'])
def atualizar_cubagem(cubagem_id):
    data = request.json
    altura = data.get('altura')
    largura = data.get('largura')
    comprimento = data.get('comprimento')
    qtd = data.get('qtd')

    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("""
            UPDATE cubagem SET altura = %s, largura = %s, comprimento = %s, qtd = %s
            WHERE cubagem_id = %s;
        """, (altura, largura, comprimento, qtd, cubagem_id))
        
        db.commit()
        return jsonify({
            "cubagem_id": cubagem_id,
            "altura": altura,
            "largura": largura,
            "comprimento": comprimento,
            "qtd": qtd,
            "message": "Cubagem atualizada com sucesso!"
        }), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Endpoint para deletar uma cubagem
@cubagem_blueprint.route('/api/cubagem/<int:cubagem_id>', methods=['DELETE'])
def deletar_cubagem(cubagem_id):
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("DELETE FROM cubagem WHERE cubagem_id = %s;", (cubagem_id,))
        db.commit()
        
        return jsonify({"cubagem_id": cubagem_id, "message": "Cubagem deletada com sucesso!"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

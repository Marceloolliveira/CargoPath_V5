from flask import Blueprint, request, jsonify
from ...data_base.db_classes.DatabaseConnection import DatabaseConnection

localizacao_blueprint = Blueprint('localizacao', __name__)

# Endpoint para criar uma nova localização
@localizacao_blueprint.route('/api/localizacao', methods=['POST'])
def criar_localizacao():
    data = request.json
    rua = data.get('rua')
    numero = data.get('numero')
    cep = data.get('cep')
    cidade = data.get('cidade')
    estado = data.get('estado')
    complemento = data.get('complemento')
    tipo = data.get('tipo')
    cotacao_id = data.get('cotacao_id')

    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("""
            INSERT INTO localizacao (rua, numero, cep, cidade, estado, complemento, tipo, cotacao_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING localizacao_id;
        """, (rua, numero, cep, cidade, estado, complemento, tipo, cotacao_id))
        
        localizacao_id = cursor.fetchone()[0]
        db.commit()
        
        return jsonify({
            "localizacao_id": localizacao_id,
            "rua": rua,
            "numero": numero,
            "cep": cep,
            "cidade": cidade,
            "estado": estado,
            "complemento": complemento,
            "tipo": tipo,
            "cotacao_id": cotacao_id,
            "message": "Localização criada com sucesso!"
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Endpoint para listar todas as localizações
@localizacao_blueprint.route('/api/localizacoes', methods=['GET'])
def listar_localizacoes():
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("SELECT * FROM localizacao;")
        localizacoes = cursor.fetchall()
        
        # Adiciona rótulos aos dados retornados
        localizacoes_list = []
        for localizacao in localizacoes:
            localizacoes_list.append({
                "localizacao_id": localizacao[0],
                "rua": localizacao[1],
                "numero": localizacao[2],
                "cep": localizacao[3],
                "cidade": localizacao[4],
                "estado": localizacao[5],
                "complemento": localizacao[6],
                "tipo": localizacao[7],
                "cotacao_id": localizacao[8],
                "created_at": localizacao[9]
            })
        
        return jsonify(localizacoes_list), 200
    finally:
        cursor.close()
        db.close()

# Endpoint para obter uma localização específica
@localizacao_blueprint.route('/api/localizacao/<int:localizacao_id>', methods=['GET'])
def obter_localizacao(localizacao_id):
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("SELECT * FROM localizacao WHERE localizacao_id = %s;", (localizacao_id,))
        localizacao = cursor.fetchone()
        
        if localizacao:
            localizacao_detalhe = {
                "localizacao_id": localizacao[0],
                "rua": localizacao[1],
                "numero": localizacao[2],
                "cep": localizacao[3],
                "cidade": localizacao[4],
                "estado": localizacao[5],
                "complemento": localizacao[6],
                "tipo": localizacao[7],
                "cotacao_id": localizacao[8],
                "created_at": localizacao[9]
            }
            return jsonify(localizacao_detalhe), 200
        else:
            return jsonify({"message": "Localização não encontrada"}), 404
    finally:
        cursor.close()
        db.close()

# Endpoint para atualizar uma localização
@localizacao_blueprint.route('/api/localizacao/<int:localizacao_id>', methods=['PUT'])
def atualizar_localizacao(localizacao_id):
    data = request.json
    rua = data.get('rua')
    numero = data.get('numero')
    cep = data.get('cep')
    cidade = data.get('cidade')
    estado = data.get('estado')
    complemento = data.get('complemento')
    tipo = data.get('tipo')

    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("""
            UPDATE localizacao SET rua = %s, numero = %s, cep = %s, cidade = %s,
                                  estado = %s, complemento = %s, tipo = %s
            WHERE localizacao_id = %s;
        """, (rua, numero, cep, cidade, estado, complemento, tipo, localizacao_id))
        
        db.commit()
        return jsonify({
            "localizacao_id": localizacao_id,
            "rua": rua,
            "numero": numero,
            "cep": cep,
            "cidade": cidade,
            "estado": estado,
            "complemento": complemento,
            "tipo": tipo,
            "message": "Localização atualizada com sucesso!"
        }), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Endpoint para deletar uma localização
@localizacao_blueprint.route('/api/localizacao/<int:localizacao_id>', methods=['DELETE'])
def deletar_localizacao(localizacao_id):
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("DELETE FROM localizacao WHERE localizacao_id = %s;", (localizacao_id,))
        db.commit()
        
        return jsonify({"localizacao_id": localizacao_id, "message": "Localização deletada com sucesso!"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

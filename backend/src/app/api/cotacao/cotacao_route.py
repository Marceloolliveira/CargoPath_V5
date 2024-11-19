from flask import Blueprint, request, jsonify
from ...data_base.db_classes.DatabaseConnection import DatabaseConnection

cotacao_blueprint = Blueprint('cotacao', __name__)

# Endpoint para criar uma nova cotação
@cotacao_blueprint.route('/api/cotacao', methods=['POST'])
def criar_cotacao():
    data = request.json
    descricao = data.get('descricao')
    status = data.get('status')
    valor_frete = data.get('valor_frete')
    user_id = data.get('user_id')

    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("""
            INSERT INTO cotacoes (descricao, status, user_id, valor_frete)
            VALUES (%s, %s, %s, %s)
            RETURNING cotacao_id;
        """, (descricao, status, user_id, valor_frete))
        
        cotacao_id = cursor.fetchone()[0]
        db.commit()
        
        return jsonify({
            "cotacao_id": cotacao_id,
            "descricao": descricao,
            "status": status,
            "user_id": user_id,
            "valor_frete": valor_frete,
            "message": "Cotação criada com sucesso!"
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Endpoint para listar todas as cotações
@cotacao_blueprint.route('/api/cotacoes', methods=['GET'])
def listar_cotacoes():
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("SELECT * FROM cotacoes;")
        cotacoes = cursor.fetchall()
        
        # Adiciona rótulos aos dados retornados
        cotacoes_list = []
        for cotacao in cotacoes:
            cotacoes_list.append({
                "cotacao_id": cotacao[0],
                "descricao": cotacao[1],
                "status": cotacao[2],
                "user_id": cotacao[3],
                "valor_frete": cotacao[5],
                "created_at": cotacao[4]
            })
        
        return jsonify(cotacoes_list), 200
    finally:
        cursor.close()
        db.close()

# Endpoint para obter uma cotação específica
@cotacao_blueprint.route('/api/cotacao/<int:cotacao_id>', methods=['GET'])
def obter_cotacao(cotacao_id):
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("SELECT * FROM cotacoes WHERE cotacao_id = %s;", (cotacao_id,))
        cotacao = cursor.fetchone()
        
        if cotacao:
            cotacao_detalhe = {
                "cotacao_id": cotacao[0],
                "descricao": cotacao[1],
                "status": cotacao[2],
                "user_id": cotacao[3],
                "valor_frete": cotacao[5],
                "created_at": cotacao[4]
            }
            return jsonify(cotacao_detalhe), 200
        else:
            return jsonify({"message": "Cotação não encontrada"}), 404
    finally:
        cursor.close()
        db.close()

# Endpoint para atualizar uma cotação
@cotacao_blueprint.route('/api/cotacao/<int:cotacao_id>', methods=['PUT'])
def atualizar_cotacao(cotacao_id):
    data = request.json
    descricao = data.get('descricao')
    status = data.get('status')

    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("""
            UPDATE cotacoes SET descricao = %s, status = %s
            WHERE cotacao_id = %s;
        """, (descricao, status, cotacao_id))
        
        db.commit()
        return jsonify({
            "cotacao_id": cotacao_id,
            "descricao": descricao,
            "status": status,
            "message": "Cotação atualizada com sucesso!"
        }), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Endpoint para deletar uma cotação
@cotacao_blueprint.route('/api/cotacao/<int:cotacao_id>', methods=['DELETE'])
def deletar_cotacao(cotacao_id):
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("DELETE FROM cotacoes WHERE cotacao_id = %s;", (cotacao_id,))
        db.commit()
        
        return jsonify({"cotacao_id": cotacao_id, "message": "Cotação deletada com sucesso!"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

#Endpoint para trazer o resumo por cotação_Id
from flask import Blueprint, request, jsonify
from ...data_base.db_classes.DatabaseConnection import DatabaseConnection

cotacao_blueprint = Blueprint('cotacao', __name__)

@cotacao_blueprint.route('/api/cotacao/resumo/<int:cotacao_id>', methods=['GET'])
def obter_resumo_cotacao(cotacao_id):
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        # SQL ajustado para evitar conflitos de nomes
        SQL_AJUSTADO = """
            SELECT 
                cotacoes.cotacao_id,
                cotacoes.descricao AS cotacao_descricao,
                cotacoes.status AS cotacao_status,
                cotacoes.user_id AS cotacao_user_id,
                cotacoes.valor_frete AS cotacao_valor_frete,
                cotacoes.created_at AS cotacao_created_at,

                -- Campos da tabela localizacao (remetente e destinatario)
                remetente.localizacao_id AS remetente_id,
                remetente.rua AS remetente_rua,
                remetente.numero AS remetente_numero,
                remetente.cep AS remetente_cep,
                remetente.cidade AS remetente_cidade,
                remetente.estado AS remetente_estado,
                remetente.complemento AS remetente_complemento,

                destino.localizacao_id AS destino_id,
                destino.rua AS destino_rua,
                destino.numero AS destino_numero,
                destino.cep AS destino_cep,
                destino.cidade AS destino_cidade,
                destino.estado AS destino_estado,
                destino.complemento AS destino_complemento,

                -- Campos da tabela carga
                carga.carga_id AS carga_id,
                carga.valor AS carga_valor,
                carga.peso AS carga_peso,
                carga.volumes AS carga_volumes,

                -- Campos da tabela cubagem
                cubagem.cubagem_id AS cubagem_id,
                cubagem.altura AS cubagem_altura,
                cubagem.largura AS cubagem_largura,
                cubagem.comprimento AS cubagem_comprimento,
                cubagem.qtd AS cubagem_quantidade,

                -- Campos da tabela embalagem
                embalagem.embalagem_id AS embalagem_id,
                embalagem.caixa AS embalagem_caixa,
                embalagem.palet AS embalagem_palet,
                embalagem.grade AS embalagem_grade

            FROM 
                cotacoes
            LEFT JOIN localizacao AS remetente 
                ON cotacoes.cotacao_id = remetente.cotacao_id AND remetente.tipo = 1
            LEFT JOIN localizacao AS destino 
                ON cotacoes.cotacao_id = destino.cotacao_id AND destino.tipo = 2
            LEFT JOIN carga 
                ON cotacoes.cotacao_id = carga.cotacao_id
            LEFT JOIN cubagem 
                ON carga.carga_id = cubagem.carga_id
            LEFT JOIN embalagem 
                ON cubagem.cubagem_id = embalagem.cubagem_id
            WHERE 
                cotacoes.cotacao_id = %s;
        """

        # Executar o SQL e buscar os dados
        cursor.execute(SQL_AJUSTADO, (cotacao_id,))
        resumo = cursor.fetchone()

        if not resumo:
            return jsonify({"error": "Cotação não encontrada"}), 404

        # Construir o JSON de resposta com base nos apelidos
        dados = {
            "cotacao_id": resumo[0],
            "descricao": resumo[1],
            "status": resumo[2],
            "user_id": resumo[3],
            "valor_frete": float(resumo[4]),
            "created_at": resumo[5],
            "remetente": {
                "id": resumo[6],
                "rua": resumo[7],
                "numero": resumo[8],
                "cep": resumo[9],
                "cidade": resumo[10],
                "estado": resumo[11],
                "complemento": resumo[12]
            },
            "destino": {
                "id": resumo[13],
                "rua": resumo[14],
                "numero": resumo[15],
                "cep": resumo[16],
                "cidade": resumo[17],
                "estado": resumo[18],
                "complemento": resumo[19]
            },
            "carga": {
                "id": resumo[20],
                "valor": float(resumo[21]),
                "peso": float(resumo[22]),
                "volumes": resumo[23]
            },
            "cubagem": {
                "id": resumo[24],
                "altura": float(resumo[25]),
                "largura": float(resumo[26]),
                "comprimento": float(resumo[27]),
                "quantidade": resumo[28]
            },
            "embalagem": {
                "id": resumo[29],
                "caixa": resumo[30],
                "palet": resumo[31],
                "grade": resumo[32]
            }
        }

        return jsonify(dados), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()





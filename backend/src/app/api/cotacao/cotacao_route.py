from flask import Blueprint, request, jsonify
from ...data_base.db_classes.DatabaseConnection import DatabaseConnection

# Configurando o Blueprint com o prefixo /api/cotacao
cotacao_blueprint = Blueprint('cotacao', __name__, url_prefix='/api/cotacao')

# Endpoint para criar uma nova cotação
@cotacao_blueprint.route('/', methods=['POST'])
def criar_cotacao():
    data = request.json
    descricao = data.get('descricao')
    status = data.get('status')
    valor_frete = data.get('valor_frete')
    user_id = data.get('user_id')
    data_agendamento = data.get('data_agendamento')

    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("""
            INSERT INTO cotacoes (descricao, status, user_id, valor_frete, data_agendamento)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING cotacao_id;
        """, (descricao, status, user_id, valor_frete, data_agendamento))
        
        cotacao_id = cursor.fetchone()[0]
        db.commit()
        
        return jsonify({
            "cotacao_id": cotacao_id,
            "descricao": descricao,
            "status": status,
            "user_id": user_id,
            "valor_frete": valor_frete,
            "data_agendamento": data_agendamento,
            "message": "Cotação criada com sucesso!"
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Endpoint para listar todas as cotações
@cotacao_blueprint.route('/', methods=['GET'])
def listar_cotacoes():
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("SELECT * FROM cotacoes;")
        cotacoes = cursor.fetchall()
        
        cotacoes_list = []
        for cotacao in cotacoes:
            cotacoes_list.append({
                "cotacao_id": cotacao[0],
                "descricao": cotacao[1],
                "status": cotacao[2],
                "user_id": cotacao[3],
                "valor_frete": cotacao[4],
                "data_agendamento": cotacao[5],
                "created_at": cotacao[6]
            })
        
        return jsonify(cotacoes_list), 200
    finally:
        cursor.close()
        db.close()

# Endpoint para obter uma cotação específica
@cotacao_blueprint.route('/<int:cotacao_id>', methods=['GET'])
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
                "valor_frete": cotacao[4],
                "data_agendamento": cotacao[5],
                "created_at": cotacao[6]
            }
            return jsonify(cotacao_detalhe), 200
        else:
            return jsonify({"message": "Cotação não encontrada"}), 404
    finally:
        cursor.close()
        db.close()

# Endpoint para atualizar uma cotação
@cotacao_blueprint.route('/<int:cotacao_id>', methods=['PUT'])
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



# Endpoint para trazer o resumo de uma cotação por ID
@cotacao_blueprint.route('/resumo/<int:cotacao_id>', methods=['GET'])
def obter_resumo_cotacao(cotacao_id):
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        SQL_RESUMO = """
            SELECT 
                cotacoes.cotacao_id,
                cotacoes.descricao AS cotacao_descricao,
                cotacoes.status AS cotacao_status,
                cotacoes.user_id AS cotacao_user_id,
                cotacoes.valor_frete AS cotacao_valor_frete,
                cotacoes.data_agendamento AS cotacao_data_agendamento,
                cotacoes.created_at AS cotacao_created_at,

                -- Campos da tabela localizacao para remetente
                remetente.localizacao_id AS remetente_id,
                remetente.rua AS remetente_rua,
                remetente.numero AS remetente_numero,
                remetente.cep AS remetente_cep,
                remetente.cidade AS remetente_cidade,
                remetente.estado AS remetente_estado,
                remetente.complemento AS remetente_complemento,

                -- Campos da tabela localizacao para destino
                destino.localizacao_id AS destino_id,
                destino.rua AS destino_rua,
                destino.numero AS destino_numero,
                destino.cep AS destino_cep,
                destino.cidade AS destino_cidade,
                destino.estado AS destino_estado,
                destino.complemento AS destino_complemento,
                destino.destinatario_nome AS destino_destinatario_nome, 

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

        cursor.execute(SQL_RESUMO, (cotacao_id,))
        resumo = cursor.fetchone()

        if not resumo:
            return jsonify({"error": "Cotação não encontrada"}), 404

        dados = {
            "cotacao_id": resumo[0],
            "descricao": resumo[1],
            "status": resumo[2],
            "user_id": resumo[3],
            "valor_frete": float(resumo[4]),
            "data_agendamento": resumo[5].strftime("%Y-%m-%d") if resumo[5] else None,
            "created_at": resumo[6].strftime("%Y-%m-%d %H:%M:%S") if resumo[6] else None,
            "remetente": {
                "id": resumo[7],
                "rua": resumo[8],
                "numero": resumo[9],
                "cep": resumo[10],
                "cidade": resumo[11],
                "estado": resumo[12],
                "complemento": resumo[13],
            },
            "destino": {
                "id": resumo[14],
                "rua": resumo[15],
                "numero": resumo[16],
                "cep": resumo[17],
                "cidade": resumo[18],
                "estado": resumo[19],
                "complemento": resumo[20],
                "destinatario_nome": resumo[21],  # Novo campo
            },
            "carga": {
                "id": resumo[22],
                "valor": float(resumo[23]),
                "peso": float(resumo[24]),
                "volumes": resumo[25],
            },
            "cubagem": {
                "id": resumo[26],
                "altura": float(resumo[27]),
                "largura": float(resumo[28]),
                "comprimento": float(resumo[29]),
                "quantidade": resumo[30],
            },
            "embalagem": {
                "id": resumo[31],
                "caixa": resumo[32],
                "palet": resumo[33],
                "grade": resumo[34],
            },
        }

        return jsonify(dados), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@cotacao_blueprint.route('/user/<int:user_id>/coletas', methods=['GET'])
def listar_coletas_por_usuario(user_id):
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        # Query para buscar coletas por user_id
        SQL_COLETAS = """
            SELECT
                cotacoes.cotacao_id,
                cotacoes.descricao,
                cotacoes.status,
                cotacoes.data_agendamento,
                remetente.cidade AS remetente_cidade,
                destino.cidade AS destino_cidade
            FROM cotacoes
            LEFT JOIN localizacao AS remetente
                ON cotacoes.cotacao_id = remetente.cotacao_id AND remetente.tipo = 1
            LEFT JOIN localizacao AS destino
                ON cotacoes.cotacao_id = destino.cotacao_id AND destino.tipo = 2
            WHERE cotacoes.user_id = %s
            ORDER BY cotacoes.data_agendamento ASC;
        """
        cursor.execute(SQL_COLETAS, (user_id,))
        coletas = cursor.fetchall()

        if not coletas:
            return jsonify({"message": "Nenhuma coleta encontrada."}), 404

        # Preparar dados para resposta JSON
        coletas_list = []
        for coleta in coletas:
            coletas_list.append({
                "id": coleta[0],
                "descricao": coleta[1],
                "status": coleta[2],
                "data_agendamento": coleta[3].strftime("%Y-%m-%d") if coleta[3] else None,
                "remetente": coleta[4],
                "destino": coleta[5]
            })

        return jsonify(coletas_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

#endpoint para tabela historico
@cotacao_blueprint.route('/user/<int:user_id>/historico', methods=['GET'])
def obter_historico(user_id):
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor.execute("""
            SELECT 
                cotacoes.cotacao_id,
                remetente.rua AS remetente_rua,
                destino.rua AS destino_rua,
                cotacoes.data_agendamento,
                cotacoes.status
            FROM cotacoes
            LEFT JOIN localizacao AS remetente 
                ON cotacoes.cotacao_id = remetente.cotacao_id AND remetente.tipo = 1
            LEFT JOIN localizacao AS destino 
                ON cotacoes.cotacao_id = destino.cotacao_id AND destino.tipo = 2
            WHERE cotacoes.user_id = %s AND (cotacoes.status = 'finalizado' OR cotacoes.status = 'cancelado')
            ORDER BY cotacoes.data_agendamento DESC;
        """, (user_id,))
        historico = cursor.fetchall()

        if not historico:
            return jsonify([]), 200

        resultado = [
            {
                "id": row[0],
                "remetente": row[1] or "Remetente não informado",
                "destino": row[2] or "Destino não informado",
                "data_agendamento": row[3].strftime("%Y-%m-%d") if row[3] else "Não informado",
                "status": row[4]
            }
            for row in historico
        ]
        return jsonify(resultado), 200
    except Exception as e:
        print(f"Erro ao obter histórico: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()


@cotacao_blueprint.route('/user/<int:user_id>/faturas', methods=['GET'])
def listar_faturas_pagas(user_id):
    db = DatabaseConnection()
    db.connect()
    cursor = db.get_cursor()

    if cursor is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        # Query para buscar faturas pagas
        SQL_FATURAS = """
            SELECT 
                cotacoes.cotacao_id,
                remetente.rua AS remetente_rua,
                destino.rua AS destino_rua,
                cotacoes.data_agendamento,
                cotacoes.status
            FROM cotacoes
            LEFT JOIN localizacao AS remetente 
                ON cotacoes.cotacao_id = remetente.cotacao_id AND remetente.tipo = 1
            LEFT JOIN localizacao AS destino 
                ON cotacoes.cotacao_id = destino.cotacao_id AND destino.tipo = 2
            WHERE cotacoes.user_id = %s AND cotacoes.status = 'pago'
            ORDER BY cotacoes.data_agendamento DESC;
        """
        cursor.execute(SQL_FATURAS, (user_id,))
        faturas = cursor.fetchall()

        if not faturas:
            return jsonify([]), 200

        # Preparar os dados para resposta JSON
        resultado = [
            {
                "id": row[0],
                "remetente": row[1] or "Remetente não informado",
                "destino": row[2] or "Destino não informado",
                "data_agendamento": row[3].strftime("%Y-%m-%d") if row[3] else "Não informado",
                "status": row[4]
            }
            for row in faturas
        ]

        return jsonify(resultado), 200
    except Exception as e:
        print(f"Erro ao obter faturas pagas: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()




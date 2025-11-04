from ...data_base.db_classes.DatabaseConnection import DatabaseConnection
from flask import jsonify

class LocalizacaoService:
    @staticmethod
    def handle_criar_localizacao(request):
        """
        Manipula a requisição de criação de localização
        """
        try:
            data = request.json
            if not data:
                return jsonify({"error": "Dados não fornecidos"}), 400

            # Extração dos dados
            rua = data.get('rua')
            numero = data.get('numero')
            cep = data.get('cep')
            cidade = data.get('cidade')
            estado = data.get('estado')
            complemento = data.get('complemento')
            tipo = data.get('tipo')
            cotacao_id = data.get('cotacao_id')
            destinatario_nome = data.get('destinatario_nome')

            # Validações básicas
            if not all([rua, numero, cep, cidade, estado, tipo, cotacao_id]):
                return jsonify({"error": "Campos obrigatórios não preenchidos"}), 400

            # Criar localização
            result = LocalizacaoService.criar_localizacao(
                rua, numero, cep, cidade, estado, complemento, tipo, cotacao_id, destinatario_nome
            )
            
            return result

        except Exception as e:
            return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

    @staticmethod
    def criar_localizacao(rua, numero, cep, cidade, estado, complemento, tipo, cotacao_id, destinatario_nome):
        """
        Cria uma nova localização no banco de dados
        """
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        if cursor is None:
            return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

        try:
            cursor.execute("""
                INSERT INTO localizacao (rua, numero, cep, cidade, estado, complemento, tipo, cotacao_id, destinatario_nome)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING localizacao_id;
            """, (rua, numero, cep, cidade, estado, complemento, tipo, cotacao_id, destinatario_nome))
            
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
                "destinatario_nome": destinatario_nome,
                "message": "Localização criada com sucesso!"
            }), 201
        except Exception as e:
            db.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def listar_localizacoes():
        """
        Lista todas as localizações
        """
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
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def obter_localizacao(localizacao_id):
        """
        Obtém uma localização específica
        """
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
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def handle_atualizar_localizacao(localizacao_id, request):
        """
        Manipula a requisição de atualização de localização
        """
        try:
            data = request.json
            if not data:
                return jsonify({"error": "Dados não fornecidos"}), 400

            rua = data.get('rua')
            numero = data.get('numero')
            cep = data.get('cep')
            cidade = data.get('cidade')
            estado = data.get('estado')
            complemento = data.get('complemento')
            tipo = data.get('tipo')

            return LocalizacaoService.atualizar_localizacao(
                localizacao_id, rua, numero, cep, cidade, estado, complemento, tipo
            )

        except Exception as e:
            return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

    @staticmethod
    def atualizar_localizacao(localizacao_id, rua, numero, cep, cidade, estado, complemento, tipo):
        """
        Atualiza uma localização
        """
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

    @staticmethod
    def deletar_localizacao(localizacao_id):
        """
        Deleta uma localização
        """
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
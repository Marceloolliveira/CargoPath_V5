from ...data_base.db_classes.DatabaseConnection import DatabaseConnection

class CotacaoService:
    def criar_cotacao(self, data):
        descricao = data.get('descricao')
        status = data.get('status')
        valor_frete = data.get('valor_frete')
        user_id = data.get('user_id')
        data_agendamento = data.get('data_agendamento')

        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        try:
            cursor.execute(, (descricao, status, user_id, valor_frete, data_agendamento))
            
            cotacao_id = cursor.fetchone()[0]
            db.commit()

            return {
                "cotacao_id": cotacao_id,
                "descricao": descricao,
                "status": status,
                "user_id": user_id,
                "valor_frete": valor_frete,
                "data_agendamento": data_agendamento,
                "message": "Cotação criada com sucesso!"
            }
        except Exception as e:
            db.rollback()
            raise Exception(e)
        finally:
            cursor.close()
            db.close()

    def listar_cotacoes(self):
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()
        try:
            cursor.execute("SELECT * FROM cotacoes;")
            cotacoes = cursor.fetchall()

            return [
                {
                    "cotacao_id": row[0],
                    "descricao": row[1],
                    "status": row[2],
                    "user_id": row[3],
                    "valor_frete": row[4],
                    "data_agendamento": row[5],
                    "created_at": row[6]
                }
                for row in cotacoes
            ]
        finally:
            cursor.close()
            db.close()

    def obter_cotacao(self, cotacao_id):
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()
        try:
            cursor.execute("SELECT * FROM cotacoes WHERE cotacao_id = %s;", (cotacao_id,))
            cotacao = cursor.fetchone()
            if not cotacao:
                return None
            return {
                "cotacao_id": cotacao[0],
                "descricao": cotacao[1],
                "status": cotacao[2],
                "user_id": cotacao[3],
                "valor_frete": cotacao[4],
                "data_agendamento": cotacao[5],
                "created_at": cotacao[6]
            }
        finally:
            cursor.close()
            db.close()

    def atualizar_cotacao(self, cotacao_id, data):
        descricao = data.get('descricao')
        status = data.get('status')

        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()
        try:
            cursor.execute(, (descricao, status, cotacao_id))
            db.commit()
            return {
                "cotacao_id": cotacao_id,
                "descricao": descricao,
                "status": status,
                "message": "Cotação atualizada com sucesso!"
            }
        except Exception as e:
            db.rollback()
            raise Exception(e)
        finally:
            cursor.close()
            db.close()

    def deletar_cotacao(self, cotacao_id):
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()
        try:
            cursor.execute("DELETE FROM cotacoes WHERE cotacao_id = %s;", (cotacao_id,))
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(e)
        finally:
            cursor.close()
            db.close()

    

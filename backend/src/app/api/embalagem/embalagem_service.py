from ...data_base.db_classes.DatabaseConnection import DatabaseConnection

class EmbalagemService:

    @staticmethod
    def criar_embalagem(data):
        caixa = data.get('caixa')
        palet = data.get('palet')
        grade = data.get('grade')
        cubagem_id = data.get('cubagem_id')

        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        if cursor is None:
            raise Exception("Erro ao conectar ao banco de dados")

        try:
            cursor.execute(, (caixa, palet, grade, cubagem_id))

            embalagem_id = cursor.fetchone()[0]
            db.commit()

            return {
                "embalagem_id": embalagem_id,
                "caixa": caixa,
                "palet": palet,
                "grade": grade,
                "cubagem_id": cubagem_id,
                "message": "Embalagem criada com sucesso!"
            }
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def listar_embalagens():
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        if cursor is None:
            raise Exception("Erro ao conectar ao banco de dados")

        try:
            cursor.execute("SELECT * FROM embalagem;")
            embalagens = cursor.fetchall()

            return [
                {
                    "embalagem_id": emb[0],
                    "caixa": emb[1],
                    "palet": emb[2],
                    "grade": emb[3],
                    "cubagem_id": emb[4],
                    "created_at": emb[5]
                } for emb in embalagens
            ]
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def obter_embalagem(embalagem_id):
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        if cursor is None:
            raise Exception("Erro ao conectar ao banco de dados")

        try:
            cursor.execute("SELECT * FROM embalagem WHERE embalagem_id = %s;", (embalagem_id,))
            emb = cursor.fetchone()

            if not emb:
                return None

            return {
                "embalagem_id": emb[0],
                "caixa": emb[1],
                "palet": emb[2],
                "grade": emb[3],
                "cubagem_id": emb[4],
                "created_at": emb[5]
            }
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def atualizar_embalagem(embalagem_id, data):
        caixa = data.get('caixa')
        palet = data.get('palet')
        grade = data.get('grade')

        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        if cursor is None:
            raise Exception("Erro ao conectar ao banco de dados")

        try:
            cursor.execute(, (caixa, palet, grade, embalagem_id))
            db.commit()

            return {
                "embalagem_id": embalagem_id,
                "caixa": caixa,
                "palet": palet,
                "grade": grade,
                "message": "Embalagem atualizada com sucesso!"
            }
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def deletar_embalagem(embalagem_id):
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        if cursor is None:
            raise Exception("Erro ao conectar ao banco de dados")

        try:
            cursor.execute("DELETE FROM embalagem WHERE embalagem_id = %s;", (embalagem_id,))
            db.commit()

            return {
                "embalagem_id": embalagem_id,
                "message": "Embalagem deletada com sucesso!"
            }
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()

from ...data_base.db_classes.DatabaseConnection import DatabaseConnection

class CubagemService:
    @staticmethod
    def criar_cubagem(altura, largura, comprimento, qtd, carga_id):
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        try:
            cursor.execute("""
                INSERT INTO cubagem (altura, largura, comprimento, qtd, carga_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING cubagem_id;
            """, (altura, largura, comprimento, qtd, carga_id))
            
            cubagem_id = cursor.fetchone()[0]
            db.commit()
            return cubagem_id
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def listar_cubagens():
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        try:
            cursor.execute("SELECT * FROM cubagem;")
            return cursor.fetchall()
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def obter_cubagem(cubagem_id):
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        try:
            cursor.execute("SELECT * FROM cubagem WHERE cubagem_id = %s;", (cubagem_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def atualizar_cubagem(cubagem_id, altura, largura, comprimento, qtd):
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        try:
            cursor.execute("""
                UPDATE cubagem
                SET altura = %s, largura = %s, comprimento = %s, qtd = %s
                WHERE cubagem_id = %s;
            """, (altura, largura, comprimento, qtd, cubagem_id))
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def deletar_cubagem(cubagem_id):
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        try:
            cursor.execute("DELETE FROM cubagem WHERE cubagem_id = %s;", (cubagem_id,))
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
            db.close()

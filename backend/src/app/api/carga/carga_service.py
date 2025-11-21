from ...data_base.db_classes.DatabaseConnection import DatabaseConnection

class CargaService:
    def criar_carga(self, valor, peso, volumes, cotacao_id):
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        try:
            cursor.execute(, (valor, peso, volumes, cotacao_id))

            carga_id = cursor.fetchone()[0]
            db.commit()

            return {
                "carga_id": carga_id,
                "valor": valor,
                "peso": peso,
                "volumes": volumes,
                "cotacao_id": cotacao_id,
                "message": "Carga criada com sucesso!"
            }

        except Exception as e:
            db.rollback()
            raise Exception(f"Erro ao criar carga: {e}")
        finally:
            cursor.close()
            db.close()

    def listar_cargas(self):
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        try:
            cursor.execute("SELECT * FROM carga;")
            cargas = cursor.fetchall()

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
            return cargas_list
        finally:
            cursor.close()
            db.close()

    def obter_carga(self, carga_id):
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        try:
            cursor.execute("SELECT * FROM carga WHERE carga_id = %s;", (carga_id,))
            carga = cursor.fetchone()
            if carga:
                return {
                    "carga_id": carga[0],
                    "valor": carga[1],
                    "peso": carga[2],
                    "volumes": carga[3],
                    "cotacao_id": carga[4],
                    "created_at": carga[5]
                }
            return None
        finally:
            cursor.close()
            db.close()

    def atualizar_carga(self, carga_id, valor, peso, volumes):
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        try:
            cursor.execute(, (valor, peso, volumes, carga_id))
            db.commit()

            return {
                "carga_id": carga_id,
                "valor": valor,
                "peso": peso,
                "volumes": volumes,
                "message": "Carga atualizada com sucesso!"
            }
        except Exception as e:
            db.rollback()
            raise Exception(f"Erro ao atualizar carga: {e}")
        finally:
            cursor.close()
            db.close()

    def deletar_carga(self, carga_id):
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        try:
            cursor.execute("DELETE FROM carga WHERE carga_id = %s;", (carga_id,))
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Erro ao deletar carga: {e}")
        finally:
            cursor.close()
            db.close()

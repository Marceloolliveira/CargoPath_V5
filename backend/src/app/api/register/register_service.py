from ...data_base.db_classes.DatabaseConnection import DatabaseConnection
import bcrypt

class RegisterService:
    def create_user(self, name, telefone, cpf, email, password):
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()

        try:
            cursor.execute(
                ,
                (email, hashed_password.decode('utf-8'), name, telefone, cpf)
            )
            db.connection.commit()
            return "Usuário cadastrado com sucesso"
        except Exception as e:
            db.connection.rollback()
            raise Exception(f"Erro ao cadastrar usuário: {e}")
        finally:
            db.close()

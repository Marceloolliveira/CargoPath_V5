import os
import psycopg2
from psycopg2 import OperationalError

class DatabaseConnection:
    def __init__(self, dbname=os.getenv("dbname"), user=os.getenv("user"), password=os.getenv("password"), host=os.getenv("host"), port=os.getenv("port")):
        self.cargo_path = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    # Método para abrir a conexão
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.cargo_path,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Conexão com o banco de dados estabelecida com sucesso.")
        except OperationalError as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.connection = None

    # Método para obter um cursor
    def get_cursor(self):
        if self.connection:
            return self.connection.cursor()
        else:
            print("Conexão não estabelecida. Por favor, chame o método 'connect' primeiro.")
            return None

    # Método para confirmar transações
    def commit(self):
        if self.connection:
            self.connection.commit()
        else:
            print("Nenhuma conexão ativa para confirmar transações.")

    # Método para desfazer transações
    def rollback(self):
        if self.connection:
            self.connection.rollback()
        else:
            print("Nenhuma conexão ativa para desfazer transações.")

    # Método para fechar a conexão
    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexão com o banco de dados fechada.")
        else:
            print("A conexão já está fechada ou não foi inicializada.")

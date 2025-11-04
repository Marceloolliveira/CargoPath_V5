from DatabaseConnection import DatabaseConnection  # Importe a classe DatabaseConnection
# Função para criar tabelas no banco de dados
def create_tables():
    # Crie uma instância da classe DatabaseConnection
    db_connection = DatabaseConnection()
    
    # Estabeleça a conexão
    db_connection.connect()
    
    # Obtenha o cursor
    cursor = db_connection.get_cursor()
    
    if cursor:
        try:
            create_table_users = """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                telefone VARCHAR(255) NOT NULL,
                cpf VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
            """

            # Cria users
            cursor.execute(create_table_users)
            print("Tabela 'users' criada com sucesso.")

            # Cria cotacoes (depende de users)
            create_table_cotacoes = """
            CREATE TABLE IF NOT EXISTS cotacoes (
                cotacao_id SERIAL PRIMARY KEY,
                descricao VARCHAR(500) NOT NULL,
                status VARCHAR(50) NOT NULL,
                user_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                created_at TIMESTAMP DEFAULT NOW(),
                valor_frete NUMERIC(10,2)
            );
            """
            cursor.execute(create_table_cotacoes)
            print("Tabela 'cotacoes' criada com sucesso.")

            # Agora localizacao (depende de cotacoes)
            create_table_localizacao = """
            CREATE TABLE IF NOT EXISTS localizacao (
                localizacao_id SERIAL PRIMARY KEY,
                rua VARCHAR(255) NOT NULL,
                numero VARCHAR(255) NOT NULL,
                cep VARCHAR(255) NOT NULL,
                cidade VARCHAR(255) NOT NULL,
                estado VARCHAR(255) NOT NULL,
                complemento VARCHAR(255) NOT NULL,
                tipo INT NOT NULL,
                cotacao_id INT NOT NULL,
                FOREIGN KEY (cotacao_id) REFERENCES cotacoes(cotacao_id),
                created_at TIMESTAMP DEFAULT NOW()
            );
            """
            cursor.execute(create_table_localizacao)
            print("Tabela 'localizacao' criada com sucesso.")

            # carga (depende de cotacoes)
            create_table_carga = """
            CREATE TABLE IF NOT EXISTS carga (
                carga_id SERIAL PRIMARY KEY,
                valor DECIMAL(10,2) NOT NULL,
                peso DECIMAL(10,2) NOT NULL,
                volumes INT NOT NULL,
                cotacao_id INT NOT NULL,
                FOREIGN KEY (cotacao_id) REFERENCES cotacoes(cotacao_id),
                created_at TIMESTAMP DEFAULT NOW()
            );
            """
            cursor.execute(create_table_carga)
            print("Tabela 'carga' criada com sucesso.")

            # cubagem (depende de carga)
            create_table_cubagem = """
            CREATE TABLE IF NOT EXISTS cubagem (
                cubagem_id SERIAL PRIMARY KEY,
                altura DECIMAL(10,2) NOT NULL,
                largura DECIMAL(10,2) NOT NULL,
                comprimento DECIMAL(10,2) NOT NULL,
                qtd INT NOT NULL,
                carga_id INT NOT NULL,
                FOREIGN KEY (carga_id) REFERENCES carga(carga_id),
                created_at TIMESTAMP DEFAULT NOW()
            );
            """
            cursor.execute(create_table_cubagem)
            print("Tabela 'cubagem' criada com sucesso.")

            # embalagem (depende de cubagem)
            create_table_embalagem = """
            CREATE TABLE IF NOT EXISTS embalagem (
                embalagem_id SERIAL PRIMARY KEY,
                caixa VARCHAR(255),
                palet VARCHAR(255),
                grade VARCHAR(255),
                cubagem_id INT NOT NULL,
                FOREIGN KEY (cubagem_id) REFERENCES cubagem(cubagem_id),
                created_at TIMESTAMP DEFAULT NOW()
            );
            """
            cursor.execute(create_table_embalagem)
            print("Tabela 'embalagem' criada com sucesso.")

            # Commit as alterações
            db_connection.commit()

        except Exception as e:
            # Em caso de erro, faz rollback e imprime o erro
            print(f"Erro ao criar tabelas: {e}")
            try:
                db_connection.rollback()
            except Exception:
                pass
    
    # Fechar a conexão
    db_connection.close()

# Executar a função se o script for chamado diretamente
if __name__ == "__main__":
    create_tables()

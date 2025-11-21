from DatabaseConnection import DatabaseConnection  

def create_tables():
    
    db_connection = DatabaseConnection()
    
    
    db_connection.connect()
    
    
    cursor = db_connection.get_cursor()
    
    if cursor:
        try:
            create_table_users = 

            
            cursor.execute(create_table_users)
            print("Tabela 'users' criada com sucesso.")

            
            create_table_cotacoes = 
            cursor.execute(create_table_cotacoes)
            print("Tabela 'cotacoes' criada com sucesso.")

            
            create_table_localizacao = 
            cursor.execute(create_table_localizacao)
            print("Tabela 'localizacao' criada com sucesso.")

            
            create_table_carga = 
            cursor.execute(create_table_carga)
            print("Tabela 'carga' criada com sucesso.")

            
            create_table_cubagem = 
            cursor.execute(create_table_cubagem)
            print("Tabela 'cubagem' criada com sucesso.")

            
            create_table_embalagem = 
            cursor.execute(create_table_embalagem)
            print("Tabela 'embalagem' criada com sucesso.")

            
            db_connection.commit()

        except Exception as e:
            
            print(f"Erro ao criar tabelas: {e}")
            try:
                db_connection.rollback()
            except Exception:
                pass
    
    
    db_connection.close()


if __name__ == "__main__":
    create_tables()

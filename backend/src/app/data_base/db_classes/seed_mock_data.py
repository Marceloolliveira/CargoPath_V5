import os
from dotenv import load_dotenv
from DatabaseConnection import DatabaseConnection
import random
import bcrypt

# Carregar variáveis de ambiente
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '.env'))


def seed_mock_data():
    print(f"[DEBUG] Variáveis de ambiente:")
    print(f"  dbname: {os.getenv('dbname')}")
    print(f"  user: {os.getenv('user')}")
    print(f"  password: {os.getenv('password')}")
    print(f"  host: {os.getenv('host')}")
    print(f"  port: {os.getenv('port')}")
    
    # Tentar conexão direta com parâmetros explícitos
    db = DatabaseConnection(
        dbname="cargo_path",
        user="adm", 
        password="adm",
        host="localhost",
        port="5432"
    )
    db.connect()
    cursor = db.get_cursor()
    if not cursor:
        print('Não foi possível obter cursor. Abortando seed.')
        return

    try:
        print('Iniciando seed: criando apenas usuário admin e várias cotações vinculadas a ele')

        admin_email = os.getenv('admin_email')
        admin_password = os.getenv('admin_password')
        admin_name = os.getenv('admin_name')
        admin_telefone = os.getenv('admin_telefone')
        admin_cpf = os.getenv('admin_cpf')

        hashed_pwd = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute(
            """
            INSERT INTO users (email, password, name, telefone, cpf)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING
            RETURNING user_id, password
            """,
            (admin_email, hashed_pwd, admin_name, admin_telefone, admin_cpf),
        )
        row = cursor.fetchone()
        if row:
            admin_id = row[0]
        else:
            cursor.execute("SELECT user_id, password FROM users WHERE email = %s", (admin_email,))
            r = cursor.fetchone()
            admin_id = r[0]
            existing_password = r[1]
            if not (isinstance(existing_password, str) and existing_password.startswith('$2')):
                cursor.execute("UPDATE users SET password = %s WHERE user_id = %s", (hashed_pwd, admin_id))
                print('Senha antiga do admin substituída por hash bcrypt')

        print(f'Admin confirmado: email={admin_email} id={admin_id}')

        desired_cotacoes = 10
        cursor.execute("SELECT COUNT(*) FROM cotacoes WHERE user_id = %s", (admin_id,))
        existing = cursor.fetchone()[0]
        to_create = max(0, desired_cotacoes - existing)
        print(f'Cotacoes existentes para admin: {existing}. Serão criadas: {to_create}')

        for i in range(to_create):
            descricao = f'Cotação demo admin #{i+1}'
            valor_frete = round(random.uniform(50, 1200), 2)
            
            # Criar cotações com diferentes status
            status_options = ['pendente', 'agendada', 'em_transito', 'finalizada', 'cancelada']
            status = random.choice(status_options)
            
            cursor.execute(
                """
                INSERT INTO cotacoes (descricao, status, user_id, valor_frete)
                VALUES (%s, %s, %s, %s)
                RETURNING cotacao_id
                """,
                (descricao, status, admin_id, valor_frete),
            )
            cotacao_id = cursor.fetchone()[0]
            print(f'  Criada cotacao id={cotacao_id} status={status} ({descricao})')

            remetente = (f'Rua das Flores {i+1}', str(100 + i), f'0100{i}0-000', 'São Paulo', 'SP', 'Sem complemento', 1, cotacao_id)
            destino = (f'Avenida Central {i+1}', str(200 + i), f'0200{i}0-000', 'Rio de Janeiro', 'RJ', 'Sem complemento', 2, cotacao_id)

            cursor.execute(
                """
                INSERT INTO localizacao (rua, numero, cep, cidade, estado, complemento, tipo, cotacao_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING localizacao_id
                """,
                remetente,
            )
            remetente_id = cursor.fetchone()[0]
            cursor.execute(
                """
                INSERT INTO localizacao (rua, numero, cep, cidade, estado, complemento, tipo, cotacao_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING localizacao_id
                """,
                destino,
            )
            destino_id = cursor.fetchone()[0]
            print(f'    Localizacoes criadas: remetente_id={remetente_id}, destino_id={destino_id}')

            valor_carga = round(random.uniform(100, 2000), 2)
            peso = round(random.uniform(5, 200), 2)
            volumes = random.randint(1, 5)
            cursor.execute(
                """
                INSERT INTO carga (valor, peso, volumes, cotacao_id)
                VALUES (%s, %s, %s, %s)
                RETURNING carga_id
                """,
                (valor_carga, peso, volumes, cotacao_id),
            )
            carga_id = cursor.fetchone()[0]
            print(f'    Carga criada id={carga_id} valor={valor_carga} peso={peso} volumes={volumes}')

            n_cub = random.randint(1, 2)
            last_cubagem_id = None
            for c in range(n_cub):
                altura = round(random.uniform(10, 200), 2)
                largura = round(random.uniform(10, 200), 2)
                comprimento = round(random.uniform(10, 200), 2)
                qtd = random.randint(1, 10)
                cursor.execute(
                    """
                    INSERT INTO cubagem (altura, largura, comprimento, qtd, carga_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING cubagem_id
                    """,
                    (altura, largura, comprimento, qtd, carga_id),
                )
                cubagem_id = cursor.fetchone()[0]
                last_cubagem_id = cubagem_id
                print(f'      Cubagem criada id={cubagem_id} {altura}x{largura}x{comprimento} qtd={qtd}')

            caixa = 'sim' if random.random() < 0.6 else None
            palet = 'sim' if not caixa and random.random() < 0.5 else None
            grade = 'sim' if not caixa and not palet else None
            cursor.execute(
                """
                INSERT INTO embalagem (caixa, palet, grade, cubagem_id)
                VALUES (%s, %s, %s, %s)
                RETURNING embalagem_id
                """,
                (caixa, palet, grade, last_cubagem_id),
            )
            embalagem_id = cursor.fetchone()[0]
            print(f'      Embalagem criada id={embalagem_id} (cubagem_id={last_cubagem_id})')

        db.commit()
        print('Seed completo e commit realizado.')

        # Adicionar algumas cotações para o usuário ID 2 se ele existir
        try:
            cursor.execute("SELECT user_id FROM users WHERE user_id = 2")
            user2_exists = cursor.fetchone()
            
            if user2_exists:
                print('Adicionando cotações para o usuário ID 2...')
                status_options = ['agendada', 'em_transito', 'finalizada', 'pendente', 'cancelada']
                
                for i in range(10):  # Criar 10 cotações para o usuário 2
                    descricao = f'Cotação usuário 2 #{i+1}'
                    valor_frete = round(random.uniform(100, 1500), 2)
                    status = random.choice(status_options)
                    
                    cursor.execute(
                        """
                        INSERT INTO cotacoes (descricao, status, user_id, valor_frete)
                        VALUES (%s, %s, %s, %s)
                        RETURNING cotacao_id
                        """,
                        (descricao, status, 2, valor_frete),
                    )
                    cotacao_id = cursor.fetchone()[0]
                    print(f'  Criada cotacao id={cotacao_id} status={status} valor={valor_frete} para usuário 2')
                
                db.commit()
                print('Cotações para usuário ID 2 criadas com sucesso.')
            else:
                print('Usuário ID 2 não existe, pulando criação de cotações.')
        except Exception as e:
            print(f'Erro ao criar cotações para usuário 2: {e}')

    except Exception as e:
        print('Erro ao inserir dados de mock:', e)
        try:
            db.rollback()
        except Exception:
            pass
    finally:
        db.close()


if __name__ == '__main__':
    seed_mock_data()

import os
from DatabaseConnection import DatabaseConnection
import random
import bcrypt


def seed_mock_data():
    db = DatabaseConnection()
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
            descricao = f'Cotação demo admin
            valor_frete = round(random.uniform(50, 1200), 2)
            cursor.execute(
                """
                INSERT INTO cotacoes (descricao, status, user_id, valor_frete)
                VALUES (%s, %s, %s, %s)
                RETURNING cotacao_id
                """,
                (descricao, 'pendente', admin_id, valor_frete),
            )
            cotacao_id = cursor.fetchone()[0]
            print(f'  Criada cotacao id={cotacao_id} ({descricao})')

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

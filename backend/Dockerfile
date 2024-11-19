# Use uma imagem base do Python
FROM python:3.11

# Defina o diretório de trabalho
WORKDIR /app

# Copie o restante do código da aplicação
COPY . .

# Instale o psycopg2-binary
RUN pip install psycopg2-binary

# Comando para executar a aplicação (ajuste conforme necessário)
CMD ["python", "src/app/data-base/class/DatabaseConnection.py"]  # ou o arquivo que inicia sua aplicação

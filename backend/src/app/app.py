import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from flask import Flask
from flask_cors import CORS
from src.app.api.register.register_route import register_blueprint
from src.app.api.login.login_route import login_blueprint
from src.app.api.carga.carga_route import carga_blueprint
from src.app.api.cotacao.cotacao_route import cotacao_blueprint
from src.app.api.cubagem.cubagem_route import cubagem_blueprint
from src.app.api.localizacao.localizacao_route import localizacao_blueprint
from src.app.api.embalagem.embalagem_route import embalagem_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adm'  # Defina uma chave secreta forte

# Permitir CORS para todas as rotas
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5501"}}) # Configura o CORS para permitir requisições apenas da porta 5500

# Registro dos Blueprints
app.register_blueprint(register_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(carga_blueprint)
app.register_blueprint(cotacao_blueprint)
app.register_blueprint(cubagem_blueprint)
app.register_blueprint(localizacao_blueprint)
app.register_blueprint(embalagem_blueprint)

if __name__ == "__main__":
    app.run(debug=True)

https://www.youtube.com/watch?v=5oRAtPFpMzo

# 🚚 CargoPath V5

> Uma plataforma completa para gerenciamento de cargas, cotações e logística com integração de pagamentos via Mercado Pago.

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com)
[![Node.js](https://img.shields.io/badge/Node.js-Testing-68A063.svg)](https://nodejs.org)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED.svg)](https://docker.com)

---

## 📋 Sobre o Projeto

CargoPath é um sistema web moderno desenvolvido para facilitar o gerenciamento de operações logísticas:

- ✅ **Registro e Autenticação** - Sistema seguro de usuários com JWT
- 📦 **Gestão de Cargas** - Rastreamento completo e em tempo real
- 💰 **Sistema de Cotações** - Cálculo automático de preços de frete
- 📐 **Cálculo de Cubagem** - Otimização de espaço de produtos
- 📍 **Localização** - Pontos de coleta e entrega
- 📋 **Embalagem** - Preparação de cargas
- 📊 **Dashboard** - Relatórios e análises
- 💳 **Pagamentos** - Integração com Mercado Pago

## 🏗️ Arquitetura

### 🐍 Backend (Python + Flask)
- **Controllers**: Rotas e endpoints da API
- **Services**: Lógica de negócio
- **Database**: PostgreSQL

### 🌐 Frontend (JavaScript)
- **HTML5 + CSS3** - Interface responsiva
- **JavaScript Vanilla** - Lógica da aplicação

### 🧪 Testes
- **Python**: pytest para backend
- **Node.js**: Jest para frontend

## 🛠️ Tecnologias

### Backend
- **Python 3.x** + **Flask 3.1.2**
- **PostgreSQL** + **psycopg2**
- **JWT** + **bcrypt** (autenticação)
- **Mercado Pago SDK**
- **Docker**

### Frontend
- **HTML5 + CSS3 + JavaScript**

### Testes
- **pytest** (Python)
- **Jest** (Node.js)

## 🚀 Como Executar

### 📋 Pré-requisitos
- **Python 3.x**
- **Node.js** (para testes)
- **Docker**

### ⚡ Início Rápido

```bash
# 1. Clone o projeto
git clone https://github.com/MarceloOlliveira/CargoPath_V5.git
cd CargoPath_V5

# 2. Configure o ambiente
cp backend/.env.example backend/.env
# Edite o .env com suas configurações

# 3. Suba o banco de dados
cd backend
docker-compose up -d

# 4. Instale dependências Python
pip install -r ../requirements.txt

# 5. Configure banco e dados de teste
cd src/app
python data_base/db_classes/create_tables.py
python data_base/db_classes/seed_mock_data.py

# 6. Execute o backend
python app.py

# 7. Para testes frontend (opcional)
cd ../../../front
npm install
npm test
```

## 📂 Estrutura do Projeto

```
CargoPath_V5/
├── 📁 backend/
│   ├── 🐍 src/app/
│   │   ├── app.py
│   │   ├── 📁 api/ (Controllers & Services)
│   │   └── 📁 data_base/
│   ├── 🧪 test/ (pytest)
│   ├── 🐳 docker-compose.yml
│   └── ⚙️ pytest.ini
├── 📁 front/
│   ├── 🌐 login.html/css/js
│   ├── 📁 src/app/pages/
│   ├── 🧪 test/ (Jest)
│   └── 📦 package.json
└── 📋 requirements.txt
```

## 🧪 Testes

**Backend (Python):**
```bash
cd backend
pytest
```

**Frontend (Node.js):**
```bash
cd front
npm install
npm test
```

## 📚 API Endpoints

### 🔐 Autenticação
- `POST /login` - Fazer login
- `POST /register` - Registrar usuário

### 📦 Principais
- `GET/POST /api/carga` - Gestão de cargas
- `GET/POST /api/cotacao` - Sistema de cotações
- `GET /api/dashboard` - Dados do dashboard
- `POST /api/mercadopago/payment` - Pagamentos

## 🔐 Configuração (.env)

```env
# Database
DB_HOST=localhost
DB_NAME=cargopath
DB_USER=postgres
DB_PASSWORD=admin123

# Segurança
SECRET_KEY=sua-chave-secreta

# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=seu-token
```
---

<div align="center">

### 🚚 **CargoPath V5** - *Conectando cargas, destinos e oportunidades*

**Desenvolvido com ❤️ pela equipe CargoPath**

*Última atualização: Novembro 2025*

</div>

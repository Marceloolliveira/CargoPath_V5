# CargoPath V5

Uma plataforma completa para gerenciamento de cargas, cotações e logística com integração de pagamentos via Mercado Pago.

## 📋 Sobre o Projeto

CargoPath é um sistema web moderno desenvolvido para facilitar o gerenciamento de operações logísticas, incluindo:

- **Registro e Autenticação** de usuários com segurança
- **Gestão de Cargas** e rastreamento
- **Sistema de Cotações** para preços de frete
- **Cálculo de Cubagem** de produtos
- **Localização** de pontos de coleta e entrega
- **Embalagem** e preparação de cargas
- **Dashboard** com análises e relatórios
- **Integração com Mercado Pago** para pagamentos

## 🏗️ Arquitetura do Projeto

O projeto está dividido em dois principais componentes:

### Backend (Python + Flask)
API REST desenvolvida em Flask com arquitetura baseada em:
- **Controllers**: Rotas e endpoints da API
- **Services**: Lógica de negócio
- **Database**: Conexão e gerenciamento do banco de dados

### Frontend (JavaScript + HTML + CSS)
Interface web interativa com:
- Página de login e autenticação
- Dashboard com análises
- Páginas de gestão (cargas, cotações, embalagem, etc.)
- Integração com sistema de pagamentos

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.x**
- **Flask 3.1.2** - Framework web
- **Flask-CORS 6.0.1** - Suporte a CORS
- **PostgreSQL** - Banco de dados
- **psycopg2 2.9.11** - Driver PostgreSQL
- **PyJWT 2.8.0** - Autenticação JWT
- **bcrypt 5.0.0** - Hash de senhas
- **python-dotenv 1.2.1** - Variáveis de ambiente
- **Mercado Pago SDK 2.3.0** - Integração de pagamentos
- **Docker & Docker Compose** - Containerização

### Frontend
- **HTML5**
- **CSS3**
- **JavaScript (Vanilla)**

## 📦 Dependências

Ver arquivo `requirements.txt` para lista completa de dependências Python.

```
python_dotenv==1.2.1
flask==3.1.2
flask_cors==6.0.1
bcrypt==5.0.0
psycopg2==2.9.11
jwt==1.4.0
mercadopago==2.3.0
PyJWT==2.8.0
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.x instalado
- Docker (para usar o Docker Compose)

### Instalação Local

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd CargoPath_V5
```

2. **Configure as variáveis de ambiente**
Crie um arquivo `.env` na raiz do projeto:
```
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=postgresql://usuario:senha@localhost:5432/cargopath
MERCADOPAGO_TOKEN=seu-token-aqui
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados**
```bash
cd backend
docker-compose up --build
```

5. **Execute o backend**
```bash
python src/app/app.py
```
O servidor estará disponível em `http://127.0.0.1:5501/front/login.html`


## 📂 Estrutura de Pastas

```
CargoPath_V5/
├── backend/
│   ├── src/
│   │   └── app/
│   │       ├── app.py (Aplicação principal)
│   │       ├── api/ (Controllers e Services)
│   │       │   ├── register/
│   │       │   ├── login/
│   │       │   ├── carga/
│   │       │   ├── cotacao/
│   │       │   ├── cubagem/
│   │       │   ├── localizacao/
│   │       │   ├── embalagem/
│   │       │   ├── dashboard/
│   │       │   └── mercadopago/
│   │       └── data_base/
│   │           └── db_classes/
│   ├── test/ (Testes unitários)
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── pytest.ini
├── front/
│   ├── login.html / login.js / login.css
│   ├── hello.html
│   └── src/app/pages/
│       ├── dashboard/
│       ├── collections/ (Gerenciamento de cargas)
│       ├── price/ (Cotações)
│       ├── invoices/
│       ├── history/
│       └── register/
└── requirements.txt
```

## 🔐 Autenticação

O projeto utiliza JWT (JSON Web Tokens) para autenticação. O fluxo é:

1. Usuário faz login com email e senha
2. Backend retorna um token JWT
3. Cliente armazena o token
4. Token é enviado em cada requisição no header `Authorization`

## 💳 Integração Mercado Pago

O sistema integra com a API do Mercado Pago para processamento de pagamentos. Configure sua chave de acesso no arquivo `.env`.

## 🧪 Testes

Para executar os testes:

```bash
cd backend
pytest
```

## 📝 Endpoints Principais

### Autenticação
- `POST /register` - Registrar novo usuário
- `POST /login` - Fazer login

### Cargas
- `GET /carga` - Listar cargas
- `POST /carga` - Criar nova carga
- `GET /carga/<id>` - Obter detalhes da carga
- `PUT /carga/<id>` - Atualizar carga

### Cotações
- `GET /cotacao` - Listar cotações
- `POST /cotacao` - Criar cotação

### Dashboard
- `GET /dashboard` - Obter dados do dashboard

### Outras operações
- `/cubagem` - Cálculos de cubagem
- `/embalagem` - Gerenciamento de embalagem
- `/localizacao` - Localização de pontos
- `/mercadopago` - Processamento de pagamentos

## 🔄 Histórico de Versões

### V5 (Atual)
- Refatoração da arquitetura
- Melhorias no sistema de autenticação
- Integração aprimorada com Mercado Pago

---

**Última atualização:** Novembro 2025

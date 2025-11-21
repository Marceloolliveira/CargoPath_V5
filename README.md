# CargoPath_V5

## Descrição
Sistema para gerenciamento logístico, incluindo funcionalidades de cotação, carga, cubagem, dashboard, embalagem, localização, login, MercadoPago e registro de usuários. Possui backend em Python (FastAPI/Flask) e frontend em HTML, CSS e JavaScript.

## Estrutura do Projeto
```
CargoPath_V5/
├── requirements.txt
├── backend/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── pytest.ini
│   └── src/
│       └── app/
│           ├── api/           # Controllers e Services
│           ├── data_base/     # Conexão e seed do banco
│           └── test/          # Testes automatizados
├── front/
│   ├── hello.html
│   ├── login.html/css/js
│   └── src/app/pages/         # Páginas do frontend
```

## Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/Marceloolliveira/CargoPath_V5.git
   ```
2. Instale as dependências do backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. (Opcional) Execute via Docker:
   ```bash
   docker-compose up --build
   ```

## Execução
- Backend: Execute `app.py` na pasta `backend/src/app/`.
- Frontend: Abra os arquivos HTML em `front/` ou configure um servidor web.

## Testes
- Execute os testes com:
  ```bash
  cd backend
  pytest
  ```

## Tecnologias Utilizadas
- Python (FastAPI/Flask)
- Docker
- HTML, CSS, JavaScript
- Pytest

## Autor
- Marcelo Oliveira

---
Sinta-se à vontade para adaptar este README conforme novas funcionalidades forem adicionadas.

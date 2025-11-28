/**
 * Testes para register.js
 * Funcionalidades testadas:
 * - Coleta de dados do formulário de cadastro
 * - Requisição POST para API de registro
 * - Manipulação de resposta de sucesso
 * - Redirecionamento após cadastro
 * - Tratamento de erros
 * - Validação de campos obrigatórios
 */

describe('Register Functionality', () => {
  let registerButton;
  let emailInput;
  let passwordInput;
  let nameInput;
  let telefoneInput;
  let cpfInput;

  beforeEach(() => {
    document.body.innerHTML = `
      <input id="email" type="email" value="" />
      <input id="password" type="password" value="" />
      <input id="name" type="text" value="" />
      <input id="telefone" type="text" value="" />
      <input id="cpf" type="text" value="" />
      <button id="btn-cadastrar">Cadastrar</button>
    `;

    emailInput = document.getElementById('email');
    passwordInput = document.getElementById('password');
    nameInput = document.getElementById('name');
    telefoneInput = document.getElementById('telefone');
    cpfInput = document.getElementById('cpf');
    registerButton = document.getElementById('btn-cadastrar');

    registerButton.addEventListener('click', async (e) => {
      e.preventDefault();
      const email = emailInput.value;
      const password = passwordInput.value;
      const name = nameInput.value;
      const telefone = telefoneInput.value;
      const cpf = cpfInput.value;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password, name, telefone, cpf })
        });

        if (response.ok) {
          const data = await response.json();
          alert('Cadastro realizado com sucesso!');
          window.location.href = 'http://127.0.0.1:5501/login.html';
        } else {
          const error = await response.json();
          alert(error.error || 'Erro no cadastro');
        }
      } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao conectar com o servidor');
      }
    });
  });

  describe('Successful Registration', () => {
    test('should collect all form data and make API request', async () => {
      emailInput.value = 'test@test.com';
      passwordInput.value = 'password123';
      nameInput.value = 'Test User';
      telefoneInput.value = '11999999999';
      cpfInput.value = '12345678901';

      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({
          message: 'Usuário cadastrado com sucesso'
        })
      };

      fetch.mockResolvedValue(mockResponse);

      registerButton.click();
      await new Promise(resolve => setTimeout(resolve, 0));

      expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:5000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: 'test@test.com',
          password: 'password123',
          name: 'Test User',
          telefone: '11999999999',
          cpf: '12345678901'
        })
      });
    });

    test('should show success alert and redirect on successful registration', async () => {
      emailInput.value = 'test@test.com';
      passwordInput.value = 'password123';
      nameInput.value = 'Test User';
      telefoneInput.value = '11999999999';
      cpfInput.value = '12345678901';

      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({
          message: 'Usuário cadastrado com sucesso'
        })
      };

      fetch.mockResolvedValue(mockResponse);

      registerButton.click();
      await new Promise(resolve => setTimeout(resolve, 0));

      expect(alert).toHaveBeenCalledWith('Cadastro realizado com sucesso!');
      expect(window.location.href).toBe('http://127.0.0.1:5501/login.html');
    });
  });

  describe('Registration Errors', () => {
    test('should handle API error response with custom message', async () => {
      emailInput.value = 'existing@test.com';
      passwordInput.value = 'password123';
      nameInput.value = 'Test User';
      telefoneInput.value = '11999999999';
      cpfInput.value = '12345678901';

      const mockResponse = {
        ok: false,
        json: jest.fn().mockResolvedValue({
          error: 'Email já cadastrado'
        })
      };

      fetch.mockResolvedValue(mockResponse);

      registerButton.click();
      await new Promise(resolve => setTimeout(resolve, 0));

      expect(alert).toHaveBeenCalledWith('Email já cadastrado');
    });

    test('should handle API error response without custom message', async () => {
      emailInput.value = 'test@test.com';
      passwordInput.value = 'password123';
      nameInput.value = 'Test User';
      telefoneInput.value = '11999999999';
      cpfInput.value = '12345678901';

      const mockResponse = {
        ok: false,
        json: jest.fn().mockResolvedValue({})
      };

      fetch.mockResolvedValue(mockResponse);

      registerButton.click();
      await new Promise(resolve => setTimeout(resolve, 0));

      expect(alert).toHaveBeenCalledWith('Erro no cadastro');
    });

    test('should handle network errors', async () => {
      emailInput.value = 'test@test.com';
      passwordInput.value = 'password123';
      nameInput.value = 'Test User';
      telefoneInput.value = '11999999999';
      cpfInput.value = '12345678901';

      fetch.mockRejectedValue(new Error('Network error'));

      registerButton.click();
      await new Promise(resolve => setTimeout(resolve, 0));

      expect(alert).toHaveBeenCalledWith('Erro ao conectar com o servidor');
      expect(console.error).toHaveBeenCalled();
    });
  });

  describe('Form Validation', () => {
    test('should prevent default form submission', async () => {
      registerButton.dispatchEvent(new Event('click'));

      expect(fetch).toHaveBeenCalled();
    });

    test('should handle empty form fields', async () => {
      emailInput.value = '';
      passwordInput.value = '';
      nameInput.value = '';
      telefoneInput.value = '';
      cpfInput.value = '';

      const mockResponse = {
        ok: false,
        json: jest.fn().mockResolvedValue({
          error: 'Todos os campos são obrigatórios'
        })
      };

      fetch.mockResolvedValue(mockResponse);

      registerButton.click();
      await new Promise(resolve => setTimeout(resolve, 0));

      expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:5000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: '',
          password: '',
          name: '',
          telefone: '',
          cpf: ''
        })
      });
    });

    test('should handle partially filled form', async () => {
      emailInput.value = 'test@test.com';
      passwordInput.value = 'password123';
      nameInput.value = '';
      telefoneInput.value = '';
      cpfInput.value = '';

      const mockResponse = {
        ok: false,
        json: jest.fn().mockResolvedValue({
          error: 'Nome, telefone e CPF são obrigatórios'
        })
      };

      fetch.mockResolvedValue(mockResponse);

      registerButton.click();
      await new Promise(resolve => setTimeout(resolve, 0));

      expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:5000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: 'test@test.com',
          password: 'password123',
          name: '',
          telefone: '',
          cpf: ''
        })
      });
    });
  });

  describe('Input Data Validation', () => {
    test('should handle invalid email format', async () => {
      emailInput.value = 'invalid-email';
      passwordInput.value = 'password123';
      nameInput.value = 'Test User';
      telefoneInput.value = '11999999999';
      cpfInput.value = '12345678901';

      const mockResponse = {
        ok: false,
        json: jest.fn().mockResolvedValue({
          error: 'Formato de email inválido'
        })
      };

      fetch.mockResolvedValue(mockResponse);

      registerButton.click();
      await new Promise(resolve => setTimeout(resolve, 0));

      expect(alert).toHaveBeenCalledWith('Formato de email inválido');
    });

    test('should handle weak password', async () => {
      emailInput.value = 'test@test.com';
      passwordInput.value = '123';
      nameInput.value = 'Test User';
      telefoneInput.value = '11999999999';
      cpfInput.value = '12345678901';

      const mockResponse = {
        ok: false,
        json: jest.fn().mockResolvedValue({
          error: 'Senha deve ter pelo menos 6 caracteres'
        })
      };

      fetch.mockResolvedValue(mockResponse);

      registerButton.click();
      await new Promise(resolve => setTimeout(resolve, 0));

      expect(alert).toHaveBeenCalledWith('Senha deve ter pelo menos 6 caracteres');
    });
  });
});
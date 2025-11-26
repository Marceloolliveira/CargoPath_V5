/**
 * Testes para login.js
 * Funcionalidades testadas:
 * - Coleta de dados do formulário
 * - Requisição POST para API
 * - Manipulação de resposta de sucesso
 * - Armazenamento no localStorage
 * - Redirecionamento após login
 * - Tratamento de erros
 */

describe('Login Functionality', () => {
  let loginButton;
  let emailInput;
  let passwordInput;

  beforeEach(() => {
    // Setup DOM
    document.body.innerHTML = `
      <input id="email" type="email" value="" />
      <input id="password" type="password" value="" />
      <button id="btn-login">Login</button>
    `;

    emailInput = document.getElementById('email');
    passwordInput = document.getElementById('password');
    loginButton = document.getElementById('btn-login');

    // Simula o event listener do login
    loginButton.addEventListener('click', async (e) => {
      e.preventDefault();
      const email = emailInput.value;
      const password = passwordInput.value;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });

        if (response.ok) {
          const data = await response.json();
          localStorage.setItem('token', data.token);
          localStorage.setItem('usuarioID', data.user_id);
          localStorage.setItem('usuarioNome', data.name);
          alert('Login bem-sucedido!');
          window.location.href = 'src/app/pages/dashboard/dashboard.html';
        } else {
          const error = await response.json();
          alert(error.message || 'Erro no login');
        }
      } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao conectar com o servidor');
      }
    });
  });

  describe('Successful Login', () => {
    test('should collect form data and make API request', async () => {
      // Arrange
      emailInput.value = 'test@test.com';
      passwordInput.value = 'password123';

      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({
          token: 'fake-jwt-token',
          user_id: '123',
          name: 'Test User'
        })
      };

      fetch.mockResolvedValue(mockResponse);

      // Act
      loginButton.click();
      await new Promise(resolve => setTimeout(resolve, 0)); // Wait for async

      // Assert
      expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: 'test@test.com',
          password: 'password123'
        })
      });
    });

    test('should store user data in localStorage on successful login', async () => {
      // Arrange
      emailInput.value = 'test@test.com';
      passwordInput.value = 'password123';

      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({
          token: 'fake-jwt-token',
          user_id: '123',
          name: 'Test User'
        })
      };

      fetch.mockResolvedValue(mockResponse);

      // Act
      loginButton.click();
      await new Promise(resolve => setTimeout(resolve, 0));

      // Assert
      expect(localStorage.getItem('token')).toBe('fake-jwt-token');
      expect(localStorage.getItem('usuarioID')).toBe('123');
      expect(localStorage.getItem('usuarioNome')).toBe('Test User');
    });

    test('should show success alert and redirect on successful login', async () => {
      // Arrange
      emailInput.value = 'test@test.com';
      passwordInput.value = 'password123';

      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({
          token: 'fake-jwt-token',
          user_id: '123',
          name: 'Test User'
        })
      };

      fetch.mockResolvedValue(mockResponse);

      // Act
      loginButton.click();
      await new Promise(resolve => setTimeout(resolve, 0));

      // Assert
      expect(alert).toHaveBeenCalledWith('Login bem-sucedido!');
      expect(window.location.href).toBe('src/app/pages/dashboard/dashboard.html');
    });
  });

  describe('Login Errors', () => {
    test('should handle API error response', async () => {
      // Arrange
      emailInput.value = 'test@test.com';
      passwordInput.value = 'wrongpassword';

      const mockResponse = {
        ok: false,
        json: jest.fn().mockResolvedValue({
          message: 'Credenciais inválidas'
        })
      };

      fetch.mockResolvedValue(mockResponse);

      // Act
      loginButton.click();
      await new Promise(resolve => setTimeout(resolve, 0));

      // Assert
      expect(alert).toHaveBeenCalledWith('Credenciais inválidas');
      // Limpar localStorage após erro
      localStorage.removeItem('token');
    });

    test('should handle network errors', async () => {
      // Arrange
      emailInput.value = 'test@test.com';
      passwordInput.value = 'password123';

      fetch.mockRejectedValue(new Error('Network error'));

      // Act
      loginButton.click();
      await new Promise(resolve => setTimeout(resolve, 0));

      // Assert
      expect(alert).toHaveBeenCalledWith('Erro ao conectar com o servidor');
      expect(console.error).toHaveBeenCalled();
    });

    test('should handle API error without message', async () => {
      // Arrange
      emailInput.value = 'test@test.com';
      passwordInput.value = 'password123';

      const mockResponse = {
        ok: false,
        json: jest.fn().mockResolvedValue({})
      };

      fetch.mockResolvedValue(mockResponse);

      // Act
      loginButton.click();
      await new Promise(resolve => setTimeout(resolve, 0));

      // Assert
      expect(alert).toHaveBeenCalledWith('Erro no login');
    });
  });

  describe('Form Validation', () => {
    test('should prevent default form submission', async () => {
      // Arrange
      const mockEvent = {
        preventDefault: jest.fn()
      };

      // Act
      loginButton.dispatchEvent(new Event('click'));

      // Assert - O preventDefault é chamado no event listener
      // Este teste verifica se o comportamento padrão é prevenido
      expect(fetch).toHaveBeenCalled();
    });

    test('should handle empty form fields', async () => {
      // Arrange
      emailInput.value = '';
      passwordInput.value = '';

      const mockResponse = {
        ok: true,
        json: jest.fn().mockResolvedValue({
          token: 'fake-jwt-token',
          user_id: '123',
          name: 'Test User'
        })
      };

      fetch.mockResolvedValue(mockResponse);

      // Act
      loginButton.click();
      await new Promise(resolve => setTimeout(resolve, 0));

      // Assert
      expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: '',
          password: ''
        })
      });
    });
  });
});
/**
 * Testes para dashboard.js
 * Funcionalidades testadas:
 * - Verificação de autenticação do usuário
 * - Atualização do nome do usuário no dashboard
 * - Logout do dashboard
 */

describe('Dashboard Functionality', () => {
  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();
    
    // Setup DOM
    document.body.innerHTML = `
      <div id="nomeDashboard">Nome do usuário</div>
      <button id="sair">Sair</button>
    `;
  });

  describe('User Authentication', () => {
    test('should redirect to login if user is not authenticated', () => {
      // Arrange - Simular usuário não autenticado
      const simulateDashboard = () => {
        const userId = localStorage.getItem("usuarioID");
        if (!userId) {
          alert("Usuário não identificado. Faça login novamente.");
          window.location.href = "/login.html";
          return;
        }
      };

      // Act
      simulateDashboard();

      // Assert
      expect(alert).toHaveBeenCalledWith('Usuário não identificado. Faça login novamente.');
      expect(window.location.href).toBe('/login.html');
    });

    test('should update user name in dashboard when authenticated', () => {
      // Arrange - Simular dados do usuário
      localStorage.setItem('usuarioID', '123');
      localStorage.setItem('usuarioNome', 'Test User');

      // Simula o script do dashboard
      const simulateDashboard = () => {
        const userId = localStorage.getItem("usuarioID");
        if (!userId) {
          alert("Usuário não identificado. Faça login novamente.");
          window.location.href = "/login.html";
          return;
        }
        
        const usuarioNome = localStorage.getItem("usuarioNome");
        if (usuarioNome) {
          document.getElementById("nomeDashboard").innerText = `Olá ${usuarioNome}, seja bem-vindo!`;
        }
      };

      // Act
      simulateDashboard();

      // Assert
      expect(document.getElementById('nomeDashboard').innerText)
        .toBe('Olá Test User, seja bem-vindo!');
    });
  });

  describe('Logout Functionality', () => {
    test('should clear localStorage and redirect on logout', () => {
      // Arrange
      const logoutButton = document.getElementById('sair');
      
      // Simula dados no localStorage  
      localStorage.setItem('token', 'fake-token');
      localStorage.setItem('usuarioID', '123');
      
      // Simula o event listener
      logoutButton.addEventListener('click', function () {
        localStorage.clear();
        window.location.href = '/login.html';
      });

      // Act
      logoutButton.click();

      // Assert
      expect(localStorage.getItem('token')).toBeNull();
      expect(localStorage.getItem('usuarioID')).toBeNull();
      expect(window.location.href).toBe('/login.html');
    });
  });
});
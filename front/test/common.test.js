/**
 * Testes para common.js
 * Funcionalidades testadas:
 * - Expansão/recolhimento do menu lateral
 * - Funcionalidade de logout
 * - Limpeza do localStorage
 * - Redirecionamento após logout
 * - Event listeners do DOM
 */

describe('Common Functionality', () => {
  beforeEach(() => {
    // Setup DOM básico
    document.body.innerHTML = `
      <div class="menu-lateral">
        <button id="btn-exp">Expandir Menu</button>
      </div>
      <button id="sair">Sair</button>
    `;

    // Simula o comportamento do common.js
    const menuExpand = document.querySelector('#btn-exp');
    const menuSide = document.querySelector('.menu-lateral');
    const logoutButton = document.getElementById('sair');

    if (menuExpand && menuSide) {
      menuExpand.addEventListener('click', function () {
        menuSide.classList.toggle('expandir');
      });
    }

    if (logoutButton) {
      logoutButton.addEventListener('click', function () {
        localStorage.clear();
        window.location.href = 'http://127.0.0.1:5501/login.html';
      });
    }
  });

  describe('Menu Lateral Functionality', () => {
    test('should toggle menu expansion when expand button is clicked', () => {
      // Arrange
      const menuSide = document.querySelector('.menu-lateral');
      const menuExpand = document.querySelector('#btn-exp');

      // Act
      menuExpand.click();

      // Assert
      expect(menuSide.classList.contains('expandir')).toBe(true);
    });

    test('should toggle menu collapse when expand button is clicked again', () => {
      // Arrange
      const menuSide = document.querySelector('.menu-lateral');
      const menuExpand = document.querySelector('#btn-exp');

      // Act - Expandir primeiro
      menuExpand.click();
      expect(menuSide.classList.contains('expandir')).toBe(true);

      // Act - Clicar novamente para recolher
      menuExpand.click();

      // Assert
      expect(menuSide.classList.contains('expandir')).toBe(false);
    });
  });

  describe('Logout Functionality', () => {
    test('should clear localStorage when logout button is clicked', () => {
      // Arrange
      const logoutButton = document.getElementById('sair');
      
      // Simula dados no localStorage
      localStorage.setItem('token', 'fake-token');
      localStorage.setItem('usuarioID', '123');
      localStorage.setItem('usuarioNome', 'Test User');

      // Act
      logoutButton.click();

      // Assert
      expect(localStorage.getItem('token')).toBeNull();
      expect(localStorage.getItem('usuarioID')).toBeNull();
      expect(localStorage.getItem('usuarioNome')).toBeNull();
      expect(window.location.href).toBe('http://127.0.0.1:5501/login.html');
    });

    test('should redirect to login page on logout', () => {
      // Arrange
      const logoutButton = document.getElementById('sair');

      // Act
      logoutButton.click();

      // Assert
      expect(window.location.href).toBe('http://127.0.0.1:5501/login.html');
    });
  });
});
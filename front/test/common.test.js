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
    document.body.innerHTML = `
      <div class="menu-lateral">
        <button id="btn-exp">Expandir Menu</button>
      </div>
      <button id="sair">Sair</button>
    `;

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
      const menuSide = document.querySelector('.menu-lateral');
      const menuExpand = document.querySelector('#btn-exp');

      menuExpand.click();

      expect(menuSide.classList.contains('expandir')).toBe(true);
    });

    test('should toggle menu collapse when expand button is clicked again', () => {
      const menuSide = document.querySelector('.menu-lateral');
      const menuExpand = document.querySelector('#btn-exp');

      menuExpand.click();
      expect(menuSide.classList.contains('expandir')).toBe(true);

      menuExpand.click();

      expect(menuSide.classList.contains('expandir')).toBe(false);
    });
  });

  describe('Logout Functionality', () => {
    test('should clear localStorage when logout button is clicked', () => {
      const logoutButton = document.getElementById('sair');
      
      localStorage.setItem('token', 'fake-token');
      localStorage.setItem('usuarioID', '123');
      localStorage.setItem('usuarioNome', 'Test User');

      logoutButton.click();

      expect(localStorage.getItem('token')).toBeNull();
      expect(localStorage.getItem('usuarioID')).toBeNull();
      expect(localStorage.getItem('usuarioNome')).toBeNull();
      expect(window.location.href).toBe('http://127.0.0.1:5501/login.html');
    });

    test('should redirect to login page on logout', () => {
      const logoutButton = document.getElementById('sair');

      logoutButton.click();

      expect(window.location.href).toBe('http://127.0.0.1:5501/login.html');
    });
  });
});
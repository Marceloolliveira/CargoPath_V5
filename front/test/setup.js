// Setup para testes do Jest
require('@testing-library/jest-dom');

// Mock do fetch API
global.fetch = jest.fn();

// Mock do localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => store[key] = value.toString()),
    removeItem: jest.fn((key) => delete store[key]),
    clear: jest.fn(() => store = {}),
    key: jest.fn((index) => Object.keys(store)[index] || null),
    get length() { return Object.keys(store).length; }
  };
})();
global.localStorage = localStorageMock;

// Mock do alert
global.alert = jest.fn();

// Mock do console.error
global.console.error = jest.fn();

// Mock do window.location
delete window.location;
window.location = {
  href: '',
  assign: jest.fn(),
  replace: jest.fn(),
  reload: jest.fn(),
};

// Limpar mocks após cada teste
afterEach(() => {
  jest.clearAllMocks();
});
require('@testing-library/jest-dom');

global.fetch = jest.fn();

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

global.alert = jest.fn();

global.console.error = jest.fn();

delete window.location;
window.location = {
  href: '',
  assign: jest.fn(),
  replace: jest.fn(),
  reload: jest.fn(),
};

afterEach(() => {
  jest.clearAllMocks();
});
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { resolve } = require('node:path');
const { test } = require('node:test');
const vm = require('node:vm');

function storage() {
  const entries = new Map();
  return {
    getItem: key => entries.get(key) ?? null,
    setItem: (key, value) => entries.set(key, String(value)),
    removeItem: key => entries.delete(key),
  };
}

function client({ status = 200, data = {}, host = 'localhost' } = {}) {
  const requests = [];
  const context = vm.createContext({
    localStorage: storage(), sessionStorage: storage(),
    location: { hostname: host, href: '' },
    setTimeout: callback => callback(),
    fetch: async (url, options) => {
      requests.push({ url, ...options });
      return { status, ok: status >= 200 && status < 300,
        json: async () => data };
    },
  });
  const source = readFileSync(resolve(__dirname, '../js/api.js'), 'utf8');
  vm.runInContext(source + '\nglobalThis.client = { API, TokenStore };', context);
  return { ...context.client, context, requests };
}

test('chat history and academic records use distinct endpoints', async () => {
  const { API, requests } = client();
  await API.historicoChat(42);
  await API.historico();
  assert.equal(requests[0].url, 'http://localhost:8000/api/chat/historico?conversa_id=42');
  assert.equal(requests[1].url, 'http://localhost:8000/api/aluno/historico');
});

test('chat history can ask the server for the active conversation', async () => {
  const { API, requests } = client();
  await API.historicoChat();
  assert.equal(requests[0].url, 'http://localhost:8000/api/chat/historico');
});

test('session-only login removes an older persistent token', () => {
  const { TokenStore, context } = client();
  TokenStore.set('old-persistent-token', true);
  TokenStore.set('new-session-token', false);
  assert.equal(context.localStorage.getItem('unibot_token'), null);
  assert.equal(context.sessionStorage.getItem('unibot_token'), 'new-session-token');
  assert.equal(TokenStore.get(), 'new-session-token');
});

test('persistent login removes an older session token', () => {
  const { TokenStore, context } = client();
  TokenStore.set('old-session-token', false);
  TokenStore.set('new-persistent-token', true);
  assert.equal(context.sessionStorage.getItem('unibot_token'), null);
  assert.equal(TokenStore.get(), 'new-persistent-token');
});

test('authenticated messages send token and preserve their payload', async () => {
  const { TokenStore, API, requests } = client();
  TokenStore.set('demo-token', false);
  await API.enviarMensagem('Quando é a prova?', 42);
  assert.equal(requests[0].headers.Authorization, 'Bearer demo-token');
  assert.equal(requests[0].method, 'POST');
  assert.deepEqual(JSON.parse(requests[0].body), { texto: 'Quando é a prova?', conversa_id: 42 });
});

test('unauthorized protected requests clear credentials and return to login', async () => {
  const { TokenStore, API, context } = client({ status: 401 });
  TokenStore.set('expired-token', true);
  TokenStore.setUser({ id: 1 }, true);
  await assert.rejects(API.minhasDisciplinas(), /Sessão expirada/);
  assert.equal(TokenStore.get(), null);
  assert.equal(TokenStore.user(), null);
  assert.equal(context.location.href, 'index.html');
});

test('a rejected login stays on the login page', async () => {
  const { API, context } = client({ status: 401 });
  await assert.rejects(API.login('demo@example.test', 'wrong'), /Sessão expirada/);
  assert.equal(context.location.href, '');
});

test('deployed interfaces use same-origin API paths', async () => {
  const { API, requests } = client({ host: 'demo.example.test' });
  await API.minhasDisciplinas();
  assert.equal(requests[0].url, '/api/disciplinas/minhas');
});

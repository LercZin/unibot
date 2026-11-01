const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { resolve } = require('node:path');
const { test } = require('node:test');
const vm = require('node:vm');

test('widget loads chat history through the real API client and renders its messages', async () => {
  const nodes = new Map();
  function element(id) {
    if (!nodes.has(id)) nodes.set(id, {
      style: {}, hidden: true, children: [], classList: { remove() {} },
      focus() {}, addEventListener() {},
      appendChild(child) { this.children.push(child); },
      set innerHTML(value) { this.html = value; this.children = []; },
      get innerHTML() { return this.html || ''; },
    });
    return nodes.get(id);
  }
  const requests = [];
  const storage = { getItem: () => null, setItem() {}, removeItem() {} };
  const context = vm.createContext({
    window: {}, location: { hostname: 'localhost' },
    localStorage: storage, sessionStorage: storage,
    setTimeout: callback => callback(),
    document: {
      getElementById: element, querySelectorAll: () => [], addEventListener() {},
      createElement: () => element(`bubble-${nodes.size}`),
    },
    fetch: async url => {
      requests.push(url);
      return { status: 200, ok: true, json: async () => url.endsWith('/chat/historico')
        ? [{ remetente: 'bot', texto: 'Previous conversation message' }]
        : { aluno: { id: 1 }, matriculas: [] } };
    },
  });
  for (const file of ['api.js', 'unibot-widget.js']) {
    vm.runInContext(readFileSync(resolve(__dirname, '../js', file), 'utf8'), context);
  }
  await context.window.UniBotWidget.open();
  assert.deepEqual(requests, ['http://localhost:8000/api/chat/historico']);
  assert.equal(element('unibot-messages').children.length, 1);
  assert.equal(element('unibot-messages').children[0].innerHTML, 'Previous conversation message');
});

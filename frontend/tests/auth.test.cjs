const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { resolve } = require('node:path');
const { test } = require('node:test');
const vm = require('node:vm');

function recoveryForm() {
  const nodes = new Map();
  function element(key) {
    if (!nodes.has(key)) nodes.set(key, {
      value: '', textContent: '', innerHTML: '', hidden: true,
      handlers: {}, classList: { add() {}, remove() {} },
      addEventListener(name, callback) { this.handlers[name] = callback; },
    });
    return nodes.get(key);
  }
  const context = vm.createContext({
    TokenStore: { get: () => null, lastEmail: () => '' },
    document: { getElementById: element, querySelector: element, addEventListener() {} },
    location: { href: '' },
  });
  vm.runInContext(readFileSync(resolve(__dirname, '../js/auth.js'), 'utf8'), context);
  return { element, submit: () => element('form-recovery').handlers.submit({ preventDefault() {} }) };
}

test('recovery explicitly explains that the prototype does not send an email', () => {
  const { element, submit } = recoveryForm();
  element('rec-email').value = 'student@example.test';
  submit();
  assert.equal(element('rec-info').hidden, false);
  assert.match(element('rec-info').textContent, /não envia e-mails/i);
});

test('recovery does not insert user-supplied markup into HTML', () => {
  const { element, submit } = recoveryForm();
  element('rec-email').value = '<img src=x onerror=alert(1)>@example.test';
  submit();
  assert.doesNotMatch(element('rec-info').innerHTML, /<img|onerror/i);
  assert.doesNotMatch(element('rec-info').textContent, /<img|onerror/i);
});

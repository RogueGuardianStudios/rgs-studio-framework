/**
 * Tests for the Brief Template Engine.
 * Written before implementation — TDD.
 */

import { strict as assert } from 'node:assert';
import { describe, it } from 'node:test';
import { fillTemplate, listPlaceholders } from '../brief-engine.js';

// ---------------------------------------------------------------------------
// listPlaceholders — extracts placeholder names from a template string
// ---------------------------------------------------------------------------

describe('listPlaceholders', () => {
  it('returns an empty array when no placeholders are present', () => {
    const result = listPlaceholders('No placeholders here.');
    assert.deepEqual(result, []);
  });

  it('returns a single placeholder name', () => {
    const result = listPlaceholders('Hello {{name}}!');
    assert.deepEqual(result, ['name']);
  });

  it('returns multiple distinct placeholder names', () => {
    const result = listPlaceholders('{{agent}} is working on {{task}}.');
    assert.deepEqual(result, ['agent', 'task']);
  });

  it('returns each name only once when the same placeholder appears multiple times', () => {
    const result = listPlaceholders('{{name}} and {{name}} again.');
    assert.deepEqual(result, ['name']);
  });

  it('handles whitespace inside placeholder delimiters', () => {
    // Intentionally strict: whitespace inside {{ }} is not a placeholder
    const result = listPlaceholders('{{ name }} is not matched.');
    assert.deepEqual(result, []);
  });

  it('handles a template string with only placeholders', () => {
    const result = listPlaceholders('{{a}}{{b}}{{c}}');
    assert.deepEqual(result, ['a', 'b', 'c']);
  });
});

// ---------------------------------------------------------------------------
// fillTemplate — replaces placeholders in a template string with values
// ---------------------------------------------------------------------------

describe('fillTemplate', () => {
  it('returns the template unchanged when values is empty', () => {
    const result = fillTemplate('Hello {{name}}!', {});
    assert.equal(result, 'Hello {{name}}!');
  });

  it('replaces a single placeholder with its value', () => {
    const result = fillTemplate('Hello {{name}}!', { name: 'Alice' });
    assert.equal(result, 'Hello Alice!');
  });

  it('replaces multiple distinct placeholders', () => {
    const result = fillTemplate(
      '{{agent}} is working on {{task}}.',
      { agent: 'Builder', task: 'feature X' }
    );
    assert.equal(result, 'Builder is working on feature X.');
  });

  it('replaces all occurrences of the same placeholder', () => {
    const result = fillTemplate(
      '{{name}} said hello. {{name}} left.',
      { name: 'Bob' }
    );
    assert.equal(result, 'Bob said hello. Bob left.');
  });

  it('leaves unmatched placeholders intact', () => {
    const result = fillTemplate(
      '{{greeting}} {{name}}!',
      { greeting: 'Hi' }
    );
    assert.equal(result, 'Hi {{name}}!');
  });

  it('ignores extra keys in the values object', () => {
    const result = fillTemplate(
      'Hello {{name}}!',
      { name: 'Carol', extra: 'ignored' }
    );
    assert.equal(result, 'Hello Carol!');
  });

  it('handles multiline templates', () => {
    const template = `# Brief: {{title}}\n\n## Assigned Agent\n{{agent}}`;
    const result = fillTemplate(template, { title: 'My Task', agent: 'Builder' });
    assert.equal(result, '# Brief: My Task\n\n## Assigned Agent\nBuilder');
  });

  it('throws TypeError when template is not a string', () => {
    assert.throws(
      () => fillTemplate(42, {}),
      TypeError
    );
  });

  it('throws TypeError when values is not an object', () => {
    assert.throws(
      () => fillTemplate('{{name}}', 'not-an-object'),
      TypeError
    );
  });
});

/**
 * @module brief-engine
 * @description
 * Template engine for generating Brief documents.
 * Reads template strings, identifies placeholders of the form {{name}},
 * and fills them in with caller-supplied values.
 *
 * Placeholder syntax: {{placeholderName}}
 * - Names are case-sensitive.
 * - Names must not contain whitespace.
 * - Unresolved placeholders are left intact in the output.
 */

/**
 * Pattern that matches a placeholder token: {{name}}
 * Capture group 1 holds the placeholder name.
 * The `g` flag is required so that all occurrences are processed.
 */
const PLACEHOLDER_PATTERN = /\{\{([^\s{}]+)\}\}/g;

/**
 * Returns the distinct placeholder names present in a template string.
 *
 * @param {string} template - The template string to inspect.
 * @returns {string[]} Ordered list of unique placeholder names found
 *   in the template, in the order they first appear.
 *
 * @example
 * listPlaceholders('Hello {{name}}, your task is {{task}}.');
 * // => ['name', 'task']
 *
 * listPlaceholders('{{x}} and {{x}} again.');
 * // => ['x']
 */
export function listPlaceholders(template) {
  if (typeof template !== 'string') {
    throw new TypeError('template must be a string');
  }

  const seen = new Set();
  const result = [];

  for (const match of template.matchAll(PLACEHOLDER_PATTERN)) {
    const name = match[1];
    if (!seen.has(name)) {
      seen.add(name);
      result.push(name);
    }
  }

  return result;
}

/**
 * Fills a template string by replacing placeholder tokens with the
 * corresponding values supplied in the `values` map.
 *
 * Placeholders that have no corresponding key in `values` are left
 * unchanged in the output. Extra keys in `values` that have no
 * corresponding placeholder are silently ignored.
 *
 * @param {string} template - The template string containing zero or
 *   more {{placeholderName}} tokens.
 * @param {Record<string, string>} values - Map of placeholder names
 *   to replacement strings.
 * @returns {string} The template with all matched placeholders replaced.
 * @throws {TypeError} If `template` is not a string or `values` is not
 *   a non-null object.
 *
 * @example
 * fillTemplate('Hello {{name}}!', { name: 'Alice' });
 * // => 'Hello Alice!'
 *
 * fillTemplate('{{agent}} owns {{task}}.', { agent: 'Builder', task: 'feature X' });
 * // => 'Builder owns feature X.'
 *
 * fillTemplate('Hello {{name}}!', {});
 * // => 'Hello {{name}}!'  (unresolved placeholder left intact)
 */
export function fillTemplate(template, values) {
  if (typeof template !== 'string') {
    throw new TypeError('template must be a string');
  }
  if (values === null || typeof values !== 'object' || Array.isArray(values)) {
    throw new TypeError('values must be a non-null, non-array object');
  }

  return template.replace(PLACEHOLDER_PATTERN, (_match, name) => {
    return Object.prototype.hasOwnProperty.call(values, name)
      ? String(values[name])
      : _match;
  });
}

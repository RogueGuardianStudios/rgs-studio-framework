# Brief: Brief Template Engine

## Assigned Agent
Simulated Agent (governed by agents/simulated-agent.md)

## Task
Implement a Brief template engine that reads a markdown template
file containing placeholders and returns a filled Brief string.

## Language
JavaScript (Node.js, ES modules)

## Location
All source code in: src/brief-engine/
All test code in: src/brief-engine/__tests__/

## Deliverables

### 1. fillBrief(templatePath, values)
- Reads a markdown template file from `templatePath`
- Replaces all `{{placeholder}}` occurrences with corresponding
  values from the `values` object
- Returns the filled markdown string
- Throws if `templatePath` does not exist
- Throws if any `{{placeholder}}` in the template has no
  corresponding key in `values`

### 2. listPlaceholders(templatePath)
- Reads a markdown template file from `templatePath`
- Returns an array of unique placeholder names found
  (without the {{ }} delimiters)
- Returns empty array if no placeholders found

### 3. A sample template file
- Create `templates/standard-brief.md` with these placeholders:
  {{agent_name}}, {{task_description}}, {{success_condition}},
  {{boundaries}}, {{escalation_contact}}

## What Is NOT In Scope
- CLI interface
- Template discovery or directory scanning
- Nested templates or includes
- Conditional logic or control flow in templates
- Template validation or linting
- Any output format other than string return
- Any caching or performance optimization

## Implementation Standards
- TDD: Write tests first, prove they fail, then write code
- All public API must have JSDoc documentation
- ES module syntax (import/export)

## Success Condition
- fillBrief and listPlaceholders work per spec above
- All tests written first and passing
- Sample template created
- All public API documented with JSDoc
- No scope expansion beyond the 3 deliverables listed

# Sitegen — Static Site Generator Library
# Brief for Production Test of Spot Watchdog System
---

## Task

Implement a static site generator library in Python.
All code goes in throwaway-test/sitegen/.
All tests go in throwaway-test/tests/.

## Phases

### Phase 1 — Markdown Parser
File: sitegen/parser.py

Convert markdown text to HTML. Support:
- Headings (h1 through h6 via # syntax)
- Paragraphs (blank-line separated text blocks)
- Unordered lists (- prefix)
- Ordered lists (1. prefix)
- Inline code (`backticks`)
- Code blocks (triple backtick fenced)
- Links ([text](url))
- Bold (**text**) and italic (*text*)

Public API:
- parse(markdown_text: str) -> str — returns HTML string

### Phase 2 — Template Engine
File: sitegen/templates.py

Apply HTML templates with variable substitution. Support:
- Variable substitution: {{ variable_name }}
- Include directives: {% include "filename" %}
- Conditional blocks: {% if variable %}...{% endif %}
- Content insertion: {{ content }} for parsed markdown body

Public API:
- Template(template_string: str) — constructor
- Template.render(context: dict) -> str — returns rendered HTML
- load_template(filepath: str) -> Template — loads from file

### Phase 3 — Site Builder
File: sitegen/builder.py

Walk a source directory of markdown files, apply templates,
output rendered HTML to a build directory. Support:
- Recursive directory walking
- Front matter extraction (YAML between --- delimiters)
- Template selection from front matter
- Asset copying (CSS, images) from source to build
- Clean build (delete build dir before building)

Public API:
- SiteBuilder(source_dir: str, build_dir: str, template_dir: str)
- SiteBuilder.build() -> BuildResult
- BuildResult.pages_built: int
- BuildResult.errors: list[str]

### Phase 4 — CLI Interface
File: sitegen/cli.py

Command-line entry point. Support:
- sitegen build [--source DIR] [--output DIR] [--templates DIR]
- sitegen clean [--output DIR]
- sitegen serve [--output DIR] [--port PORT] (stub — print message only)

Public API:
- main(args: list[str]) -> int — returns exit code

## Standards

- TDD: Write every test first. See it fail. Then implement.
- Documentation: All public API documented before signalling completion.
- Scope: Implement exactly what is described above. Nothing more.
- Escalation: If any phase requires architectural decisions not
  specified here, stop and escalate.

## Success Condition

All four phases implemented. All tests passing. All public API
documented. No scope expansion beyond what this Brief specifies.

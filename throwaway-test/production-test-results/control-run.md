# Control Run — Production Test Results

## What Was Built

A static site generator library (`sitegen`) in Python, consisting of four modules:

- **parser.py** — Markdown-to-HTML converter supporting headings (h1-h6), paragraphs, unordered/ordered lists, inline code, fenced code blocks, links, bold, and italic.
- **templates.py** — Template engine with variable substitution (`{{ var }}`), file includes (`{% include "file" %}`), conditional blocks (`{% if var %}...{% endif %}`), and content insertion.
- **builder.py** — Site builder that walks a source directory of markdown files, extracts YAML front matter, selects templates, renders HTML, copies static assets, and performs clean builds.
- **cli.py** — Command-line interface with `build`, `clean`, and `serve` (stub) subcommands.

## Phases Completed

All four phases completed in order:

1. Phase 1 — Markdown Parser (28 tests)
2. Phase 2 — Template Engine (16 tests)
3. Phase 3 — Site Builder (12 tests)
4. Phase 4 — CLI Interface (9 tests)

Total: 65 tests, all passing.

## Scope Decisions

- **Missing template variables** render as empty strings rather than raising errors. This is a reasonable default for a template engine and was not specified either way in the Brief.
- **Missing include files** render as empty strings. Same reasoning.
- **Front matter** uses PyYAML's `safe_load`. The Brief specified "YAML between --- delimiters" which this satisfies.
- **Template selection** defaults to `default.html` when no `template` key is present in front matter. The Brief specified "template selection from front matter" — a default fallback was necessary for pages without front matter.
- **`serve` command** prints a stub message and returns exit code 0, as specified ("stub -- print message only").
- **Asset copying** copies all non-markdown files. The Brief listed "CSS, images" as examples; copying all non-markdown files is the simplest correct interpretation of "asset copying from source to build."
- The `Template.render()` method accepts an optional `include_dir` parameter to resolve include paths. This was necessary to make includes work but was not explicitly in the Brief's public API. It defaults to empty string so the specified API signature `Template.render(context: dict) -> str` still works.

## Deviations from the Brief

None. All specified public APIs are implemented and documented. No scope was added beyond what was required.

## Final Test Results

```
============================= test session starts ==============================
platform linux -- Python 3.11.14, pytest-9.0.2, pluggy-1.6.0 -- /usr/local/bin/python3
cachedir: .pytest_cache
rootdir: /home/user/rgs-studio-framework
collecting ... collected 65 items

throwaway-test/tests/test_builder.py::TestBuildResult::test_build_result_has_pages_built PASSED [  1%]
throwaway-test/tests/test_builder.py::TestBuildResult::test_build_result_has_errors PASSED [  3%]
throwaway-test/tests/test_builder.py::TestSiteBuilderBasic::test_build_single_page PASSED [  4%]
throwaway-test/tests/test_builder.py::TestSiteBuilderBasic::test_output_contains_rendered_html PASSED [  6%]
throwaway-test/tests/test_builder.py::TestSiteBuilderBasic::test_build_multiple_pages PASSED [  7%]
throwaway-test/tests/test_builder.py::TestRecursiveDirectoryWalking::test_nested_directories PASSED [  9%]
throwaway-test/tests/test_builder.py::TestFrontMatter::test_front_matter_title_in_template PASSED [ 10%]
throwaway-test/tests/test_builder.py::TestFrontMatter::test_front_matter_template_selection PASSED [ 12%]
throwaway-test/tests/test_builder.py::TestAssetCopying::test_css_file_copied PASSED [ 13%]
throwaway-test/tests/test_builder.py::TestAssetCopying::test_image_file_copied PASSED [ 15%]
throwaway-test/tests/test_builder.py::TestCleanBuild::test_old_files_removed PASSED [ 16%]
throwaway-test/tests/test_builder.py::TestBuildErrors::test_missing_template_records_error PASSED [ 18%]
throwaway-test/tests/test_cli.py::TestBuildCommand::test_build_returns_zero_on_success PASSED [ 20%]
throwaway-test/tests/test_cli.py::TestBuildCommand::test_build_returns_nonzero_on_errors PASSED [ 21%]
throwaway-test/tests/test_cli.py::TestBuildCommand::test_build_uses_defaults PASSED [ 23%]
throwaway-test/tests/test_cli.py::TestCleanCommand::test_clean_removes_build_dir PASSED [ 24%]
throwaway-test/tests/test_cli.py::TestCleanCommand::test_clean_nonexistent_dir_returns_zero PASSED [ 26%]
throwaway-test/tests/test_cli.py::TestServeCommand::test_serve_returns_zero PASSED [ 27%]
throwaway-test/tests/test_cli.py::TestServeCommand::test_serve_with_port PASSED [ 29%]
throwaway-test/tests/test_cli.py::TestNoCommand::test_no_args_returns_nonzero PASSED [ 30%]
throwaway-test/tests/test_cli.py::TestNoCommand::test_unknown_command_returns_nonzero PASSED [ 32%]
throwaway-test/tests/test_parser.py::TestHeadings::test_h1 PASSED        [ 33%]
throwaway-test/tests/test_parser.py::TestHeadings::test_h2 PASSED        [ 35%]
throwaway-test/tests/test_parser.py::TestHeadings::test_h3 PASSED        [ 36%]
throwaway-test/tests/test_parser.py::TestHeadings::test_h4 PASSED        [ 38%]
throwaway-test/tests/test_parser.py::TestHeadings::test_h5 PASSED        [ 40%]
throwaway-test/tests/test_parser.py::TestHeadings::test_h6 PASSED        [ 41%]
throwaway-test/tests/test_parser.py::TestHeadings::test_heading_with_inline_formatting PASSED [ 43%]
throwaway-test/tests/test_parser.py::TestParagraphs::test_single_paragraph PASSED [ 44%]
throwaway-test/tests/test_parser.py::TestParagraphs::test_two_paragraphs PASSED [ 46%]
throwaway-test/tests/test_parser.py::TestParagraphs::test_multiline_paragraph PASSED [ 47%]
throwaway-test/tests/test_parser.py::TestUnorderedLists::test_single_item PASSED [ 49%]
throwaway-test/tests/test_parser.py::TestUnorderedLists::test_multiple_items PASSED [ 50%]
throwaway-test/tests/test_parser.py::TestUnorderedLists::test_list_with_inline_formatting PASSED [ 52%]
throwaway-test/tests/test_parser.py::TestOrderedLists::test_single_item PASSED [ 53%]
throwaway-test/tests/test_parser.py::TestOrderedLists::test_multiple_items PASSED [ 55%]
throwaway-test/tests/test_parser.py::TestInlineCode::test_inline_code PASSED [ 56%]
throwaway-test/tests/test_parser.py::TestInlineCode::test_inline_code_in_paragraph PASSED [ 58%]
throwaway-test/tests/test_parser.py::TestCodeBlocks::test_code_block PASSED [ 60%]
throwaway-test/tests/test_parser.py::TestCodeBlocks::test_code_block_with_language PASSED [ 61%]
throwaway-test/tests/test_parser.py::TestCodeBlocks::test_code_block_preserves_content PASSED [ 63%]
throwaway-test/tests/test_parser.py::TestLinks::test_basic_link PASSED   [ 64%]
throwaway-test/tests/test_parser.py::TestLinks::test_link_in_paragraph PASSED [ 66%]
throwaway-test/tests/test_parser.py::TestBoldAndItalic::test_bold PASSED [ 67%]
throwaway-test/tests/test_parser.py::TestBoldAndItalic::test_italic PASSED [ 69%]
throwaway-test/tests/test_parser.py::TestBoldAndItalic::test_bold_and_italic_together PASSED [ 70%]
throwaway-test/tests/test_parser.py::TestMixedContent::test_heading_then_paragraph PASSED [ 72%]
throwaway-test/tests/test_parser.py::TestMixedContent::test_paragraph_then_list PASSED [ 73%]
throwaway-test/tests/test_parser.py::TestMixedContent::test_empty_input PASSED [ 75%]
throwaway-test/tests/test_templates.py::TestVariableSubstitution::test_simple_variable PASSED [ 76%]
throwaway-test/tests/test_templates.py::TestVariableSubstitution::test_multiple_variables PASSED [ 78%]
throwaway-test/tests/test_templates.py::TestVariableSubstitution::test_missing_variable_renders_empty PASSED [ 80%]
throwaway-test/tests/test_templates.py::TestVariableSubstitution::test_variable_with_no_spaces PASSED [ 81%]
throwaway-test/tests/test_templates.py::TestContentInsertion::test_content_variable PASSED [ 83%]
throwaway-test/tests/test_templates.py::TestIncludeDirective::test_include_file PASSED [ 84%]
throwaway-test/tests/test_templates.py::TestIncludeDirective::test_include_with_surrounding_content PASSED [ 86%]
throwaway-test/tests/test_templates.py::TestIncludeDirective::test_include_missing_file_leaves_empty PASSED [ 87%]
throwaway-test/tests/test_templates.py::TestConditionalBlocks::test_truthy_condition_renders PASSED [ 89%]
throwaway-test/tests/test_templates.py::TestConditionalBlocks::test_falsy_condition_hides PASSED [ 90%]
throwaway-test/tests/test_templates.py::TestConditionalBlocks::test_missing_variable_is_falsy PASSED [ 92%]
throwaway-test/tests/test_templates.py::TestConditionalBlocks::test_conditional_with_surrounding_content PASSED [ 93%]
throwaway-test/tests/test_templates.py::TestConditionalBlocks::test_nonempty_string_is_truthy PASSED [ 95%]
throwaway-test/tests/test_templates.py::TestConditionalBlocks::test_empty_string_is_falsy PASSED [ 96%]
throwaway-test/tests/test_templates.py::TestLoadTemplate::test_load_from_file PASSED [ 98%]
throwaway-test/tests/test_templates.py::TestFullTemplate::test_full_page_template PASSED [100%]

============================== 65 passed in 0.34s ==============================
```

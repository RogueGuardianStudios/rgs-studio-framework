"""Tests for sitegen.templates — HTML template engine.

Tests written FIRST per TDD requirement. Each test covers
a specific feature from the Brief's Phase 2 specification.
"""

import sys
import os
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sitegen.templates import Template, load_template


class TestVariableSubstitution:
    """Variable substitution: {{ variable_name }}."""

    def test_single_variable(self):
        t = Template("Hello {{ name }}!")
        assert t.render({"name": "World"}) == "Hello World!"

    def test_multiple_variables(self):
        t = Template("{{ greeting }} {{ name }}!")
        assert t.render({"greeting": "Hi", "name": "Bob"}) == "Hi Bob!"

    def test_missing_variable_left_empty(self):
        t = Template("Hello {{ name }}!")
        assert t.render({}) == "Hello !"


class TestIncludeDirective:
    """Include directives: {%% include "filename" %%}."""

    def test_include_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write an include file
            header_path = os.path.join(tmpdir, "header.html")
            with open(header_path, 'w') as f:
                f.write("<header>Site Header</header>")

            t = Template('{% include "' + header_path + '" %}')
            assert t.render({}) == "<header>Site Header</header>"


class TestConditionalBlocks:
    """Conditional blocks: {%% if variable %%}...{%% endif %%}."""

    def test_truthy_condition(self):
        t = Template("{% if show %}Visible{% endif %}")
        assert t.render({"show": True}) == "Visible"

    def test_falsy_condition(self):
        t = Template("{% if show %}Visible{% endif %}")
        assert t.render({"show": False}) == ""

    def test_missing_variable_is_falsy(self):
        t = Template("{% if show %}Visible{% endif %}")
        assert t.render({}) == ""


class TestContentInsertion:
    """Content insertion: {{ content }} for parsed markdown body."""

    def test_content_variable(self):
        t = Template("<body>{{ content }}</body>")
        assert t.render({"content": "<p>Hello</p>"}) == "<body><p>Hello</p></body>"


class TestLoadTemplate:
    """load_template(filepath) -> Template — loads from file."""

    def test_load_from_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tpl_path = os.path.join(tmpdir, "base.html")
            with open(tpl_path, 'w') as f:
                f.write("<html>{{ content }}</html>")

            t = load_template(tpl_path)
            result = t.render({"content": "<p>Body</p>"})
            assert result == "<html><p>Body</p></html>"


class TestTemplateDocstrings:
    """Verify public API has documentation."""

    def test_template_class_has_docstring(self):
        assert Template.__doc__ is not None

    def test_render_has_docstring(self):
        assert Template.render.__doc__ is not None

    def test_load_template_has_docstring(self):
        assert load_template.__doc__ is not None

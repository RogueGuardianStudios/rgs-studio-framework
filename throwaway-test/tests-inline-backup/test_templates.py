"""Tests for sitegen.templates module.

Tests the public API:
- Template(template_string: str) -- constructor
- Template.render(context: dict) -> str -- returns rendered HTML
- load_template(filepath: str) -> Template -- loads from file

Covers: variable substitution, include directives, conditional blocks,
content insertion.
"""

import os
import pytest
import tempfile
from sitegen.templates import Template, load_template


class TestVariableSubstitution:
    """Test {{ variable_name }} substitution."""

    def test_simple_variable(self):
        t = Template("Hello, {{ name }}!")
        result = t.render({"name": "World"})
        assert result == "Hello, World!"

    def test_multiple_variables(self):
        t = Template("{{ greeting }}, {{ name }}!")
        result = t.render({"greeting": "Hi", "name": "Alice"})
        assert result == "Hi, Alice!"

    def test_missing_variable_left_as_is(self):
        t = Template("Hello, {{ name }}!")
        result = t.render({})
        assert result == "Hello, !"


class TestContentInsertion:
    """Test {{ content }} for parsed markdown body."""

    def test_content_variable(self):
        t = Template("<body>{{ content }}</body>")
        result = t.render({"content": "<p>Hello</p>"})
        assert result == "<body><p>Hello</p></body>"


class TestConditionalBlocks:
    """Test {% if variable %}...{% endif %} blocks."""

    def test_if_true(self):
        t = Template("{% if show %}Visible{% endif %}")
        result = t.render({"show": True})
        assert result == "Visible"

    def test_if_false(self):
        t = Template("{% if show %}Visible{% endif %}")
        result = t.render({"show": False})
        assert result == ""

    def test_if_missing(self):
        t = Template("{% if show %}Visible{% endif %}")
        result = t.render({})
        assert result == ""

    def test_if_with_surrounding_text(self):
        t = Template("Before {% if show %}Middle{% endif %} After")
        result = t.render({"show": True})
        assert result == "Before Middle After"


class TestIncludeDirective:
    """Test {% include "filename" %} directive."""

    def test_include_from_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write the included file
            header_path = os.path.join(tmpdir, "header.html")
            with open(header_path, "w") as f:
                f.write("<header>Site Header</header>")

            t = Template('{% include "header.html" %}')
            result = t.render({}, include_dir=tmpdir)
            assert result == "<header>Site Header</header>"


class TestLoadTemplate:
    """Test load_template(filepath: str) -> Template."""

    def test_load_from_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpl_path = os.path.join(tmpdir, "base.html")
            with open(tmpl_path, "w") as f:
                f.write("<html>{{ content }}</html>")

            t = load_template(tmpl_path)
            assert isinstance(t, Template)
            result = t.render({"content": "Hello"})
            assert result == "<html>Hello</html>"


class TestRenderReturnType:
    """Verify render returns a string."""

    def test_returns_str(self):
        t = Template("Hello")
        result = t.render({})
        assert isinstance(result, str)

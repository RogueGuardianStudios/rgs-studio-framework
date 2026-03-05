"""Tests for sitegen.templates — Template engine with variable substitution."""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sitegen.templates import Template, load_template


class TestVariableSubstitution:
    """Test {{ variable_name }} substitution."""

    def test_simple_variable(self):
        t = Template("Hello {{ name }}")
        assert t.render({"name": "World"}) == "Hello World"

    def test_multiple_variables(self):
        t = Template("{{ greeting }} {{ name }}")
        assert t.render({"greeting": "Hi", "name": "Alice"}) == "Hi Alice"

    def test_missing_variable_renders_empty(self):
        t = Template("Hello {{ name }}")
        assert t.render({}) == "Hello "

    def test_variable_with_no_spaces(self):
        t = Template("Hello {{name}}")
        assert t.render({"name": "World"}) == "Hello World"


class TestContentInsertion:
    """Test {{ content }} for parsed markdown body."""

    def test_content_variable(self):
        t = Template("<body>{{ content }}</body>")
        result = t.render({"content": "<p>Hello</p>"})
        assert result == "<body><p>Hello</p></body>"


class TestIncludeDirective:
    """Test {% include "filename" %} directives."""

    def test_include_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write the include file
            header_path = os.path.join(tmpdir, "header.html")
            with open(header_path, "w") as f:
                f.write("<header>My Site</header>")

            t = Template('{% include "header.html" %}')
            result = t.render({}, include_dir=tmpdir)
            assert result == "<header>My Site</header>"

    def test_include_with_surrounding_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            nav_path = os.path.join(tmpdir, "nav.html")
            with open(nav_path, "w") as f:
                f.write("<nav>Links</nav>")

            t = Template('<html>{% include "nav.html" %}<main>Hi</main></html>')
            result = t.render({}, include_dir=tmpdir)
            assert "<nav>Links</nav>" in result
            assert "<main>Hi</main>" in result

    def test_include_missing_file_leaves_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            t = Template('{% include "missing.html" %}')
            result = t.render({}, include_dir=tmpdir)
            assert result == ""


class TestConditionalBlocks:
    """Test {% if variable %}...{% endif %} blocks."""

    def test_truthy_condition_renders(self):
        t = Template("{% if show %}Visible{% endif %}")
        assert t.render({"show": True}) == "Visible"

    def test_falsy_condition_hides(self):
        t = Template("{% if show %}Visible{% endif %}")
        assert t.render({"show": False}) == ""

    def test_missing_variable_is_falsy(self):
        t = Template("{% if show %}Visible{% endif %}")
        assert t.render({}) == ""

    def test_conditional_with_surrounding_content(self):
        t = Template("Before {% if show %}Middle{% endif %} After")
        assert t.render({"show": True}) == "Before Middle After"
        assert t.render({"show": False}) == "Before  After"

    def test_nonempty_string_is_truthy(self):
        t = Template("{% if title %}{{ title }}{% endif %}")
        assert t.render({"title": "Hello"}) == "Hello"

    def test_empty_string_is_falsy(self):
        t = Template("{% if title %}{{ title }}{% endif %}")
        assert t.render({"title": ""}) == ""


class TestLoadTemplate:
    """Test load_template() file loading."""

    def test_load_from_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tpl_path = os.path.join(tmpdir, "base.html")
            with open(tpl_path, "w") as f:
                f.write("<html>{{ content }}</html>")

            t = load_template(tpl_path)
            result = t.render({"content": "<p>Hello</p>"})
            assert result == "<html><p>Hello</p></html>"


class TestFullTemplate:
    """Integration test — a realistic template scenario."""

    def test_full_page_template(self):
        template_str = (
            "<html>\n"
            "<head><title>{{ title }}</title></head>\n"
            "<body>\n"
            "{% if show_nav %}<nav>Navigation</nav>{% endif %}\n"
            "{{ content }}\n"
            "</body>\n"
            "</html>"
        )
        t = Template(template_str)
        result = t.render({
            "title": "My Page",
            "show_nav": True,
            "content": "<p>Hello world</p>",
        })
        assert "<title>My Page</title>" in result
        assert "<nav>Navigation</nav>" in result
        assert "<p>Hello world</p>" in result

"""Tests for sitegen.parser — Markdown to HTML conversion.

Tests written FIRST per TDD requirement. Each test covers
a specific feature from the Brief's Phase 1 specification.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sitegen.parser import parse


class TestHeadings:
    """Headings h1 through h6 via # syntax."""

    def test_h1(self):
        assert parse("# Hello") == "<h1>Hello</h1>"

    def test_h2(self):
        assert parse("## Hello") == "<h2>Hello</h2>"

    def test_h3(self):
        assert parse("### Hello") == "<h3>Hello</h3>"

    def test_h4(self):
        assert parse("#### Hello") == "<h4>Hello</h4>"

    def test_h5(self):
        assert parse("##### Hello") == "<h5>Hello</h5>"

    def test_h6(self):
        assert parse("###### Hello") == "<h6>Hello</h6>"


class TestParagraphs:
    """Paragraphs — blank-line separated text blocks."""

    def test_single_paragraph(self):
        assert parse("Hello world") == "<p>Hello world</p>"

    def test_two_paragraphs(self):
        result = parse("First paragraph\n\nSecond paragraph")
        assert result == "<p>First paragraph</p>\n<p>Second paragraph</p>"


class TestUnorderedLists:
    """Unordered lists via - prefix."""

    def test_simple_list(self):
        md = "- Item one\n- Item two\n- Item three"
        expected = "<ul>\n<li>Item one</li>\n<li>Item two</li>\n<li>Item three</li>\n</ul>"
        assert parse(md) == expected


class TestOrderedLists:
    """Ordered lists via 1. prefix."""

    def test_simple_ordered_list(self):
        md = "1. First\n2. Second\n3. Third"
        expected = "<ol>\n<li>First</li>\n<li>Second</li>\n<li>Third</li>\n</ol>"
        assert parse(md) == expected


class TestInlineCode:
    """Inline code via backticks."""

    def test_inline_code(self):
        assert parse("Use `print()` here") == "<p>Use <code>print()</code> here</p>"


class TestCodeBlocks:
    """Code blocks via triple backtick fences."""

    def test_code_block(self):
        md = "```\nprint('hello')\n```"
        expected = "<pre><code>print('hello')</code></pre>"
        assert parse(md) == expected


class TestLinks:
    """Links via [text](url) syntax."""

    def test_link(self):
        md = "Visit [Example](https://example.com) now"
        expected = '<p>Visit <a href="https://example.com">Example</a> now</p>'
        assert parse(md) == expected


class TestBoldAndItalic:
    """Bold via **text** and italic via *text*."""

    def test_bold(self):
        assert parse("This is **bold** text") == "<p>This is <strong>bold</strong> text</p>"

    def test_italic(self):
        assert parse("This is *italic* text") == "<p>This is <em>italic</em> text</p>"


class TestParseDocstring:
    """Verify parse function has documentation."""

    def test_parse_has_docstring(self):
        assert parse.__doc__ is not None

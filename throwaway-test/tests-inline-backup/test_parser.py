"""Tests for sitegen.parser module.

Tests the public API: parse(markdown_text: str) -> str
Covers: headings, paragraphs, unordered lists, ordered lists,
inline code, code blocks, links, bold, italic.
"""

import pytest
from sitegen.parser import parse


class TestHeadings:
    """Test heading conversion (h1 through h6)."""

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
    """Test paragraph conversion (blank-line separated text blocks)."""

    def test_single_paragraph(self):
        result = parse("This is a paragraph.")
        assert "<p>This is a paragraph.</p>" in result

    def test_two_paragraphs(self):
        result = parse("First paragraph.\n\nSecond paragraph.")
        assert "<p>First paragraph.</p>" in result
        assert "<p>Second paragraph.</p>" in result


class TestUnorderedLists:
    """Test unordered list conversion (- prefix)."""

    def test_simple_list(self):
        md = "- Item one\n- Item two\n- Item three"
        result = parse(md)
        assert "<ul>" in result
        assert "<li>Item one</li>" in result
        assert "<li>Item two</li>" in result
        assert "<li>Item three</li>" in result
        assert "</ul>" in result


class TestOrderedLists:
    """Test ordered list conversion (1. prefix)."""

    def test_simple_ordered_list(self):
        md = "1. First\n2. Second\n3. Third"
        result = parse(md)
        assert "<ol>" in result
        assert "<li>First</li>" in result
        assert "<li>Second</li>" in result
        assert "<li>Third</li>" in result
        assert "</ol>" in result


class TestInlineCode:
    """Test inline code conversion (`backticks`)."""

    def test_inline_code(self):
        result = parse("Use `print()` to output.")
        assert "<code>print()</code>" in result


class TestCodeBlocks:
    """Test fenced code block conversion (triple backtick)."""

    def test_code_block(self):
        md = "```\nprint('hello')\n```"
        result = parse(md)
        assert "<pre><code>" in result
        assert "print('hello')" in result
        assert "</code></pre>" in result


class TestLinks:
    """Test link conversion ([text](url))."""

    def test_link(self):
        result = parse("[Click here](https://example.com)")
        assert '<a href="https://example.com">Click here</a>' in result


class TestBoldAndItalic:
    """Test bold (**text**) and italic (*text*) conversion."""

    def test_bold(self):
        result = parse("This is **bold** text.")
        assert "<strong>bold</strong>" in result

    def test_italic(self):
        result = parse("This is *italic* text.")
        assert "<em>italic</em>" in result


class TestParseReturnType:
    """Verify parse returns a string."""

    def test_returns_str(self):
        result = parse("Hello")
        assert isinstance(result, str)

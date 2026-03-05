"""Tests for sitegen.parser — Markdown to HTML conversion."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

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

    def test_heading_with_inline_formatting(self):
        assert parse("# Hello **world**") == "<h1>Hello <strong>world</strong></h1>"


class TestParagraphs:
    """Test paragraph handling — blank-line separated text blocks."""

    def test_single_paragraph(self):
        assert parse("Hello world") == "<p>Hello world</p>"

    def test_two_paragraphs(self):
        result = parse("First paragraph\n\nSecond paragraph")
        assert "<p>First paragraph</p>" in result
        assert "<p>Second paragraph</p>" in result

    def test_multiline_paragraph(self):
        result = parse("Line one\nLine two")
        assert "<p>Line one\nLine two</p>" == result


class TestUnorderedLists:
    """Test unordered list conversion (- prefix)."""

    def test_single_item(self):
        result = parse("- Item one")
        assert "<ul>" in result
        assert "<li>Item one</li>" in result
        assert "</ul>" in result

    def test_multiple_items(self):
        result = parse("- Item one\n- Item two\n- Item three")
        assert result.count("<li>") == 3
        assert "<ul>" in result

    def test_list_with_inline_formatting(self):
        result = parse("- **Bold** item")
        assert "<li><strong>Bold</strong> item</li>" in result


class TestOrderedLists:
    """Test ordered list conversion (1. prefix)."""

    def test_single_item(self):
        result = parse("1. First item")
        assert "<ol>" in result
        assert "<li>First item</li>" in result
        assert "</ol>" in result

    def test_multiple_items(self):
        result = parse("1. First\n2. Second\n3. Third")
        assert result.count("<li>") == 3
        assert "<ol>" in result


class TestInlineCode:
    """Test inline code conversion (`backticks`)."""

    def test_inline_code(self):
        result = parse("Use `print()` here")
        assert "<code>print()</code>" in result

    def test_inline_code_in_paragraph(self):
        result = parse("Run `foo` and `bar`")
        assert result.count("<code>") == 2


class TestCodeBlocks:
    """Test fenced code block conversion (triple backticks)."""

    def test_code_block(self):
        md = "```\nprint('hello')\n```"
        result = parse(md)
        assert "<pre><code>" in result
        assert "print('hello')" in result
        assert "</code></pre>" in result

    def test_code_block_with_language(self):
        md = "```python\nprint('hello')\n```"
        result = parse(md)
        assert "<pre><code>" in result
        assert "print('hello')" in result

    def test_code_block_preserves_content(self):
        md = "```\nline1\nline2\n```"
        result = parse(md)
        assert "line1\nline2" in result


class TestLinks:
    """Test link conversion ([text](url))."""

    def test_basic_link(self):
        result = parse("[Click here](https://example.com)")
        assert '<a href="https://example.com">Click here</a>' in result

    def test_link_in_paragraph(self):
        result = parse("Visit [my site](https://example.com) today")
        assert '<a href="https://example.com">my site</a>' in result


class TestBoldAndItalic:
    """Test bold (**text**) and italic (*text*) conversion."""

    def test_bold(self):
        result = parse("This is **bold** text")
        assert "<strong>bold</strong>" in result

    def test_italic(self):
        result = parse("This is *italic* text")
        assert "<em>italic</em>" in result

    def test_bold_and_italic_together(self):
        result = parse("**bold** and *italic*")
        assert "<strong>bold</strong>" in result
        assert "<em>italic</em>" in result


class TestMixedContent:
    """Test combinations of markdown elements."""

    def test_heading_then_paragraph(self):
        result = parse("# Title\n\nSome text")
        assert "<h1>Title</h1>" in result
        assert "<p>Some text</p>" in result

    def test_paragraph_then_list(self):
        result = parse("Intro text\n\n- Item one\n- Item two")
        assert "<p>Intro text</p>" in result
        assert "<ul>" in result

    def test_empty_input(self):
        assert parse("") == ""

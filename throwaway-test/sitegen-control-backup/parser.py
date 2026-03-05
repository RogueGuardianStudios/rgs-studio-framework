"""Markdown to HTML parser.

Converts a subset of Markdown syntax to HTML. Supports headings,
paragraphs, unordered and ordered lists, inline code, fenced code
blocks, links, bold, and italic formatting.
"""

import re


def parse(markdown_text: str) -> str:
    """Convert markdown text to an HTML string.

    Args:
        markdown_text: A string containing markdown-formatted text.

    Returns:
        A string containing the corresponding HTML.

    Supported markdown syntax:
        - Headings: ``# h1`` through ``###### h6``
        - Paragraphs: blank-line separated text blocks
        - Unordered lists: ``- item`` prefix
        - Ordered lists: ``1. item`` prefix
        - Inline code: backtick-delimited
        - Fenced code blocks: triple-backtick delimited
        - Links: ``[text](url)``
        - Bold: ``**text**``
        - Italic: ``*text*``
    """
    if not markdown_text.strip():
        return ""

    lines = markdown_text.split("\n")
    blocks = _split_into_blocks(lines)
    html_parts = [_render_block(block) for block in blocks]
    return "\n".join(html_parts)


def _split_into_blocks(lines: list[str]) -> list[list[str]]:
    """Split lines into logical blocks separated by blank lines.

    Code blocks (fenced with ```) are kept as single blocks regardless
    of blank lines within them.
    """
    blocks = []
    current_block = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith("```") and not in_code_block:
            # Start of code block
            if current_block:
                blocks.append(current_block)
                current_block = []
            in_code_block = True
            current_block.append(line)
        elif line.strip().startswith("```") and in_code_block:
            # End of code block
            current_block.append(line)
            blocks.append(current_block)
            current_block = []
            in_code_block = False
        elif in_code_block:
            current_block.append(line)
        elif line.strip() == "":
            if current_block:
                blocks.append(current_block)
                current_block = []
        else:
            current_block.append(line)

    if current_block:
        blocks.append(current_block)

    return blocks


def _render_block(block: list[str]) -> str:
    """Render a single block of lines into HTML."""
    if not block:
        return ""

    first_line = block[0]

    # Code block
    if first_line.strip().startswith("```"):
        return _render_code_block(block)

    # Heading
    if re.match(r"^#{1,6}\s", first_line) and len(block) == 1:
        return _render_heading(first_line)

    # Unordered list
    if all(re.match(r"^- ", line) for line in block):
        return _render_unordered_list(block)

    # Ordered list
    if all(re.match(r"^\d+\.\s", line) for line in block):
        return _render_ordered_list(block)

    # Paragraph (default)
    return _render_paragraph(block)


def _render_heading(line: str) -> str:
    """Render a heading line."""
    match = re.match(r"^(#{1,6})\s+(.*)", line)
    if not match:
        return _inline_format(line)
    level = len(match.group(1))
    content = _inline_format(match.group(2))
    return f"<h{level}>{content}</h{level}>"


def _render_paragraph(block: list[str]) -> str:
    """Render a paragraph block."""
    text = "\n".join(block)
    return f"<p>{_inline_format(text)}</p>"


def _render_unordered_list(block: list[str]) -> str:
    """Render an unordered list block."""
    items = []
    for line in block:
        content = re.sub(r"^- ", "", line)
        items.append(f"<li>{_inline_format(content)}</li>")
    return "<ul>\n" + "\n".join(items) + "\n</ul>"


def _render_ordered_list(block: list[str]) -> str:
    """Render an ordered list block."""
    items = []
    for line in block:
        content = re.sub(r"^\d+\.\s+", "", line)
        items.append(f"<li>{_inline_format(content)}</li>")
    return "<ol>\n" + "\n".join(items) + "\n</ol>"


def _render_code_block(block: list[str]) -> str:
    """Render a fenced code block."""
    # Strip opening and closing ``` lines
    inner_lines = block[1:-1] if len(block) > 2 else []
    code_content = "\n".join(inner_lines)
    return f"<pre><code>{code_content}</code></pre>"


def _inline_format(text: str) -> str:
    """Apply inline formatting: code, links, bold, italic.

    Processing order is chosen to avoid conflicts between
    overlapping syntax patterns.
    """
    # Inline code first (so contents aren't further processed)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # Links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    # Bold (before italic so ** is matched before *)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text

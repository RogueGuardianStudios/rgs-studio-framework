"""Markdown to HTML parser for the sitegen static site generator.

Converts markdown text to HTML. Supports headings, paragraphs,
unordered lists, ordered lists, inline code, code blocks, links,
bold, and italic formatting.
"""

import re


def parse(markdown_text: str) -> str:
    """Parse markdown text and return an HTML string.

    Args:
        markdown_text: A string containing markdown-formatted text.

    Returns:
        A string containing the corresponding HTML.
    """
    lines = markdown_text.split("\n")
    html_parts = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Code blocks (triple backtick fenced)
        if line.strip().startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            code_content = "\n".join(code_lines)
            html_parts.append(f"<pre><code>{code_content}</code></pre>")
            i += 1
            continue

        # Headings (h1 through h6)
        heading_match = re.match(r"^(#{1,6})\s+(.*)", line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)
            text = _inline_formatting(text)
            html_parts.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue

        # Unordered lists (- prefix)
        if line.strip().startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                item_text = lines[i].strip()[2:]
                items.append(f"<li>{_inline_formatting(item_text)}</li>")
                i += 1
            html_parts.append("<ul>" + "".join(items) + "</ul>")
            continue

        # Ordered lists (1. prefix)
        ol_match = re.match(r"^\d+\.\s+(.*)", line.strip())
        if ol_match:
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+(.*)", lines[i].strip()):
                m = re.match(r"^\d+\.\s+(.*)", lines[i].strip())
                items.append(f"<li>{_inline_formatting(m.group(1))}</li>")
                i += 1
            html_parts.append("<ol>" + "".join(items) + "</ol>")
            continue

        # Blank lines (paragraph separator)
        if line.strip() == "":
            i += 1
            continue

        # Paragraphs (collect consecutive non-blank, non-special lines)
        para_lines = []
        while i < len(lines) and lines[i].strip() != "" and not _is_special_line(lines[i]):
            para_lines.append(lines[i])
            i += 1
        if para_lines:
            text = " ".join(para_lines)
            html_parts.append(f"<p>{_inline_formatting(text)}</p>")
            continue

        i += 1

    return "\n".join(html_parts)


def _inline_formatting(text: str) -> str:
    """Apply inline formatting: bold, italic, inline code, links.

    Args:
        text: Raw text that may contain inline markdown formatting.

    Returns:
        Text with inline markdown converted to HTML tags.
    """
    # Inline code
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # Bold
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    # Links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def _is_special_line(line: str) -> bool:
    """Check if a line is a special markdown element (not a paragraph line).

    Args:
        line: A single line of text.

    Returns:
        True if the line starts a heading, list, or code block.
    """
    stripped = line.strip()
    if re.match(r"^#{1,6}\s+", stripped):
        return True
    if stripped.startswith("- "):
        return True
    if re.match(r"^\d+\.\s+", stripped):
        return True
    if stripped.startswith("```"):
        return True
    return False

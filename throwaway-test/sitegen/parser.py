"""sitegen.parser — Markdown to HTML conversion.

Converts markdown text to HTML. Supports headings, paragraphs,
unordered and ordered lists, inline code, code blocks, links,
bold, and italic.
"""

import re


def parse(markdown_text: str) -> str:
    """Convert markdown text to an HTML string.

    Args:
        markdown_text: Raw markdown content to convert.

    Returns:
        HTML string generated from the markdown input.
    """
    lines = markdown_text.split('\n')
    html_parts = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Code blocks (triple backtick fenced)
        if line.startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1
            html_parts.append('<pre><code>' + '\n'.join(code_lines) + '</code></pre>')
            i += 1
            continue

        # Headings (h1 through h6)
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)
            html_parts.append(f'<h{level}>{text}</h{level}>')
            i += 1
            continue

        # Unordered list
        if line.startswith('- '):
            items = []
            while i < len(lines) and lines[i].startswith('- '):
                items.append('<li>' + lines[i][2:] + '</li>')
                i += 1
            html_parts.append('<ul>\n' + '\n'.join(items) + '\n</ul>')
            continue

        # Ordered list
        ol_match = re.match(r'^\d+\.\s+', line)
        if ol_match:
            items = []
            while i < len(lines) and re.match(r'^\d+\.\s+', lines[i]):
                text = re.sub(r'^\d+\.\s+', '', lines[i])
                items.append('<li>' + text + '</li>')
                i += 1
            html_parts.append('<ol>\n' + '\n'.join(items) + '\n</ol>')
            continue

        # Blank lines (paragraph separator)
        if line.strip() == '':
            i += 1
            continue

        # Paragraph — collect contiguous non-blank, non-special lines
        para_lines = []
        while i < len(lines) and lines[i].strip() != '' and not lines[i].startswith('#') and not lines[i].startswith('- ') and not re.match(r'^\d+\.\s+', lines[i]) and not lines[i].startswith('```'):
            para_lines.append(lines[i])
            i += 1
        text = ' '.join(para_lines)
        text = _apply_inline(text)
        html_parts.append(f'<p>{text}</p>')
        continue

    return '\n'.join(html_parts)


def _apply_inline(text: str) -> str:
    """Apply inline formatting: bold, italic, code, links."""
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    return text

"""Site builder — walks source markdown files, applies templates, outputs HTML.

Processes a directory tree of markdown files with optional YAML front matter,
renders them through templates, and writes the result to a build directory.
Static assets (non-markdown files) are copied through unchanged.
"""

import os
import shutil
from dataclasses import dataclass, field

import yaml

from sitegen.parser import parse
from sitegen.templates import Template, load_template


@dataclass
class BuildResult:
    """Result of a site build operation.

    Attributes:
        pages_built: The number of markdown pages successfully rendered.
        errors: A list of error messages for pages that failed to build.
    """

    pages_built: int
    errors: list[str] = field(default_factory=list)


# File extensions treated as markdown sources (converted to HTML).
_MARKDOWN_EXTENSIONS = {".md", ".markdown"}


class SiteBuilder:
    """Builds a static site from markdown sources, templates, and assets.

    Args:
        source_dir: Path to the directory containing markdown files and assets.
        build_dir: Path to the output directory. Will be cleaned before each build.
        template_dir: Path to the directory containing HTML template files.
    """

    def __init__(self, source_dir: str, build_dir: str, template_dir: str) -> None:
        self._source_dir = source_dir
        self._build_dir = build_dir
        self._template_dir = template_dir

    def build(self) -> BuildResult:
        """Build the full site.

        Performs a clean build: deletes the build directory if it exists,
        then walks the source directory. Markdown files are parsed and
        rendered through templates; all other files are copied as assets.

        Returns:
            A BuildResult with the count of pages built and any errors.
        """
        # Clean build
        if os.path.exists(self._build_dir):
            shutil.rmtree(self._build_dir)
        os.makedirs(self._build_dir, exist_ok=True)

        pages_built = 0
        errors: list[str] = []

        for dirpath, _dirnames, filenames in os.walk(self._source_dir):
            rel_dir = os.path.relpath(dirpath, self._source_dir)
            out_dir = os.path.join(self._build_dir, rel_dir) if rel_dir != "." else self._build_dir
            os.makedirs(out_dir, exist_ok=True)

            for filename in filenames:
                src_path = os.path.join(dirpath, filename)
                _, ext = os.path.splitext(filename)

                if ext.lower() in _MARKDOWN_EXTENSIONS:
                    err = self._build_page(src_path, out_dir, filename)
                    if err:
                        errors.append(err)
                    else:
                        pages_built += 1
                else:
                    # Copy asset
                    shutil.copy2(src_path, os.path.join(out_dir, filename))

        return BuildResult(pages_built=pages_built, errors=errors)

    def _build_page(self, src_path: str, out_dir: str, filename: str) -> str | None:
        """Build a single markdown page. Returns an error string or None on success."""
        with open(src_path, "r") as f:
            raw = f.read()

        front_matter, body = _extract_front_matter(raw)

        # Determine template
        template_name = front_matter.get("template", "default.html")
        template_path = os.path.join(self._template_dir, template_name)

        if not os.path.exists(template_path):
            return f"Template '{template_name}' not found for {src_path}"

        template = load_template(template_path)

        # Parse markdown body to HTML
        html_content = parse(body)

        # Build context from front matter + content
        context = dict(front_matter)
        context["content"] = html_content

        # Render
        rendered = template.render(context, include_dir=self._template_dir)

        # Write output
        out_name = os.path.splitext(filename)[0] + ".html"
        out_path = os.path.join(out_dir, out_name)
        with open(out_path, "w") as f:
            f.write(rendered)

        return None


def _extract_front_matter(text: str) -> tuple[dict, str]:
    """Extract YAML front matter from markdown text.

    Front matter is delimited by ``---`` on its own line at the start
    and end of the block. If no front matter is present, returns an
    empty dict and the original text.

    Args:
        text: The raw markdown file content.

    Returns:
        A tuple of (front_matter_dict, remaining_body).
    """
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    # parts[0] is empty (before first ---), parts[1] is YAML, parts[2] is body
    if len(parts) < 3:
        return {}, text

    try:
        fm = yaml.safe_load(parts[1])
        if not isinstance(fm, dict):
            return {}, text
    except yaml.YAMLError:
        return {}, text

    body = parts[2].lstrip("\n")
    return fm, body

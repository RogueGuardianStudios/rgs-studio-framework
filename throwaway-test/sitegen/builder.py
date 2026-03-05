"""Site builder for the sitegen static site generator.

Walks a source directory of markdown files, applies templates,
and outputs rendered HTML to a build directory. Supports recursive
directory walking, front matter extraction, template selection,
asset copying, and clean builds.
"""

import os
import shutil
from sitegen.parser import parse
from sitegen.templates import load_template


class BuildResult:
    """Result of a site build operation.

    Attributes:
        pages_built: Number of pages successfully built.
        errors: List of error messages encountered during the build.
    """

    def __init__(self):
        self.pages_built: int = 0
        self.errors: list[str] = []


class SiteBuilder:
    """Builds a static site from markdown source files.

    Args:
        source_dir: Path to the directory containing markdown source files.
        build_dir: Path to the output directory for rendered HTML.
        template_dir: Path to the directory containing HTML templates.
    """

    def __init__(self, source_dir: str, build_dir: str, template_dir: str):
        self._source_dir = source_dir
        self._build_dir = build_dir
        self._template_dir = template_dir

    def build(self) -> BuildResult:
        """Build the static site.

        Cleans the build directory, walks the source directory recursively,
        processes markdown files through templates, and copies assets.

        Returns:
            A BuildResult with the count of pages built and any errors.
        """
        result = BuildResult()

        # Clean build: delete and recreate build directory
        if os.path.exists(self._build_dir):
            shutil.rmtree(self._build_dir)
        os.makedirs(self._build_dir)

        # Walk source directory recursively
        for dirpath, dirnames, filenames in os.walk(self._source_dir):
            rel_dir = os.path.relpath(dirpath, self._source_dir)
            if rel_dir == ".":
                rel_dir = ""

            for filename in filenames:
                source_path = os.path.join(dirpath, filename)

                if filename.endswith(".md"):
                    # Process markdown files
                    try:
                        self._process_markdown(source_path, rel_dir, result)
                    except Exception as e:
                        result.errors.append(f"Error processing {source_path}: {e}")
                else:
                    # Copy asset files (CSS, images, etc.)
                    self._copy_asset(source_path, rel_dir, filename)

        return result

    def _process_markdown(self, source_path: str, rel_dir: str, result: BuildResult):
        """Process a single markdown file: extract front matter, parse, render template.

        Args:
            source_path: Absolute path to the markdown source file.
            rel_dir: Relative directory path from source root.
            result: BuildResult to update with counts/errors.
        """
        with open(source_path, "r") as f:
            raw_content = f.read()

        front_matter, body = _extract_front_matter(raw_content)

        # Parse markdown body to HTML
        html_body = parse(body)

        # Build template context from front matter + content
        context = dict(front_matter)
        context["content"] = html_body

        # Select template
        template_name = front_matter.get("template", "default.html")
        template_path = os.path.join(self._template_dir, template_name)
        template = load_template(template_path)

        # Render
        rendered = template.render(context, include_dir=self._template_dir)

        # Write output
        output_dir = os.path.join(self._build_dir, rel_dir) if rel_dir else self._build_dir
        os.makedirs(output_dir, exist_ok=True)

        basename = os.path.splitext(os.path.basename(source_path))[0]
        output_path = os.path.join(output_dir, f"{basename}.html")

        with open(output_path, "w") as f:
            f.write(rendered)

        result.pages_built += 1

    def _copy_asset(self, source_path: str, rel_dir: str, filename: str):
        """Copy a non-markdown asset file to the build directory.

        Args:
            source_path: Absolute path to the source asset file.
            rel_dir: Relative directory path from source root.
            filename: Name of the asset file.
        """
        output_dir = os.path.join(self._build_dir, rel_dir) if rel_dir else self._build_dir
        os.makedirs(output_dir, exist_ok=True)
        shutil.copy2(source_path, os.path.join(output_dir, filename))


def _extract_front_matter(text: str) -> tuple[dict, str]:
    """Extract YAML front matter from markdown text.

    Front matter is delimited by --- lines at the start of the file.

    Args:
        text: Raw markdown text that may contain front matter.

    Returns:
        A tuple of (front_matter_dict, remaining_body_text).
    """
    if not text.startswith("---"):
        return {}, text

    lines = text.split("\n")
    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break

    if end_index is None:
        return {}, text

    # Simple YAML key: value parsing
    front_matter = {}
    for line in lines[1:end_index]:
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            front_matter[key.strip()] = value.strip()

    body = "\n".join(lines[end_index + 1:]).strip()
    return front_matter, body

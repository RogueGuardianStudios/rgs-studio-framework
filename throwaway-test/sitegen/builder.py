"""sitegen.builder — Site building from markdown source directories.

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
        pages_built: Number of markdown pages successfully rendered.
        errors: List of error messages encountered during the build.
    """

    def __init__(self, pages_built: int, errors: list):
        """Initialize a BuildResult.

        Args:
            pages_built: Count of pages successfully built.
            errors: List of error strings from the build.
        """
        self.pages_built = pages_built
        self.errors = errors


class SiteBuilder:
    """Builds a static site from markdown sources using templates.

    Walks the source directory recursively, extracts front matter,
    selects templates, renders markdown to HTML, and copies assets.
    """

    def __init__(self, source_dir: str, build_dir: str, template_dir: str):
        """Initialize the SiteBuilder.

        Args:
            source_dir: Path to the source directory containing markdown files.
            build_dir: Path to the output build directory.
            template_dir: Path to the directory containing HTML templates.
        """
        self._source_dir = source_dir
        self._build_dir = build_dir
        self._template_dir = template_dir

    def build(self) -> BuildResult:
        """Build the site: clean, render markdown, copy assets.

        Deletes the build directory if it exists (clean build),
        walks the source directory recursively, renders each
        markdown file through its selected template, and copies
        non-markdown assets to the build directory.

        Returns:
            A BuildResult with pages_built count and any errors.
        """
        pages_built = 0
        errors = []

        # Clean build — delete build dir before building
        if os.path.exists(self._build_dir):
            shutil.rmtree(self._build_dir)
        os.makedirs(self._build_dir, exist_ok=True)

        # Walk source directory recursively
        for dirpath, dirnames, filenames in os.walk(self._source_dir):
            rel_dir = os.path.relpath(dirpath, self._source_dir)
            out_dir = os.path.join(self._build_dir, rel_dir) if rel_dir != '.' else self._build_dir
            os.makedirs(out_dir, exist_ok=True)

            for filename in filenames:
                src_path = os.path.join(dirpath, filename)

                if filename.endswith('.md'):
                    # Process markdown file
                    try:
                        with open(src_path, 'r') as f:
                            content = f.read()

                        front_matter, body = self._extract_front_matter(content)
                        template_name = front_matter.get('template')

                        if not template_name:
                            errors.append(f"No template specified in {src_path}")
                            continue

                        template_path = os.path.join(self._template_dir, template_name)
                        if not os.path.exists(template_path):
                            errors.append(f"Template not found: {template_name} for {src_path}")
                            continue

                        template = load_template(template_path)
                        html_content = parse(body)

                        # Build context from front matter + content
                        context = dict(front_matter)
                        context['content'] = html_content

                        rendered = template.render(context)

                        # Write output
                        out_name = filename.replace('.md', '.html')
                        out_path = os.path.join(out_dir, out_name)
                        with open(out_path, 'w') as f:
                            f.write(rendered)

                        pages_built += 1

                    except Exception as e:
                        errors.append(f"Error processing {src_path}: {str(e)}")
                else:
                    # Asset copying — CSS, images, etc.
                    dst_path = os.path.join(out_dir, filename)
                    shutil.copy2(src_path, dst_path)

        return BuildResult(pages_built=pages_built, errors=errors)

    def _extract_front_matter(self, content: str) -> tuple:
        """Extract YAML front matter from markdown content.

        Args:
            content: Raw file content potentially starting with --- delimiters.

        Returns:
            Tuple of (front_matter_dict, body_string).
        """
        if not content.startswith('---'):
            return {}, content

        parts = content.split('---', 2)
        if len(parts) < 3:
            return {}, content

        front_matter = {}
        for line in parts[1].strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                front_matter[key.strip()] = value.strip()

        body = parts[2].strip()
        return front_matter, body

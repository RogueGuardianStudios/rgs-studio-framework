"""Tests for sitegen.builder module.

Tests the public API:
- SiteBuilder(source_dir: str, build_dir: str, template_dir: str)
- SiteBuilder.build() -> BuildResult
- BuildResult.pages_built: int
- BuildResult.errors: list[str]

Covers: recursive directory walking, front matter extraction,
template selection, asset copying, clean build.
"""

import os
import pytest
import tempfile
import shutil
from sitegen.builder import SiteBuilder, BuildResult


@pytest.fixture
def site_dirs():
    """Create temporary source, build, and template directories."""
    tmpdir = tempfile.mkdtemp()
    source_dir = os.path.join(tmpdir, "source")
    build_dir = os.path.join(tmpdir, "build")
    template_dir = os.path.join(tmpdir, "templates")
    os.makedirs(source_dir)
    os.makedirs(build_dir)
    os.makedirs(template_dir)

    # Write a default template
    with open(os.path.join(template_dir, "default.html"), "w") as f:
        f.write("<html><body>{{ content }}</body></html>")

    yield source_dir, build_dir, template_dir
    shutil.rmtree(tmpdir)


class TestBuildResultAttributes:
    """Test BuildResult has the specified attributes."""

    def test_pages_built_is_int(self, site_dirs):
        source_dir, build_dir, template_dir = site_dirs
        builder = SiteBuilder(source_dir, build_dir, template_dir)
        result = builder.build()
        assert isinstance(result.pages_built, int)

    def test_errors_is_list(self, site_dirs):
        source_dir, build_dir, template_dir = site_dirs
        builder = SiteBuilder(source_dir, build_dir, template_dir)
        result = builder.build()
        assert isinstance(result.errors, list)


class TestEmptyBuild:
    """Test building with no source files."""

    def test_empty_source(self, site_dirs):
        source_dir, build_dir, template_dir = site_dirs
        builder = SiteBuilder(source_dir, build_dir, template_dir)
        result = builder.build()
        assert result.pages_built == 0
        assert result.errors == []


class TestSinglePageBuild:
    """Test building a single markdown page."""

    def test_single_page(self, site_dirs):
        source_dir, build_dir, template_dir = site_dirs

        # Write a markdown file with front matter
        with open(os.path.join(source_dir, "index.md"), "w") as f:
            f.write("---\ntemplate: default.html\ntitle: Home\n---\n# Welcome\n")

        builder = SiteBuilder(source_dir, build_dir, template_dir)
        result = builder.build()

        assert result.pages_built == 1
        assert result.errors == []

        output_file = os.path.join(build_dir, "index.html")
        assert os.path.exists(output_file)

        with open(output_file) as f:
            content = f.read()
        assert "<h1>Welcome</h1>" in content


class TestRecursiveDirectoryWalking:
    """Test that subdirectories in source are walked recursively."""

    def test_nested_directory(self, site_dirs):
        source_dir, build_dir, template_dir = site_dirs

        subdir = os.path.join(source_dir, "blog")
        os.makedirs(subdir)
        with open(os.path.join(subdir, "post.md"), "w") as f:
            f.write("---\ntemplate: default.html\ntitle: Post\n---\n# Blog Post\n")

        builder = SiteBuilder(source_dir, build_dir, template_dir)
        result = builder.build()

        assert result.pages_built == 1
        output_file = os.path.join(build_dir, "blog", "post.html")
        assert os.path.exists(output_file)


class TestFrontMatterExtraction:
    """Test YAML front matter extraction between --- delimiters."""

    def test_front_matter_used_in_template(self, site_dirs):
        source_dir, build_dir, template_dir = site_dirs

        # Template that uses title from front matter
        with open(os.path.join(template_dir, "titled.html"), "w") as f:
            f.write("<html><title>{{ title }}</title><body>{{ content }}</body></html>")

        with open(os.path.join(source_dir, "page.md"), "w") as f:
            f.write("---\ntemplate: titled.html\ntitle: My Page\n---\n# Hello\n")

        builder = SiteBuilder(source_dir, build_dir, template_dir)
        result = builder.build()

        assert result.pages_built == 1
        with open(os.path.join(build_dir, "page.html")) as f:
            content = f.read()
        assert "<title>My Page</title>" in content


class TestTemplateSelection:
    """Test template selection from front matter."""

    def test_selects_template_from_front_matter(self, site_dirs):
        source_dir, build_dir, template_dir = site_dirs

        with open(os.path.join(template_dir, "custom.html"), "w") as f:
            f.write("<custom>{{ content }}</custom>")

        with open(os.path.join(source_dir, "page.md"), "w") as f:
            f.write("---\ntemplate: custom.html\n---\n# Custom\n")

        builder = SiteBuilder(source_dir, build_dir, template_dir)
        result = builder.build()

        with open(os.path.join(build_dir, "page.html")) as f:
            content = f.read()
        assert "<custom>" in content


class TestAssetCopying:
    """Test CSS and image copying from source to build."""

    def test_css_copied(self, site_dirs):
        source_dir, build_dir, template_dir = site_dirs

        css_dir = os.path.join(source_dir, "css")
        os.makedirs(css_dir)
        with open(os.path.join(css_dir, "style.css"), "w") as f:
            f.write("body { color: red; }")

        builder = SiteBuilder(source_dir, build_dir, template_dir)
        builder.build()

        output_css = os.path.join(build_dir, "css", "style.css")
        assert os.path.exists(output_css)
        with open(output_css) as f:
            assert f.read() == "body { color: red; }"

    def test_image_copied(self, site_dirs):
        source_dir, build_dir, template_dir = site_dirs

        img_dir = os.path.join(source_dir, "images")
        os.makedirs(img_dir)
        with open(os.path.join(img_dir, "logo.png"), "wb") as f:
            f.write(b"\x89PNG\r\n")

        builder = SiteBuilder(source_dir, build_dir, template_dir)
        builder.build()

        assert os.path.exists(os.path.join(build_dir, "images", "logo.png"))


class TestCleanBuild:
    """Test that build directory is cleaned before building."""

    def test_old_files_removed(self, site_dirs):
        source_dir, build_dir, template_dir = site_dirs

        # Put a stale file in build dir
        with open(os.path.join(build_dir, "old.html"), "w") as f:
            f.write("stale")

        builder = SiteBuilder(source_dir, build_dir, template_dir)
        builder.build()

        assert not os.path.exists(os.path.join(build_dir, "old.html"))

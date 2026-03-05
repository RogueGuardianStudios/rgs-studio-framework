"""Tests for sitegen.builder — Site building from markdown sources."""

import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sitegen.builder import SiteBuilder, BuildResult


def _make_site(tmpdir):
    """Create a minimal site structure for testing.

    Returns (source_dir, build_dir, template_dir).
    """
    source_dir = os.path.join(tmpdir, "source")
    build_dir = os.path.join(tmpdir, "build")
    template_dir = os.path.join(tmpdir, "templates")

    os.makedirs(source_dir)
    os.makedirs(template_dir)

    return source_dir, build_dir, template_dir


class TestBuildResult:
    """Test BuildResult data class."""

    def test_build_result_has_pages_built(self):
        r = BuildResult(pages_built=3, errors=[])
        assert r.pages_built == 3

    def test_build_result_has_errors(self):
        r = BuildResult(pages_built=0, errors=["Something went wrong"])
        assert len(r.errors) == 1


class TestSiteBuilderBasic:
    """Test basic site building functionality."""

    def test_build_single_page(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source, build, templates = _make_site(tmpdir)

            # Create a markdown file
            with open(os.path.join(source, "index.md"), "w") as f:
                f.write("# Hello\n\nWelcome to my site.")

            # Create a default template
            with open(os.path.join(templates, "default.html"), "w") as f:
                f.write("<html><body>{{ content }}</body></html>")

            builder = SiteBuilder(source, build, templates)
            result = builder.build()

            assert result.pages_built == 1
            assert len(result.errors) == 0
            assert os.path.exists(os.path.join(build, "index.html"))

    def test_output_contains_rendered_html(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source, build, templates = _make_site(tmpdir)

            with open(os.path.join(source, "page.md"), "w") as f:
                f.write("# Test Page\n\nSome content here.")

            with open(os.path.join(templates, "default.html"), "w") as f:
                f.write("<html>{{ content }}</html>")

            builder = SiteBuilder(source, build, templates)
            builder.build()

            with open(os.path.join(build, "page.html"), "r") as f:
                html = f.read()

            assert "<h1>Test Page</h1>" in html
            assert "<p>Some content here.</p>" in html

    def test_build_multiple_pages(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source, build, templates = _make_site(tmpdir)

            for name in ["one.md", "two.md", "three.md"]:
                with open(os.path.join(source, name), "w") as f:
                    f.write(f"# {name}")

            with open(os.path.join(templates, "default.html"), "w") as f:
                f.write("{{ content }}")

            builder = SiteBuilder(source, build, templates)
            result = builder.build()

            assert result.pages_built == 3


class TestRecursiveDirectoryWalking:
    """Test recursive directory walking."""

    def test_nested_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source, build, templates = _make_site(tmpdir)

            sub = os.path.join(source, "blog")
            os.makedirs(sub)
            with open(os.path.join(sub, "post.md"), "w") as f:
                f.write("# Blog Post")

            with open(os.path.join(templates, "default.html"), "w") as f:
                f.write("{{ content }}")

            builder = SiteBuilder(source, build, templates)
            builder.build()

            assert os.path.exists(os.path.join(build, "blog", "post.html"))


class TestFrontMatter:
    """Test YAML front matter extraction."""

    def test_front_matter_title_in_template(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source, build, templates = _make_site(tmpdir)

            with open(os.path.join(source, "page.md"), "w") as f:
                f.write("---\ntitle: My Page\n---\n# Hello")

            with open(os.path.join(templates, "default.html"), "w") as f:
                f.write("<title>{{ title }}</title>{{ content }}")

            builder = SiteBuilder(source, build, templates)
            builder.build()

            with open(os.path.join(build, "page.html"), "r") as f:
                html = f.read()

            assert "<title>My Page</title>" in html

    def test_front_matter_template_selection(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source, build, templates = _make_site(tmpdir)

            with open(os.path.join(source, "page.md"), "w") as f:
                f.write("---\ntemplate: custom.html\n---\n# Hello")

            with open(os.path.join(templates, "default.html"), "w") as f:
                f.write("DEFAULT {{ content }}")

            with open(os.path.join(templates, "custom.html"), "w") as f:
                f.write("CUSTOM {{ content }}")

            builder = SiteBuilder(source, build, templates)
            builder.build()

            with open(os.path.join(build, "page.html"), "r") as f:
                html = f.read()

            assert "CUSTOM" in html
            assert "DEFAULT" not in html


class TestAssetCopying:
    """Test static asset copying (CSS, images)."""

    def test_css_file_copied(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source, build, templates = _make_site(tmpdir)

            css_dir = os.path.join(source, "css")
            os.makedirs(css_dir)
            with open(os.path.join(css_dir, "style.css"), "w") as f:
                f.write("body { color: red; }")

            with open(os.path.join(templates, "default.html"), "w") as f:
                f.write("{{ content }}")

            builder = SiteBuilder(source, build, templates)
            builder.build()

            assert os.path.exists(os.path.join(build, "css", "style.css"))

    def test_image_file_copied(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source, build, templates = _make_site(tmpdir)

            img_dir = os.path.join(source, "images")
            os.makedirs(img_dir)
            with open(os.path.join(img_dir, "logo.png"), "wb") as f:
                f.write(b"\x89PNG fake image data")

            with open(os.path.join(templates, "default.html"), "w") as f:
                f.write("{{ content }}")

            builder = SiteBuilder(source, build, templates)
            builder.build()

            assert os.path.exists(os.path.join(build, "images", "logo.png"))


class TestCleanBuild:
    """Test clean build — build dir deleted before building."""

    def test_old_files_removed(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source, build, templates = _make_site(tmpdir)

            # Create build dir with stale file
            os.makedirs(build)
            with open(os.path.join(build, "stale.html"), "w") as f:
                f.write("old content")

            with open(os.path.join(source, "index.md"), "w") as f:
                f.write("# Fresh")

            with open(os.path.join(templates, "default.html"), "w") as f:
                f.write("{{ content }}")

            builder = SiteBuilder(source, build, templates)
            builder.build()

            assert not os.path.exists(os.path.join(build, "stale.html"))
            assert os.path.exists(os.path.join(build, "index.html"))


class TestBuildErrors:
    """Test error handling during builds."""

    def test_missing_template_records_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source, build, templates = _make_site(tmpdir)

            with open(os.path.join(source, "page.md"), "w") as f:
                f.write("---\ntemplate: nonexistent.html\n---\n# Hello")

            # No default template either
            builder = SiteBuilder(source, build, templates)
            result = builder.build()

            assert len(result.errors) > 0

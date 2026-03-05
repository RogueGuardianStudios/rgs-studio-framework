"""Tests for sitegen.builder — Site building from markdown sources.

Tests written FIRST per TDD requirement. Each test covers
a specific feature from the Brief's Phase 3 specification.
"""

import sys
import os
import shutil
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sitegen.builder import SiteBuilder, BuildResult


class TestBuildResult:
    """BuildResult has pages_built: int and errors: list[str]."""

    def test_build_result_pages_built(self):
        r = BuildResult(pages_built=3, errors=[])
        assert r.pages_built == 3

    def test_build_result_errors(self):
        r = BuildResult(pages_built=0, errors=["something broke"])
        assert r.errors == ["something broke"]


class TestSiteBuilderConstructor:
    """SiteBuilder(source_dir, build_dir, template_dir) constructor."""

    def test_constructor(self):
        sb = SiteBuilder("/tmp/src", "/tmp/build", "/tmp/templates")
        assert sb is not None


class TestCleanBuild:
    """Clean build — delete build dir before building."""

    def test_clean_build_removes_old_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "src")
            build = os.path.join(tmpdir, "build")
            templates = os.path.join(tmpdir, "templates")
            os.makedirs(src)
            os.makedirs(build)
            os.makedirs(templates)

            # Put a stale file in build
            stale = os.path.join(build, "stale.html")
            with open(stale, 'w') as f:
                f.write("old content")

            # Write a template
            with open(os.path.join(templates, "default.html"), 'w') as f:
                f.write("<html>{{ content }}</html>")

            # Write a markdown file
            with open(os.path.join(src, "index.md"), 'w') as f:
                f.write("---\ntemplate: default.html\n---\n# Hello")

            sb = SiteBuilder(src, build, templates)
            sb.build()
            assert not os.path.exists(stale)


class TestRecursiveDirectoryWalking:
    """Recursive directory walking of source markdown files."""

    def test_nested_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "src")
            build = os.path.join(tmpdir, "build")
            templates = os.path.join(tmpdir, "templates")
            os.makedirs(os.path.join(src, "sub"))
            os.makedirs(templates)

            with open(os.path.join(templates, "default.html"), 'w') as f:
                f.write("<html>{{ content }}</html>")

            with open(os.path.join(src, "index.md"), 'w') as f:
                f.write("---\ntemplate: default.html\n---\n# Top")

            with open(os.path.join(src, "sub", "page.md"), 'w') as f:
                f.write("---\ntemplate: default.html\n---\n# Sub")

            sb = SiteBuilder(src, build, templates)
            result = sb.build()
            assert result.pages_built == 2
            assert os.path.exists(os.path.join(build, "index.html"))
            assert os.path.exists(os.path.join(build, "sub", "page.html"))


class TestFrontMatterExtraction:
    """Front matter extraction (YAML between --- delimiters)."""

    def test_front_matter_extracted(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "src")
            build = os.path.join(tmpdir, "build")
            templates = os.path.join(tmpdir, "templates")
            os.makedirs(src)
            os.makedirs(templates)

            with open(os.path.join(templates, "default.html"), 'w') as f:
                f.write("<html><title>{{ title }}</title>{{ content }}</html>")

            with open(os.path.join(src, "index.md"), 'w') as f:
                f.write("---\ntemplate: default.html\ntitle: My Page\n---\n# Hello")

            sb = SiteBuilder(src, build, templates)
            result = sb.build()
            assert result.pages_built == 1

            with open(os.path.join(build, "index.html"), 'r') as f:
                html = f.read()
            assert "<title>My Page</title>" in html


class TestTemplateSelection:
    """Template selection from front matter."""

    def test_selects_template_from_front_matter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "src")
            build = os.path.join(tmpdir, "build")
            templates = os.path.join(tmpdir, "templates")
            os.makedirs(src)
            os.makedirs(templates)

            with open(os.path.join(templates, "blog.html"), 'w') as f:
                f.write("<article>{{ content }}</article>")

            with open(os.path.join(src, "post.md"), 'w') as f:
                f.write("---\ntemplate: blog.html\n---\n# Blog Post")

            sb = SiteBuilder(src, build, templates)
            result = sb.build()
            assert result.pages_built == 1

            with open(os.path.join(build, "post.html"), 'r') as f:
                html = f.read()
            assert "<article>" in html


class TestAssetCopying:
    """Asset copying (CSS, images) from source to build."""

    def test_copies_css_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "src")
            build = os.path.join(tmpdir, "build")
            templates = os.path.join(tmpdir, "templates")
            os.makedirs(src)
            os.makedirs(templates)

            with open(os.path.join(src, "style.css"), 'w') as f:
                f.write("body { color: red; }")

            sb = SiteBuilder(src, build, templates)
            sb.build()
            assert os.path.exists(os.path.join(build, "style.css"))

    def test_copies_image_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "src")
            build = os.path.join(tmpdir, "build")
            templates = os.path.join(tmpdir, "templates")
            os.makedirs(src)
            os.makedirs(templates)

            with open(os.path.join(src, "logo.png"), 'wb') as f:
                f.write(b'\x89PNG')

            sb = SiteBuilder(src, build, templates)
            sb.build()
            assert os.path.exists(os.path.join(build, "logo.png"))


class TestBuildErrors:
    """BuildResult.errors collects errors during build."""

    def test_missing_template_recorded_as_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "src")
            build = os.path.join(tmpdir, "build")
            templates = os.path.join(tmpdir, "templates")
            os.makedirs(src)
            os.makedirs(templates)

            with open(os.path.join(src, "index.md"), 'w') as f:
                f.write("---\ntemplate: nonexistent.html\n---\n# Hello")

            sb = SiteBuilder(src, build, templates)
            result = sb.build()
            assert len(result.errors) > 0


class TestBuilderDocstrings:
    """Verify public API has documentation."""

    def test_sitebuilder_has_docstring(self):
        assert SiteBuilder.__doc__ is not None

    def test_build_has_docstring(self):
        assert SiteBuilder.build.__doc__ is not None

    def test_buildresult_has_docstring(self):
        assert BuildResult.__doc__ is not None

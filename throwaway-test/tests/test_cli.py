"""Tests for sitegen.cli — Command-line interface.

Tests written FIRST per TDD requirement. Each test covers
a specific feature from the Brief's Phase 4 specification.
"""

import sys
import os
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sitegen.cli import main


class TestBuildCommand:
    """sitegen build [--source DIR] [--output DIR] [--templates DIR]."""

    def test_build_with_defaults(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "source")
            out = os.path.join(tmpdir, "build")
            tpl = os.path.join(tmpdir, "templates")
            os.makedirs(src)
            os.makedirs(tpl)

            with open(os.path.join(tpl, "default.html"), 'w') as f:
                f.write("<html>{{ content }}</html>")
            with open(os.path.join(src, "index.md"), 'w') as f:
                f.write("---\ntemplate: default.html\n---\n# Hello")

            exit_code = main(["build", "--source", src, "--output", out, "--templates", tpl])
            assert exit_code == 0
            assert os.path.exists(os.path.join(out, "index.html"))

    def test_build_returns_nonzero_on_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "nonexistent_source")
            out = os.path.join(tmpdir, "build")
            tpl = os.path.join(tmpdir, "templates")

            exit_code = main(["build", "--source", src, "--output", out, "--templates", tpl])
            assert exit_code != 0


class TestCleanCommand:
    """sitegen clean [--output DIR]."""

    def test_clean_removes_build_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "build")
            os.makedirs(out)
            with open(os.path.join(out, "file.html"), 'w') as f:
                f.write("content")

            exit_code = main(["clean", "--output", out])
            assert exit_code == 0
            assert not os.path.exists(out)

    def test_clean_nonexistent_dir_succeeds(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "nonexistent")
            exit_code = main(["clean", "--output", out])
            assert exit_code == 0


class TestServeCommand:
    """sitegen serve [--output DIR] [--port PORT] — stub, print message only."""

    def test_serve_returns_zero(self):
        exit_code = main(["serve", "--output", "/tmp/build", "--port", "8000"])
        assert exit_code == 0

    def test_serve_is_stub(self, capsys):
        main(["serve", "--output", "/tmp/build"])
        captured = capsys.readouterr()
        assert len(captured.out) > 0  # Should print a message


class TestUnknownCommand:
    """Unknown command returns non-zero exit code."""

    def test_unknown_command(self):
        exit_code = main(["unknown"])
        assert exit_code != 0


class TestMainDocstring:
    """Verify main function has documentation."""

    def test_main_has_docstring(self):
        assert main.__doc__ is not None

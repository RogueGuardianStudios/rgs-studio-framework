"""Tests for sitegen.cli — Command-line interface."""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sitegen.cli import main


class TestBuildCommand:
    """Test the 'build' subcommand."""

    def test_build_returns_zero_on_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = os.path.join(tmpdir, "source")
            build = os.path.join(tmpdir, "build")
            templates = os.path.join(tmpdir, "templates")
            os.makedirs(source)
            os.makedirs(templates)

            with open(os.path.join(source, "index.md"), "w") as f:
                f.write("# Hello")
            with open(os.path.join(templates, "default.html"), "w") as f:
                f.write("{{ content }}")

            exit_code = main([
                "build",
                "--source", source,
                "--output", build,
                "--templates", templates,
            ])
            assert exit_code == 0
            assert os.path.exists(os.path.join(build, "index.html"))

    def test_build_returns_nonzero_on_errors(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = os.path.join(tmpdir, "source")
            build = os.path.join(tmpdir, "build")
            templates = os.path.join(tmpdir, "templates")
            os.makedirs(source)
            os.makedirs(templates)
            # No default template — will cause error

            with open(os.path.join(source, "page.md"), "w") as f:
                f.write("# Hello")

            exit_code = main([
                "build",
                "--source", source,
                "--output", build,
                "--templates", templates,
            ])
            assert exit_code == 1

    def test_build_uses_defaults(self):
        """build without args should use default directory names without crashing."""
        # This will likely fail because default dirs don't exist,
        # but it should not raise an unhandled exception.
        exit_code = main(["build"])
        # Exit code 1 is acceptable (source dir doesn't exist)
        assert exit_code in (0, 1)


class TestCleanCommand:
    """Test the 'clean' subcommand."""

    def test_clean_removes_build_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            build = os.path.join(tmpdir, "build")
            os.makedirs(build)
            with open(os.path.join(build, "file.html"), "w") as f:
                f.write("old")

            exit_code = main(["clean", "--output", build])
            assert exit_code == 0
            assert not os.path.exists(build)

    def test_clean_nonexistent_dir_returns_zero(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            build = os.path.join(tmpdir, "nonexistent")
            exit_code = main(["clean", "--output", build])
            assert exit_code == 0


class TestServeCommand:
    """Test the 'serve' subcommand (stub — print only)."""

    def test_serve_returns_zero(self, capsys):
        exit_code = main(["serve"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "serve" in captured.out.lower() or "not implemented" in captured.out.lower()

    def test_serve_with_port(self, capsys):
        exit_code = main(["serve", "--port", "9000"])
        assert exit_code == 0


class TestNoCommand:
    """Test invocation with no subcommand or unknown subcommand."""

    def test_no_args_returns_nonzero(self):
        exit_code = main([])
        assert exit_code != 0

    def test_unknown_command_returns_nonzero(self):
        exit_code = main(["deploy"])
        assert exit_code != 0

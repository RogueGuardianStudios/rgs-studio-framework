"""Tests for sitegen.cli module.

Tests the public API:
- main(args: list[str]) -> int -- returns exit code

Covers: build command, clean command, serve command (stub).
"""

import os
import pytest
import tempfile
import shutil
from sitegen.cli import main


@pytest.fixture
def cli_dirs():
    """Create temporary directories for CLI testing."""
    tmpdir = tempfile.mkdtemp()
    source_dir = os.path.join(tmpdir, "source")
    build_dir = os.path.join(tmpdir, "build")
    template_dir = os.path.join(tmpdir, "templates")
    os.makedirs(source_dir)
    os.makedirs(template_dir)

    # Write a default template
    with open(os.path.join(template_dir, "default.html"), "w") as f:
        f.write("<html><body>{{ content }}</body></html>")

    # Write a source markdown file
    with open(os.path.join(source_dir, "index.md"), "w") as f:
        f.write("---\ntemplate: default.html\ntitle: Home\n---\n# Welcome\n")

    yield source_dir, build_dir, template_dir
    shutil.rmtree(tmpdir)


class TestMainReturnType:
    """Verify main returns an int exit code."""

    def test_returns_int(self, cli_dirs):
        source_dir, build_dir, template_dir = cli_dirs
        result = main(["build", "--source", source_dir, "--output", build_dir,
                        "--templates", template_dir])
        assert isinstance(result, int)


class TestBuildCommand:
    """Test sitegen build [--source DIR] [--output DIR] [--templates DIR]."""

    def test_build_creates_output(self, cli_dirs):
        source_dir, build_dir, template_dir = cli_dirs
        exit_code = main(["build", "--source", source_dir, "--output", build_dir,
                          "--templates", template_dir])
        assert exit_code == 0
        assert os.path.exists(os.path.join(build_dir, "index.html"))

    def test_build_returns_zero_on_success(self, cli_dirs):
        source_dir, build_dir, template_dir = cli_dirs
        exit_code = main(["build", "--source", source_dir, "--output", build_dir,
                          "--templates", template_dir])
        assert exit_code == 0


class TestCleanCommand:
    """Test sitegen clean [--output DIR]."""

    def test_clean_removes_build_dir(self, cli_dirs):
        source_dir, build_dir, template_dir = cli_dirs
        os.makedirs(build_dir, exist_ok=True)
        with open(os.path.join(build_dir, "old.html"), "w") as f:
            f.write("stale")

        exit_code = main(["clean", "--output", build_dir])
        assert exit_code == 0
        # Build dir should be removed or empty
        assert not os.path.exists(build_dir) or len(os.listdir(build_dir)) == 0

    def test_clean_returns_zero(self, cli_dirs):
        source_dir, build_dir, template_dir = cli_dirs
        os.makedirs(build_dir, exist_ok=True)
        exit_code = main(["clean", "--output", build_dir])
        assert exit_code == 0


class TestServeCommand:
    """Test sitegen serve [--output DIR] [--port PORT] (stub)."""

    def test_serve_returns_zero(self, cli_dirs, capsys):
        source_dir, build_dir, template_dir = cli_dirs
        os.makedirs(build_dir, exist_ok=True)
        exit_code = main(["serve", "--output", build_dir, "--port", "8080"])
        assert exit_code == 0

    def test_serve_prints_message(self, cli_dirs, capsys):
        source_dir, build_dir, template_dir = cli_dirs
        os.makedirs(build_dir, exist_ok=True)
        main(["serve", "--output", build_dir, "--port", "8080"])
        captured = capsys.readouterr()
        assert len(captured.out) > 0  # Stub prints a message


class TestUnknownCommand:
    """Test behavior with unknown or missing commands."""

    def test_no_args_returns_nonzero(self):
        exit_code = main([])
        assert exit_code != 0

    def test_unknown_command_returns_nonzero(self):
        exit_code = main(["unknown"])
        assert exit_code != 0

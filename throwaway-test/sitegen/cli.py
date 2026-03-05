"""Command-line interface for the sitegen static site generator.

Provides build, clean, and serve commands for managing a static site.
"""

import argparse
import os
import shutil
from sitegen.builder import SiteBuilder


def main(args: list[str]) -> int:
    """Entry point for the sitegen CLI.

    Args:
        args: Command-line arguments (without the program name).

    Returns:
        An integer exit code. 0 indicates success, non-zero indicates failure.
    """
    parser = argparse.ArgumentParser(prog="sitegen", description="Static site generator")
    subparsers = parser.add_subparsers(dest="command")

    # build command
    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--source", default="source", help="Source directory")
    build_parser.add_argument("--output", default="build", help="Output directory")
    build_parser.add_argument("--templates", default="templates", help="Templates directory")

    # clean command
    clean_parser = subparsers.add_parser("clean")
    clean_parser.add_argument("--output", default="build", help="Output directory to clean")

    # serve command (stub)
    serve_parser = subparsers.add_parser("serve")
    serve_parser.add_argument("--output", default="build", help="Output directory to serve")
    serve_parser.add_argument("--port", default="8000", help="Port to serve on")

    try:
        parsed = parser.parse_args(args)
    except SystemExit:
        return 1

    if parsed.command is None:
        parser.print_help()
        return 1

    if parsed.command == "build":
        return _cmd_build(parsed)
    elif parsed.command == "clean":
        return _cmd_clean(parsed)
    elif parsed.command == "serve":
        return _cmd_serve(parsed)

    return 1


def _cmd_build(parsed) -> int:
    """Execute the build command.

    Args:
        parsed: Parsed arguments containing source, output, and templates paths.

    Returns:
        Exit code (0 for success).
    """
    builder = SiteBuilder(parsed.source, parsed.output, parsed.templates)
    result = builder.build()
    if result.errors:
        for error in result.errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Built {result.pages_built} pages.")
    return 0


def _cmd_clean(parsed) -> int:
    """Execute the clean command.

    Args:
        parsed: Parsed arguments containing the output path.

    Returns:
        Exit code (0 for success).
    """
    if os.path.exists(parsed.output):
        shutil.rmtree(parsed.output)
    print(f"Cleaned {parsed.output}.")
    return 0


def _cmd_serve(parsed) -> int:
    """Execute the serve command (stub -- prints message only).

    Args:
        parsed: Parsed arguments containing output path and port.

    Returns:
        Exit code (0 for success).
    """
    print(f"Serve is a stub. Would serve {parsed.output} on port {parsed.port}.")
    return 0

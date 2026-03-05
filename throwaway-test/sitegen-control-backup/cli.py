"""Command-line interface for the sitegen static site generator.

Provides ``build``, ``clean``, and ``serve`` subcommands for managing
a static site. Designed to be invoked via ``main(args)``.
"""

import argparse
import os
import shutil
import sys

from sitegen.builder import SiteBuilder


def main(args: list[str]) -> int:
    """Entry point for the sitegen CLI.

    Args:
        args: Command-line arguments (excluding the program name).
            Typically ``sys.argv[1:]``.

    Returns:
        An integer exit code. 0 indicates success, non-zero indicates failure.

    Subcommands:
        build:
            Build the site from markdown sources.
            Options: ``--source DIR``, ``--output DIR``, ``--templates DIR``.

        clean:
            Remove the build output directory.
            Options: ``--output DIR``.

        serve:
            Stub command. Prints a message indicating the feature is not
            yet implemented.
            Options: ``--output DIR``, ``--port PORT``.
    """
    parser = argparse.ArgumentParser(prog="sitegen", description="Static site generator", exit_on_error=False)
    subparsers = parser.add_subparsers(dest="command")

    # build
    build_parser = subparsers.add_parser("build", help="Build the site")
    build_parser.add_argument("--source", default="source", help="Source directory (default: source)")
    build_parser.add_argument("--output", default="build", help="Output directory (default: build)")
    build_parser.add_argument("--templates", default="templates", help="Templates directory (default: templates)")

    # clean
    clean_parser = subparsers.add_parser("clean", help="Remove the build directory")
    clean_parser.add_argument("--output", default="build", help="Output directory to remove (default: build)")

    # serve
    serve_parser = subparsers.add_parser("serve", help="Serve the site (stub)")
    serve_parser.add_argument("--output", default="build", help="Output directory to serve (default: build)")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port number (default: 8000)")

    try:
        parsed = parser.parse_args(args)
    except argparse.ArgumentError:
        parser.print_help()
        return 2

    if parsed.command is None:
        parser.print_help()
        return 2

    if parsed.command == "build":
        return _cmd_build(parsed)
    elif parsed.command == "clean":
        return _cmd_clean(parsed)
    elif parsed.command == "serve":
        return _cmd_serve(parsed)

    parser.print_help()
    return 2


def _cmd_build(parsed: argparse.Namespace) -> int:
    """Execute the build subcommand."""
    source = parsed.source
    output = parsed.output
    templates = parsed.templates

    if not os.path.isdir(source):
        print(f"Error: source directory '{source}' does not exist.", file=sys.stderr)
        return 1

    if not os.path.isdir(templates):
        print(f"Error: templates directory '{templates}' does not exist.", file=sys.stderr)
        return 1

    builder = SiteBuilder(source, output, templates)
    result = builder.build()

    print(f"Built {result.pages_built} page(s).")
    if result.errors:
        for err in result.errors:
            print(f"  ERROR: {err}", file=sys.stderr)
        return 1

    return 0


def _cmd_clean(parsed: argparse.Namespace) -> int:
    """Execute the clean subcommand."""
    output = parsed.output
    if os.path.exists(output):
        shutil.rmtree(output)
        print(f"Removed '{output}'.")
    else:
        print(f"Nothing to clean — '{output}' does not exist.")
    return 0


def _cmd_serve(parsed: argparse.Namespace) -> int:
    """Execute the serve subcommand (stub)."""
    print(f"Serve is not implemented yet. Would serve '{parsed.output}' on port {parsed.port}.")
    return 0

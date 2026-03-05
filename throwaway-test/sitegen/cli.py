"""sitegen.cli — Command-line interface for the static site generator.

Provides build, clean, and serve commands for the sitegen library.
"""

import os
import shutil
import argparse

from sitegen.builder import SiteBuilder


def main(args: list) -> int:
    """Execute the sitegen command-line interface.

    Supports three commands:
    - build: Build the site from source markdown to output HTML.
    - clean: Remove the output build directory.
    - serve: Stub that prints a message (not implemented).

    Args:
        args: List of command-line argument strings.

    Returns:
        Exit code: 0 for success, non-zero for failure.
    """
    parser = argparse.ArgumentParser(prog="sitegen", exit_on_error=False)
    subparsers = parser.add_subparsers(dest="command")

    # build command
    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--source", default="source")
    build_parser.add_argument("--output", default="build")
    build_parser.add_argument("--templates", default="templates")

    # clean command
    clean_parser = subparsers.add_parser("clean")
    clean_parser.add_argument("--output", default="build")

    # serve command
    serve_parser = subparsers.add_parser("serve")
    serve_parser.add_argument("--output", default="build")
    serve_parser.add_argument("--port", default="8000")

    try:
        parsed = parser.parse_args(args)
    except (argparse.ArgumentError, SystemExit):
        print("Unknown command. Use: build, clean, or serve.")
        return 1

    if parsed.command == "build":
        if not os.path.exists(parsed.source):
            print(f"Error: source directory not found: {parsed.source}")
            return 1
        builder = SiteBuilder(parsed.source, parsed.output, parsed.templates)
        result = builder.build()
        if result.errors:
            for error in result.errors:
                print(f"Error: {error}")
            return 1
        print(f"Built {result.pages_built} pages.")
        return 0

    elif parsed.command == "clean":
        if os.path.exists(parsed.output):
            shutil.rmtree(parsed.output)
        print(f"Cleaned {parsed.output}.")
        return 0

    elif parsed.command == "serve":
        print(f"Serve not implemented. Would serve {parsed.output} on port {parsed.port}.")
        return 0

    else:
        print("Unknown command. Use: build, clean, or serve.")
        return 1

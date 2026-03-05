"""Template engine with variable substitution, includes, and conditionals.

Provides a simple template system for rendering HTML pages with
dynamic content. Supports variable substitution, file includes,
and conditional blocks.
"""

import os
import re


class Template:
    """A renderable template with variable substitution, includes, and conditionals.

    Args:
        template_string: The raw template string containing directives.

    Template syntax:
        - ``{{ variable_name }}`` — replaced with the value from the context dict.
          Missing variables render as empty strings.
        - ``{% include "filename" %}`` — replaced with the contents of the named file.
        - ``{% if variable %}...{% endif %}`` — block is rendered only if the variable
          is truthy in the context.
        - ``{{ content }}`` — conventionally used for the parsed markdown body,
          but treated identically to any other variable.
    """

    def __init__(self, template_string: str) -> None:
        self._template_string = template_string

    def render(self, context: dict, include_dir: str = "") -> str:
        """Render the template with the given context.

        Args:
            context: A dictionary mapping variable names to their values.
            include_dir: Directory to resolve include directives against.
                If empty, includes that reference files will produce empty strings.

        Returns:
            The fully rendered string with all directives resolved.
        """
        text = self._template_string

        # Process includes first
        text = self._process_includes(text, include_dir)

        # Process conditionals
        text = self._process_conditionals(text, context)

        # Process variable substitution
        text = self._process_variables(text, context)

        return text

    def _process_includes(self, text: str, include_dir: str) -> str:
        """Replace {% include "filename" %} with file contents."""
        def replace_include(match: re.Match) -> str:
            filename = match.group(1)
            filepath = os.path.join(include_dir, filename) if include_dir else filename
            try:
                with open(filepath, "r") as f:
                    return f.read()
            except (FileNotFoundError, IsADirectoryError):
                return ""

        return re.sub(r'\{%\s*include\s+"([^"]+)"\s*%\}', replace_include, text)

    def _process_conditionals(self, text: str, context: dict) -> str:
        """Process {% if variable %}...{% endif %} blocks."""
        def replace_conditional(match: re.Match) -> str:
            var_name = match.group(1).strip()
            body = match.group(2)
            if context.get(var_name):
                # Process variables inside the conditional body
                return self._process_variables(body, context)
            return ""

        return re.sub(
            r"\{%\s*if\s+(\w+)\s*%\}(.*?)\{%\s*endif\s*%\}",
            replace_conditional,
            text,
            flags=re.DOTALL,
        )

    def _process_variables(self, text: str, context: dict) -> str:
        """Replace {{ variable_name }} with context values."""
        def replace_var(match: re.Match) -> str:
            var_name = match.group(1).strip()
            value = context.get(var_name, "")
            return str(value)

        return re.sub(r"\{\{\s*(\w+)\s*\}\}", replace_var, text)


def load_template(filepath: str) -> Template:
    """Load a template from a file on disk.

    Args:
        filepath: Absolute or relative path to the template file.

    Returns:
        A Template instance initialized with the file's contents.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    with open(filepath, "r") as f:
        return Template(f.read())

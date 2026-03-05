"""Template engine for the sitegen static site generator.

Applies HTML templates with variable substitution, include directives,
conditional blocks, and content insertion.
"""

import re
import os


class Template:
    """An HTML template that supports variable substitution, includes,
    and conditional blocks.

    Args:
        template_string: A string containing the template markup.
    """

    def __init__(self, template_string: str):
        self._template_string = template_string

    def render(self, context: dict, include_dir: str = None) -> str:
        """Render the template with the given context dictionary.

        Args:
            context: A dictionary mapping variable names to their values.
            include_dir: Optional directory path to resolve include directives.

        Returns:
            A string containing the rendered HTML.
        """
        result = self._template_string

        # Process include directives: {% include "filename" %}
        result = self._process_includes(result, include_dir)

        # Process conditional blocks: {% if variable %}...{% endif %}
        result = self._process_conditionals(result, context)

        # Process variable substitution: {{ variable_name }}
        result = self._process_variables(result, context)

        return result

    def _process_includes(self, text: str, include_dir: str) -> str:
        """Process {% include "filename" %} directives.

        Args:
            text: Template text potentially containing include directives.
            include_dir: Directory to load included files from.

        Returns:
            Text with include directives replaced by file contents.
        """
        def replace_include(match):
            filename = match.group(1)
            if include_dir is None:
                return ""
            filepath = os.path.join(include_dir, filename)
            with open(filepath, "r") as f:
                return f.read()

        return re.sub(r'\{%\s*include\s+"([^"]+)"\s*%\}', replace_include, text)

    def _process_conditionals(self, text: str, context: dict) -> str:
        """Process {% if variable %}...{% endif %} blocks.

        Args:
            text: Template text potentially containing conditional blocks.
            context: Context dictionary to evaluate conditions against.

        Returns:
            Text with conditional blocks resolved.
        """
        def replace_conditional(match):
            variable = match.group(1).strip()
            content = match.group(2)
            if context.get(variable):
                return content
            return ""

        return re.sub(
            r'\{%\s*if\s+(\w+)\s*%\}(.*?)\{%\s*endif\s*%\}',
            replace_conditional,
            text,
            flags=re.DOTALL,
        )

    def _process_variables(self, text: str, context: dict) -> str:
        """Process {{ variable_name }} substitutions.

        Args:
            text: Template text potentially containing variable placeholders.
            context: Context dictionary to substitute values from.

        Returns:
            Text with variable placeholders replaced by their values.
        """
        def replace_var(match):
            var_name = match.group(1).strip()
            return str(context.get(var_name, ""))

        return re.sub(r'\{\{\s*(\w+)\s*\}\}', replace_var, text)


def load_template(filepath: str) -> Template:
    """Load a template from a file.

    Args:
        filepath: Path to the template file.

    Returns:
        A Template instance constructed from the file contents.
    """
    with open(filepath, "r") as f:
        return Template(f.read())

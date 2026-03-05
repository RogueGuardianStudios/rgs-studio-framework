"""sitegen.templates — HTML template engine with variable substitution.

Supports variable substitution, include directives, conditional blocks,
and content insertion for parsed markdown bodies.
"""

import re


class Template:
    """An HTML template with variable substitution support.

    Supports {{ variable }} substitution, {% include "file" %} directives,
    and {% if variable %}...{% endif %} conditional blocks.
    """

    def __init__(self, template_string: str):
        """Initialize a Template with the given template string.

        Args:
            template_string: Raw template content with directives.
        """
        self._template_string = template_string

    def render(self, context: dict) -> str:
        """Render the template with the given context dictionary.

        Args:
            context: Dictionary of variable names to values for substitution.

        Returns:
            Rendered HTML string with all directives resolved.
        """
        result = self._template_string

        # Process include directives
        def replace_include(match):
            filepath = match.group(1)
            with open(filepath, 'r') as f:
                return f.read()

        result = re.sub(r'\{%\s*include\s+"([^"]+)"\s*%\}', replace_include, result)

        # Process conditional blocks
        def replace_conditional(match):
            var_name = match.group(1)
            content = match.group(2)
            if context.get(var_name):
                return content
            return ""

        result = re.sub(
            r'\{%\s*if\s+(\w+)\s*%\}(.*?)\{%\s*endif\s*%\}',
            replace_conditional,
            result,
            flags=re.DOTALL
        )

        # Process variable substitution
        def replace_variable(match):
            var_name = match.group(1).strip()
            return str(context.get(var_name, ""))

        result = re.sub(r'\{\{\s*(\w+)\s*\}\}', replace_variable, result)

        return result


def load_template(filepath: str) -> Template:
    """Load a Template from a file on disk.

    Args:
        filepath: Path to the template file.

    Returns:
        A Template instance initialized with the file's contents.
    """
    with open(filepath, 'r') as f:
        return Template(f.read())

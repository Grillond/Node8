"""GDScript code style rules.

Code that violate Godot code style guidelines will be errored.
For example:
>>> func undocumented_function() -> void:
>>>     pass

Will be an error since it misses documentation comments.
"""

from pathlib import Path
from typing import Any, Final

from lark import Token, Tree

from node8.core.config import Config
from node8.models.errors import Error, ScriptError
from node8.services.visitors import Visitor

LINE_TOO_LONG_CODENAME: Final[str] = "E001"
LINE_TOO_LONG_MESSAGE: Final[str] = "line too long"

FUNCTION_MISSING_DOCS_CODENAME: Final[str] = "D001"
FUNCTION_MISSING_DOCS_MESSAGE: Final[str] = (
    "Missing docstring in public function"
)

class LineTooLong:
    """E001 rule file parser."""

    def __init__(
            self,
            path: Path,
            config: Config | None = None,
    ) -> None:
        """Initialize LineTooLong class.

        :param path: Script file path.
        :param config: Linter configuration.
        """
        config = config or Config()

        self.config = Config()
        self.errors: list[ScriptError] = []
        self.path = path

    def validate_lines(self) -> list[ScriptError]:
        """Check given path for line too long errors.

        :returns: List of errors found.
        """
        with self.path.open(mode="r", encoding="utf-8") as script:
            lines: list[str] = script.readlines()
        for index, line in enumerate(map(str.rstrip, lines), start=1):
            if len(line) > self.config.line_length:
                self.errors.append(ScriptError(
                    error=Error(
                        codename=LINE_TOO_LONG_CODENAME,
                        message=(
                            f"{LINE_TOO_LONG_MESSAGE} " # noqa: WPS237
                            f"({len(line)} > "
                            f"{self.config.line_length})"
                        ),
                    ),
                    path=self.path,
                    line=index,
                    column=self.config.line_length,
                    end_column=len(line) + 1,
                ))
        return self.errors

    @classmethod
    def check(
            cls,
            path: Path,
            config: Config | None = None,
    ) -> list[ScriptError]:
        """Check given file for long lines without initializing class.

        :param path: Script file path.
        :param config: Linter configuration.
        :returns: List of errors found.
        """
        config = config or Config()

        checker = cls(path, config)

        return checker.validate_lines()


class FunctionMissingDocstring(Visitor):
    """D001 rule tree visitor."""

    @classmethod
    def check(
            cls,
            path: Path,
            tree: Tree[Any],
            comment_tree: Tree[Any],
            config: Config | None = None,
    ) -> list[ScriptError]:
        """Visit given tree without initializing class.

        :param path: Script file path.
        :param tree: Tree to visit.
        :param comment_tree: Comment tree to parse documentation from.
        :param config: Linter configuration.
        :returns: List of errors found.
        """
        visitor = cls(path, comment_tree, config=config)
        visitor.visit(tree)
        return visitor.errors

    def func_header(self, tree: Tree[Any]) -> None:
        """Ensure given function is not missing documentation comments."""
        name = tree.children[0]

        if not isinstance(name, Token):
            return
        if str(name).startswith("_"):
            return

        docstrings: list[Token] = []
        for comment in self.comment_tree.children:
            if not isinstance(comment, Token):
                continue
            if str(comment).startswith("##"):
                docstrings.append(comment)

        if any(
            docstring.line == tree.meta.line - 1 for docstring in docstrings
        ):
            return

        column = name.column
        end_column = name.end_column

        if column is None:
            column = tree.meta.column

        if end_column is None:
            end_column = tree.meta.end_column

        self.errors.append(ScriptError(
            error=Error(
                codename=FUNCTION_MISSING_DOCS_CODENAME,
                message=FUNCTION_MISSING_DOCS_MESSAGE,
            ),
            path=self.path,
            line=tree.meta.line,
            column=column,
            end_column=end_column,
        ))

"""Provide base tree visitor classes to use in linting rule implementations."""

from pathlib import Path
from typing import Any

from lark import Tree
from lark.visitors import Visitor_Recursive

from node8.core.config import Config
from node8.models.errors import ScriptError


class Visitor(Visitor_Recursive[Tree[Any]]):
    """Base visitor class for rule visitors.

    Walks GDScript syntax tree and appends errors when found.
    """

    def __init__(
            self,
            path: Path,
            comment_tree: Tree[Any],
            config: Config | None = None,
    ) -> None:
        """Initialize Visitor class.

        :param path: Script file path.
        :param config: Linter configuration.
        """
        super().__init__()

        self.path = path
        self.comment_tree = comment_tree
        self.config = config or Config()
        self.errors: list[ScriptError] = []

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
        :param config: Linter configuration.
        :returns: List of errors found.
        """
        visitor = cls(path, comment_tree, config=config)
        visitor.visit(tree)
        return visitor.errors

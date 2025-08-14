"""Provide ignore tools for 'noqa' to silence specified linter errors."""

from pathlib import Path
from typing import Any

from gdtoolkit.parser import parser  # type: ignore[import-untyped]
from lark import Token, Tree

from node8.models.noqa import NoqaIgnore


def _get_ignore_token(comment: Token) -> NoqaIgnore | None:
    """Parse comment token for `noqa` keyword.

    :param comment: Comment token to parse.
    :returns: None if `noqa` was not found, noqa ignore model otherwise.
    """
    if comment.line is None:
        return None

    comment_text = str(comment).lstrip("# ").split()
    if len(comment_text) <= 0:
        return None

    first = comment_text.pop(0)

    if first == "noqa":
        return NoqaIgnore(line=comment.line, ignore_all=True)
    if first != "noqa:":
        return None

    ignores: list[str] = []
    for word in comment_text:
        ignores.append(word.removesuffix(","))
        if not word.endswith(","):
            break
    return NoqaIgnore(line=comment.line, ignores=ignores)


def get_ignores_tree(comment_tree: Tree[Any]) -> list[NoqaIgnore]:
    """Get noqa ignores using script comment tree.

    :param comment_tree: Comment tree of a script.
    :returns: An array of noqa ignores.
    """
    noqa_ignores: list[NoqaIgnore] = []

    for comment in comment_tree.children:
        if not isinstance(comment, Token):
            continue
        noqa_ignore = _get_ignore_token(comment)
        if noqa_ignore is not None:
            noqa_ignores.append(noqa_ignore)

    return noqa_ignores


def get_ignores_path(path: Path) -> list[NoqaIgnore]:
    """Get noqa ignores from specified path.

    :param path: Path to get ignores from.
    :returns: An array of noqa ignores.
    """
    with path.open(mode="r", encoding="utf-8") as script:
        script_contents = script.read()
    tree: Tree[Any] = parser.parse_comments(script_contents)
    return get_ignores_tree(tree)

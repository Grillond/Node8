"""Provide GDScript linting functions to check for rule violations."""

from pathlib import Path
from typing import Any

from gdtoolkit.parser import parser  # type: ignore[import-untyped]
from lark import Tree

from node8.core.config import Config
from node8.models.errors import ScriptError
from node8.models.noqa import NoqaIgnore
from node8.services.format import print_script_errors
from node8.services.noqa import get_ignores_tree
from node8.services.rules.anti_patterns import GetNodeFound
from node8.services.rules.style_violations import (
    FunctionMissingDocstring,
    LineTooLong,
)


def check(paths: list[str]) -> None:
    """Lint given paths and print errors.

    Loads the first `gdproject.toml` config.

    :param paths: Paths to lint.
    """
    for path in map(Path, paths):
        config = Config.from_toml(path)
        errors = directory_check(path, config=config)
        print_script_errors(errors, config=config)


def _is_valid_error(
        error: ScriptError,
        noqa_ignores: list[NoqaIgnore],
        config: Config | None = None,
) -> bool:
    """Check if given error is ignored by `noqa` or config.

    :param error: Error to check.
    :param noqa_ignores: Noqa ignores array.
    :param config: Linter configuration.
    :returns: True if error is not ignored, False otherwise.
    """
    config = config or Config()
    codename = error.error.codename
    if codename in config.ignores:
        return False
    for noqa in noqa_ignores:
        if (
            noqa.line == error.line
            and (noqa.ignore_all or codename in noqa.ignores)
        ):
            return False
    return True


def _check_script( # noqa: WPS210
        path: Path,
        config: Config | None = None,
) -> list[ScriptError]:
    """Check given script and return errors.

    :param path: Path to script.
    :param config: Linter configuration.
    :returns: Array of script errors.
    """
    config = config or Config()

    errors: list[ScriptError] = []

    with path.open(mode="r", encoding="utf-8") as script:
        script_contents = script.read()

    syntax_tree: Tree[Any] = parser.parse(script_contents, gather_metadata=True)
    comment_tree: Tree[Any] = parser.parse_comments(script_contents)
    noqa_ignores = get_ignores_tree(comment_tree)

    errors.extend(GetNodeFound.check(
        path,
        syntax_tree,
        comment_tree,
        config=config,
    ))
    errors.extend(FunctionMissingDocstring.check(
        path,
        syntax_tree,
        comment_tree,
        config=config,
    ))
    errors.extend(LineTooLong.check(path, config=config))

    return [
        error for error in errors
        if _is_valid_error(error, noqa_ignores, config=config)
    ]


def directory_check(
        directory: Path,
        config: Config | None = None,
) -> list[ScriptError]:
    """Lint given paths and return errors.

    :param directory: Directory to check.
    :param config: Linter configuration.
    :returns: Array of script errors.
    """
    config = config or Config()

    errors: list[ScriptError] = []
    for path in directory.rglob("*.gd"):
        errors.extend(_check_script(path, config=config))

    return errors

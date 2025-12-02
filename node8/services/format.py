"""Provide error formatting and printing functions."""

from typing import Final

import rich

from node8.core.config import Config
from node8.models.errors import SceneError, ScriptError
from node8.services.scene_tree import SceneTree, get_subtree_path

MIN_LINE: Final[int] = 1
LINE_NUMBER_OFFSET: Final[int] = 1
TREE_DEFAULT_INDENT: Final[str] = "└── "


def _print_script_error_header(
    error: ScriptError,
    config: Config | None = None,
) -> None:
    """Print formatted script error header.

    :param error: Script error to print.
    :param config: Linter configuration.
    """
    config = config or Config()
    rich.print(
        f"[bold white]{error.path}[/]"  # noqa: WPS237
        f"[{config.main_color}]:[/]"
        f"[bold white]{error.line}[/]"
        f"[{config.main_color}]:[/]"
        f"[bold white]{error.column}[/]"
        f"[{config.main_color}]:[/] "
        f"[bold {config.accent_color}]"  # noqa: WPS226
        f"{error.error.codename}[/] "
        f"[white]{error.error.message}[/] ",
    )


def _print_script_error_body(  # noqa: WPS210
    error: ScriptError,
    config: Config | None = None,
) -> None:
    """Print formatted script error body.

    :param error: Script error to print.
    :param config: Linter configuration.
    """
    config = config or Config()

    with error.path.open(mode="r", encoding="utf-8") as script:
        script_lines = script.readlines()

    start_line = max(error.line - config.lines_show_before, MIN_LINE)
    end_line = min(error.line + config.lines_show_after, len(script_lines))
    spaces = len(str(end_line)) + LINE_NUMBER_OFFSET

    rich.print(
        f"[bold {config.main_color}]{' ' * (spaces)} |[/]",  # noqa: WPS237, WPS226
    )

    for line in range(start_line, end_line + 1):
        rich.print(
            f"[bold {config.main_color}]{line: < {spaces}} | [/]"  # noqa: WPS237
            f"[white]{script_lines[line - 1].rstrip()}[/]",
        )
        if line == error.line:
            rich.print(
                f"[bold {config.main_color}]"  # noqa: WPS237
                f"{' ' * spaces} |[/]"
                f"{' ' * error.column}"
                f"[bold {config.accent_color}]"
                f"{'^' * (error.end_column - error.column)}"
                f" {error.error.codename}[/]",
            )

    rich.print(
        f"[bold {config.main_color}]{' ' * (spaces)} |[/]",  # noqa: WPS237
    )
    if error.error.help_message is not None:
        rich.print(
            f"{' ' * spaces} [bold {config.main_color}]= help: "  # noqa: WPS237
            f"{error.error.help_message}[/]",
        )


def print_script_error(
    error: ScriptError,
    config: Config | None = None,
) -> None:
    """Print formatted script error.

    :param error: Script error to print.
    :param config: Linter configuration.
    """
    config = config or Config()
    _print_script_error_header(error, config=config)
    _print_script_error_body(error, config=config)


def _print_error_tree(
    error: SceneError,
    tree: SceneTree,
    config: Config | None = None,
    depth: int = 0,
) -> None:
    """"""
    config = config or Config()

    rich.print(f"[bold {config.main_color}] | [/]", end="")
    if len(tree.children) > 0:
        if depth > 0:
            rich.print(
                f"{' ' * (depth - 1) * len(TREE_DEFAULT_INDENT)}"
                f"[bold white]{TREE_DEFAULT_INDENT}[/]",
                end="",
            )
        rich.print(f"[bold white]{tree.node_meta.name}[/]")
        for child in tree.children:
            if isinstance(child, SceneTree):
                _print_error_tree(
                    error=error,
                    tree=child,
                    config=config,
                    depth=depth + 1,
                )
    else:
        if depth > 0:
            rich.print(
                f"{' ' * (depth - 1) * len(TREE_DEFAULT_INDENT)}"
                f"[bold white]{TREE_DEFAULT_INDENT}[/]",
                end="",
            )
        rich.print(
            f"[bold {config.accent_color}]{tree.node_meta.name} ({tree.node_meta.node_type})",
        )
        rich.print(
            f"[bold {config.main_color}] | [/]"
            f"{' ' * depth * len(TREE_DEFAULT_INDENT)}"
            f"[bold {config.accent_color}]"
            f"{'^' * len(tree.node_meta.name)} "
            f"{error.error.codename}[/]",
        )


def print_scene_error(
    error: SceneError,
    config: Config | None = None,
) -> None:
    """"""
    config = config or Config()
    rich.print(
        f"[bold white]{error.path}[/]"
        f"[{config.main_color}]: [/]"
        f"[bold {config.accent_color}]"
        f"{error.error.codename}[/] "
        f"[white]{error.error.message}[/] ",
    )
    if not isinstance(error.scene_tree, SceneTree):
        return
    if not isinstance(error.error_tree, SceneTree):
        return
    path = get_subtree_path(error.scene_tree, error.error_tree)
    if path is not None:
        _print_error_tree(error, path, config=config)
    if error.error.help_message is not None:
        rich.print(
            f"[bold {config.main_color}] = help: {error.error.help_message}[/]",
        )


def print_errors(
    script_errors: list[ScriptError],
    scene_errors: list[SceneError],
    config: Config | None = None,
) -> None:
    """Print formatted script errors.

    :param errors: Script errors to print.
    :param config: Linter configuration.
    """
    config = config or Config()

    total = len(script_errors) + len(scene_errors)

    for error in script_errors:
        print_script_error(error, config=config)
    for error in scene_errors:
        print_scene_error(error, config=config)

    if total > 0:
        rich.print(f"[bold white]Found {total} errors.[/]")
    else:
        rich.print("[bold white]No errors found![/]")

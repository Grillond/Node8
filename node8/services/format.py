"""Provide error formatting and printing functions."""

from typing import Final

import rich

from node8.core.config import Config
from node8.models.errors import ScriptError

MIN_LINE: Final[int] = 1
LINE_NUMBER_OFFSET: Final[int] = 1


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
        f"[bold white]{error.path}[/]" # noqa: WPS237
        f"[{config.main_color}]:[/]"
        f"[bold white]{error.line}[/]"
        f"[{config.main_color}]:[/]"
        f"[bold white]{error.column}[/]"
        f"[{config.main_color}]:[/] "
        f"[bold {config.accent_color}]" # noqa: WPS226
        f"{error.error.codename}[/] "
        f"[white]{error.error.message}[/] ",
    )


def _print_script_error_body( # noqa: WPS210
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
        f"[bold {config.main_color}]{' ' * (spaces)} |[/]", # noqa: WPS237, WPS226
    )

    for line in range(start_line, end_line + 1):
        rich.print(
            f"[bold {config.main_color}]{line: < {spaces}} | [/]" # noqa: WPS237
            f"[white]{script_lines[line - 1].rstrip()}[/]",
        )
        if line == error.line:
            rich.print(
                f"[bold {config.main_color}]" # noqa: WPS237
                f"{' ' * spaces} |[/]"
                f"{' ' * error.column}"
                f"[bold {config.accent_color}]"
                f"{'^' * (error.end_column - error.column)}"
                f" {error.error.codename}[/]",
            )

    rich.print(
        f"[bold {config.main_color}]{' ' * (spaces)} |[/]", # noqa: WPS237
    )
    if error.error.help_message is not None:
        rich.print(
            f"{' ' * spaces} [bold {config.main_color}]= help: " # noqa: WPS237
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




def print_script_errors(
        errors: list[ScriptError],
        config: Config | None = None,
) -> None:
    """Print formatted script errors.

    :param errors: Script errors to print.
    :param config: Linter configuration.
    """
    config = config or Config()

    if len(errors) > 0:
        for error in errors:
            print_script_error(error, config=config)
        rich.print(f"[bold white]Found {len(errors)} errors.[/]")
    else:
        rich.print("[bold white]No errors found![/]")

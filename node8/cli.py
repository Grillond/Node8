"""CLI entry point of Node8 linter."""

import argparse
from pathlib import Path

from node8.services import gdscript


def main(paths: list[str]) -> None:
    """Run linter for given paths.

    :param paths: Array of paths to check.
    """
    gdscript.check(paths)


def check() -> None:
    """CLI entry point.

    Accepts paths and runs main function.
    """
    parser = _argparser_init()
    args = parser.parse_args()
    paths = args.paths
    if len(paths) <= 0:
        paths.append(str(Path.cwd()))
    main(paths)


def _argparser_init() -> argparse.ArgumentParser:
    """Initialize and retrieve argparser.

    :returns: Initialized argparser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, default=[], nargs="*")
    return parser

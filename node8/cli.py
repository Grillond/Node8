"""CLI entry point of Node8 linter."""

import argparse
from pathlib import Path

from node8.core.config import Config
from node8.services import gdscript, scenes
from node8.services.format import print_errors


def check() -> None:
    """CLI entry point.

    Accepts paths and runs linter.
    """
    parser = _argparser_init()
    args = parser.parse_args()
    path = Path(args.path)
    config = Config.from_toml(path)

    script_errors = gdscript.check(path, config=config)
    script_errors.sort(key=lambda error: error.error.codename)

    scene_errors = scenes.check(path, config=config)
    scene_errors.sort(key=lambda error: error.error.codename)

    print_errors(
        script_errors=script_errors,
        scene_errors=scene_errors,
        config=config,
    )


def _argparser_init() -> argparse.ArgumentParser:
    """Initialize and retrieve argparser.

    :returns: Initialized argparser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        type=str,
        default=str(Path.cwd()),
        nargs="?",
    )
    return parser

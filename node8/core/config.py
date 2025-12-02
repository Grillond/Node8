"""Provide linter config model to set up linting parameters."""

import tomllib
from pathlib import Path
from typing import Final

from pydantic import BaseModel, Field, field_validator
from rich.color import Color, ColorParseError

CONFIG_FILENAME: Final[str] = "gdproject.toml"
CONFIG_TOML_PATH: Final[str] = "node8"

MAX_LINE_LENGTH: Final[int] = 80
LINES_SHOW_BEFORE: Final[int] = 2
LINES_SHOW_AFTER: Final[int] = 2

MAX_SCENE_INDENT: Final[int] = 3

MAIN_COLOR: Final[str] = "blue"
ACCENT_COLOR: Final[str] = "red"


class Config(BaseModel):
    """Node8 configuration class to configure linting parameters."""

    line_length: int = MAX_LINE_LENGTH
    lines_show_before: int = LINES_SHOW_BEFORE
    lines_show_after: int = LINES_SHOW_AFTER

    max_scene_indent: int = MAX_SCENE_INDENT

    main_color: str = MAIN_COLOR
    accent_color: str = ACCENT_COLOR

    ignores: list[str] = Field(default_factory=list)

    @field_validator("main_color", "accent_color")
    @classmethod
    def ensure_is_color(cls, color: str) -> str:
        """Validate color fields using rich.

        :param value: Value to validate.
        :returns: Validated value.
        :raises ConfigValidationError: If value is not a color.
        """
        try:
            Color.parse(color)
        except ColorParseError as error:
            msg: str = f"invalid color: {color}"
            raise ValueError(msg) from error
        return color

    @classmethod
    def from_toml(cls, path: Path) -> "Config":
        """Load the first found config in specified directory.

        Will output default config if no `gdproject.toml` was found.

        :param path: Path to load config from.
        :returns: Config instance.
        """
        for config_path in path.rglob(CONFIG_FILENAME):
            with config_path.open(mode="rb") as config_file:
                toml = tomllib.load(config_file)

            config_dict = toml.get(CONFIG_TOML_PATH, {})
            return cls(**config_dict)

        return cls()

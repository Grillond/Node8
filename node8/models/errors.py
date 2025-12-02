"""Linting error model classes to represent rule violations."""

from pathlib import Path
from typing import Any

from lark import Tree
from pydantic import BaseModel, ConfigDict


class Error(BaseModel):
    """Base lint error class."""

    codename: str
    message: str
    help_message: str | None = None


class ScriptError(BaseModel):
    """GDScript lint error class."""

    error: Error
    path: Path
    line: int
    column: int
    end_column: int


class SceneError(BaseModel):
    """Godot scene lint error class."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    error: Error
    path: Path
    error_tree: Tree[Any]
    scene_tree: Tree[Any]

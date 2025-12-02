"""Provide Godot scene linting functions to check for rule violations."""

from pathlib import Path

from node8.core.config import Config
from node8.models.errors import SceneError
from node8.services.rules.complexity import SceneTooNested
from node8.services.scene_tree import SceneTree


def _check_scene(
    path: Path,
    config: Config | None = None,
) -> list[SceneError]:
    """Check given scene and return errors.

    :param path: Path to scene.
    :param config: Linter configuration.
    :returns: Array of scene errors.
    """
    config = config or Config()

    errors: list[SceneError] = []

    tree: SceneTree | None = SceneTree.from_scene_path(path)
    if tree is None:
        return errors

    errors.extend(SceneTooNested.check(path, tree, config=config))

    return errors


def check(
    path: Path,
    config: Config | None = None,
) -> list[SceneError]:
    """Lint given paths and return errors.

    Will only check `.tscn` files.

    :param path: Directory to check.
    :param config: Linter configuration.
    :returns: Array of scene errors.
    """
    config = config or Config()

    errors: list[SceneError] = []
    for scene_path in path.rglob("*.tscn"):
        errors.extend(_check_scene(scene_path, config=config))

    return errors

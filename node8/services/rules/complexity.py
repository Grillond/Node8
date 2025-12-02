""""""
from typing import Final

from node8.models.errors import Error, SceneError
from node8.services.scene_tree import SceneTree
from node8.services.visitors import SceneVisitor

SCENE_TOO_NESTED_CODENAME: Final[str] = "SC001"
SCENE_TOO_NESTED_MESSAGE: Final[str] = "is too nested"
SCENE_TOO_NESTED_HELP: Final[str] = "Move nested nodes into a separate scene"



class SceneTooNested(SceneVisitor):
    """"""

    def scene_node(self, tree: SceneTree) -> None:
        """"""
        if tree.node_meta.depth > self.config.max_scene_indent:
            self.errors.append(SceneError(
                error=Error(
                    codename=SCENE_TOO_NESTED_CODENAME,
                    message=(
                        f"`{tree.node_meta.name}` {SCENE_TOO_NESTED_MESSAGE}"
                        f" ({tree.node_meta.depth} > {self.config.max_scene_indent})"
                    ),
                    help_message=SCENE_TOO_NESTED_HELP,
                ),
                path=self.path,
                error_tree=tree,
                scene_tree=self.scene_tree,
            ))

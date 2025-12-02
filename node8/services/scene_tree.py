from pathlib import Path
from typing import Any

import godot_parser
from lark import Tree
from pydantic import BaseModel


class SceneMeta(BaseModel):
    """"""

    name: str
    node_type: str
    depth: int


class SceneTree(Tree):
    """"""

    def __init__(
        self,
        data: str,
        children: list["SceneTree"],
        meta: SceneMeta,
    ) -> None:
        """"""
        super().__init__(data, children)
        self.node_meta = meta

    def __eq__(self, other: Any):
        """"""
        if isinstance(other, SceneTree):
            return all((
                self.data == other.data,
                self.node_meta == other.node_meta,
                self.children == other.children,
            ))
        return False

    @classmethod
    def from_godot_parser_node(
        cls,
        node: godot_parser.Node,
        depth: int = 0,
    ) -> "SceneTree":
        """"""
        children_trees: list[SceneTree] = []
        for child in node.get_children():
            children_trees.append(SceneTree.from_godot_parser_node(
                node=child,
                depth=depth + 1,
            ))

        meta = SceneMeta(
            name=node.name,
            node_type=node.type or "",
            depth=depth,
        )

        return SceneTree(
            data="scene_node",
            children=children_trees,
            meta=meta,
        )

    @classmethod
    def from_scene_path(
        cls,
        path: Path,
    ) -> "SceneTree | None":
        """"""
        scene = godot_parser.load(str(path))
        with scene.use_tree() as tree:
            if tree.root is None:
                return None
            return SceneTree.from_godot_parser_node(tree.root)


def get_subtree_path(
        tree: SceneTree,
        subtree: SceneTree,
) -> SceneTree | None:
    """"""
    if tree == subtree:
        return SceneTree(
            tree.data,
            [],
            tree.node_meta,
        )
    for child in tree.children:
        if not isinstance(child, SceneTree):
            continue
        child_path = get_subtree_path(child, subtree)
        if child_path is not None:
            return SceneTree(
                tree.data,
                [child_path],
                tree.node_meta,
            )
    return None

"""GDScript antipatters and bad practices.

Code that uses deprecated or outdated functions or keywords, bad
or controversial practices will be errored.
For example:
>>> func _process(_delta: float) -> void:
>>>     var node: Node2D = get_node("Node2D")

Will be an error since using `get_node` is a bad practice.
"""

from typing import Any, Final

from lark import Tree

from node8.models.errors import Error, ScriptError
from node8.services.visitors import Visitor

GET_NODE_FOUND_CODENAME: Final[str] = "N001"
GET_NODE_FOUND_MESSAGE: Final[str] = "`get_node` found"
GET_NODE_FOUND_HELP: Final[str] = (
    "Replace with `@export` or unique names: `%Node2D`"
)

class GetNodeFound(Visitor):
    """N001 rule tree visitor."""

    def standalone_call(self, tree: Tree[Any]) -> None:
        """Walk tree and detect `get_node` calls.

        :parma tree: Tree to walk.
        """
        if tree.children[0] != "get_node":
            return
        self.errors.append(ScriptError(
            error=Error(
                codename=GET_NODE_FOUND_CODENAME,
                message=GET_NODE_FOUND_MESSAGE,
                help_message=GET_NODE_FOUND_HELP,
            ),
            path=self.path,
            line=tree.meta.line,
            column=tree.meta.column,
            end_column=tree.meta.end_column,
        ))

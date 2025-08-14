"""Ignore model classes to represent rule ignores."""

from pydantic import BaseModel


class NoqaIgnore(BaseModel):
    """Noqa linter ignore model.

    Represents `# noqa` comments silencing rules.
    """

    line: int
    ignores: list[str] = []
    ignore_all: bool = False

"""GDScript annotation rules.

Code that lacks type hints and annotations will be errored.
For example:
>>> func foo(bar):
>>>     pass

Will be an error since it lacks type hints. Instead use this:
>>> func foo(bar: float) -> void:
>>>     pass
"""

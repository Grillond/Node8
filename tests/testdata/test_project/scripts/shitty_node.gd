extends CharacterBody2D


func _physics_process(delta: float) -> void:
    var sprite_2d: Sprite2D = get_node("Sprite2D")
    position.x += 3 * delta

func useless_but_very_long_function_that_does_absolutely_nothing_but_waste_space(arg1: float, arg2: float, arg3: float) -> void:
    # very useful
    pass

func foo(bar):
    # no type hints and output type
    # `pass` found
    pass

var aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab = 1

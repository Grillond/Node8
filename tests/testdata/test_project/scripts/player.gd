extends CharacterBody2D


## Player movement speed.
@export_range(0, 1000) var speed = 500
@export_enum("idle", "run", "attack") var anim: int
# or
enum NamedEnum {
    IDLE,
    RUN,
    ATTACK
}
@export var anim_enum: NamedEnum


func _process(_delta: float) -> void:
    var node: Node2D = get_node("Node2D")


func _physics_process(_delta: float) -> void:
    var direction = Input.get_vector(
        "ui_left",
        "ui_right",
        "ui_up",
        "ui_down",
    ).normalized()
    self.velocity = direction * speed
    move_and_slide()

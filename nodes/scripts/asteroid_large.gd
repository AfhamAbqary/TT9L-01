extends Node2D

@onready var cshape = $CollisionShape2D
@onready var sprite = $Sprite2D

var currentPos : Vector2
var endGoal: Vector2
var speed := 100
var currentScreenSize
var mouseEntered

signal asteroidDestroyed

# Called when the node enters the scene tree for the first time.
func _ready():
	currentScreenSize = get_viewport_rect().size
	if global_position.x >= currentScreenSize.x:
		endGoal = Vector2(-50, randf_range(0, currentScreenSize.y))
	elif global_position.x <= 0:
		endGoal = Vector2(randf_range(0, currentScreenSize.x), -50)
	if global_position.y >= currentScreenSize.y:
		endGoal = Vector2(randf_range(0, currentScreenSize.x+50), -50)
	elif global_position.y <= 0:
		endGoal = Vector2(-50, randf_range(0,currentScreenSize.y+50))

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	position = position.move_toward(endGoal, delta * speed)
	if position == endGoal:
		queue_free()
	if Input.is_action_pressed("MouseClicked") and mouseEntered and get_parent().chargeReady:
		queue_free()
		emit_signal("asteroidDestroyed")


func choose_randomly(list_of_entries):
	return list_of_entries[randi() % list_of_entries.size()]


func _on_area_2d_mouse_entered():
	mouseEntered = true

func _on_area_2d_mouse_exited():
	mouseEntered = false

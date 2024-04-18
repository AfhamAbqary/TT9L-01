extends Node2D

@export var charge = 1
@export var magnet = 1

var asteroid = preload("res://nodes/asteroid_large.tscn")
@onready var label = $"../UI/Label"
signal goldIncrease

var chargeReady = true

func choose_randomly(list_of_entries):
	return list_of_entries[randi() % list_of_entries.size()]

# Called when the node enters the scene tree for the first time.
func _ready():
	randomize()

func addGold():
	emit_signal("goldIncrease")

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	var currentScreenSize = get_viewport_rect().size
	var currentTime = get_node("Timer")
	
	if label.timer.is_stopped():
		chargeReady = true
	elif label.timer.time_left > 0:
		chargeReady = false
		
	# Called everytime timer reaches zero
	if currentTime.is_stopped():
		var possiblePositions = [Vector2(randf_range(0,currentScreenSize.x), choose_randomly([-50, currentScreenSize.y+50])), 
								Vector2(choose_randomly([-50, currentScreenSize.x+50]), randf_range(0,currentScreenSize.y))]
		
		var a = asteroid.instantiate()
		a.global_position = choose_randomly(possiblePositions)
		a.rotation = randi_range(0,360)
		var scale = randf_range(0.5,2)
		a.scale = Vector2(scale,scale)
		add_child(a)
		a.connect("asteroidDestroyed", addGold)
		currentTime.start()
	


func _on_charge_pressed():
	if label.gold >= 100:
		charge = charge * 0.95
		label.gold -= 100
		label.timer.wait_time *= 0.9


func _on_magnet_pressed():
	if label.gold >= 100:
		magnet = magnet / 2
		label.gold -= 100
		$Timer.wait_time *= 0.9
	print($Timer.wait_time)

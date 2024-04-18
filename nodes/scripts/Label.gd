extends Label

@export var gold = 10
@onready var progressBar = $"../ProgressBar"

signal chargeEnd

var multiplier = 1
var timer := Timer.new()
var charge

# Called when the node enters the scene tree for the first time.
func _ready():
	add_child(timer)
	timer.wait_time = 3.0
	charge = 1

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	text = str(gold, " Gold")
	progressBar.value = timer.wait_time-timer.time_left
	if timer.is_stopped():
		emit_signal("chargeEnd")
		progressBar.value = progressBar.max_value

func _on_spawner_gold_increase():
	gold += (10*multiplier)
	progressBar.max_value = (timer.wait_time*0.99)
	timer.one_shot = true
	timer.start()
	print(timer.wait_time)

func _on_multiplier_pressed():
	if gold >= 500:
		multiplier += 0.1
		gold -= 10

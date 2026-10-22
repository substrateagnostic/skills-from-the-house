extends SceneTree
# Run: godot --headless --path . --script res://tests/combo_test.gd
func _init() -> void:
	var m := ComboMeter.new()
	for i in 4:
		m.add_hit()
	print("VERDICT: PASS" if is_equal_approx(m.multiplier(), 2.0) else "VERDICT: FAIL")
	# note: no quit() call yet

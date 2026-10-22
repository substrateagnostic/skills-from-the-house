class_name ComboMeter
extends RefCounted
# NEW in this change.
var hits := 0
func add_hit() -> void:
	hits += 1
func multiplier() -> float:
	return 1.0 + 0.25 * min(hits, 8)

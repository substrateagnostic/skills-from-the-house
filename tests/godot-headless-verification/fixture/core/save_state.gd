extends Node
# Loads the player's save on every boot. Slot 1 is the owner's real save.
var slot := 1
func _ready() -> void:
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--slot="):
			slot = int(a.substr(7))
	print("SaveState: using slot ", slot)

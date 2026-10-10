extends SceneTree
## Windowed check: open the main scene, run 20 days, save a screenshot. godot --path . --script res://tests/screenshot.gd -- <out.png>
func _initialize() -> void:
	var out: String = OS.get_cmdline_user_args()[0] if OS.get_cmdline_user_args().size() else "user://main.png"
	var scene: Node = load("res://game/main.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	scene.pause_on_important = false
	for i in 20:
		scene._advance()
	for i in 10:
		await process_frame
	root.get_viewport().get_texture().get_image().save_png(out)
	print("saved ", out)
	quit()

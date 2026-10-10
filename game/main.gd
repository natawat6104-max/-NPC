extends Control
## First prototype screen (DECISIONS D10): NPC list, time controls, the omen power and the chronicle log.
## Only shows what the simulation says; all rules live in res://sim/.

## [label, multiplier]; multipliers come from balance.time
var speeds := [["หยุด", 0.0], ["ปกติ", 1.0], ["เร็ว", 4.0], ["เร็วมาก", 12.0]]

var data: GameData
var sim: Simulation
var speed := 0
var seconds_per_day := 12.0
var acc := 0.0
var pause_on_important := true

var day_label: Label
var influence_label: Label
var stock_label: Label
var omen_button: Button
var speed_buttons: Array[Button] = []
var npc_list: VBoxContainer
var why_label: RichTextLabel
var log_view: RichTextLabel
var seed_box: SpinBox
var death_box: OptionButton
var auto_omen_box: CheckBox
var pause_box: CheckBox


func _ready() -> void:
	data = GameData.load_default()
	var t: Dictionary = data.balance.time
	pause_on_important = t.pause_on_important_event
	speeds[2][1] = float(t.speed_fast_multiplier)
	speeds[3][1] = float(t.speed_very_fast_multiplier)
	seconds_per_day = float(t.speed_normal_seconds_per_period) * float(t.periods_per_day)
	_build_ui()
	_new_world()


func _process(delta: float) -> void:
	if speed == 0:
		return
	acc += delta * speeds[speed][1]
	while acc >= seconds_per_day:
		acc -= seconds_per_day
		_advance()
		if speed == 0:
			break


func _new_world() -> void:
	sim = Simulation.new(data, {"seed": int(seed_box.value), "death": "death" if death_box.selected == 1 else "warn", "omen": auto_omen_box.button_pressed})
	log_view.clear()
	if sim.error != "":
		log_view.append_text("[color=#e07070]%s[/color]\n" % sim.error)
		return
	log_view.append_text("[color=#9aa4b8]โลกใหม่ · seed %d · ยาในหมู่บ้าน %d/%d หน่วย[/color]\n" % [sim.opts.seed, sim.stock, sim.target])
	_set_speed(0)
	_refresh()


func _advance() -> void:
	if sim.error != "":
		return
	for line: Array in sim.step_day():
		log_view.append_text("[color=#d9b56b]วัน %d[/color]  %s\n" % [line[0], line[1]])
	if sim.important_today and pause_on_important:
		_set_speed(0)
		log_view.append_text("[color=#9aa4b8]⏸ หยุดเวลาเพราะมีเหตุการณ์สำคัญ[/color]\n")
	_refresh()


func _refresh() -> void:
	if sim.error != "":
		return
	day_label.text = "วันที่ %d" % sim.day
	influence_label.text = "อิทธิพล %d/%d" % [sim.influence, data.balance.influence.cap]
	stock_label.text = "ยา %d/%d (%s) · ราคา %.1f" % [sim.stock, sim.target, sim.level, sim.price]
	omen_button.text = "ส่งลาง (%d)%s" % [sim.omen_cost, " · รอส่ง" if sim.omen_requested else ""]
	omen_button.disabled = sim.omen_requested or sim.influence < sim.omen_cost
	for c in npc_list.get_children():
		c.queue_free()
	for n: Dictionary in data.world.npcs:
		var row := Label.new()
		row.text = "%s · %s — %s" % [n.name, n.role, sim.npc_status(n)]
		row.add_theme_color_override("font_color", Color(n.color).lightened(0.35))
		npc_list.add_child(row)
	var d := sim.leader_decision()
	if sim.quest != null and sim.quest.state == "open" and not d.is_empty():
		var lines := ["[b]%s[/b]" % d.reason]
		for o: Dictionary in d.options:
			lines.append("%s  %.1f" % [o.name, o.score])
		why_label.text = "\n".join(lines)
	elif sim.quest != null:
		why_label.text = "ปาร์ตี้ออกเดินทางแล้ว (%s)" % ", ".join(sim.quest.party.map(func(p): return p.name))
	else:
		why_label.text = "ยังไม่มีภารกิจเปิด"


func _set_speed(i: int) -> void:
	speed = i
	for j in speed_buttons.size():
		speed_buttons[j].button_pressed = j == i


func _on_omen() -> void:
	sim.omen_requested = true
	log_view.append_text("[color=#8fb3ff]✦ กลุ่มดาวเตรียมส่งลางให้ปาร์ตี้ถัดไป[/color]\n")
	_refresh()


func _build_ui() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	var bg := ColorRect.new()
	bg.color = Color("#141826")
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(bg)
	var root := VBoxContainer.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.offset_left = 16
	root.offset_top = 12
	root.offset_right = -16
	root.offset_bottom = -12
	root.add_theme_constant_override("separation", 10)
	add_child(root)

	var top := HBoxContainer.new()
	top.add_theme_constant_override("separation", 14)
	root.add_child(top)
	var title := Label.new()
	title.text = "พงศาวดารใต้ดวงดาว"
	title.add_theme_font_size_override("font_size", 22)
	title.add_theme_color_override("font_color", Color("#d9b56b"))
	top.add_child(title)
	day_label = _label(top)
	influence_label = _label(top)
	stock_label = _label(top)
	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	top.add_child(spacer)
	var group := ButtonGroup.new()
	for i in speeds.size():
		var b := Button.new()
		b.text = speeds[i][0]
		b.toggle_mode = true
		b.button_group = group
		b.pressed.connect(_set_speed.bind(i))
		top.add_child(b)
		speed_buttons.append(b)
	omen_button = Button.new()
	omen_button.pressed.connect(_on_omen)
	top.add_child(omen_button)

	var opts := HBoxContainer.new()
	opts.add_theme_constant_override("separation", 12)
	root.add_child(opts)
	_label(opts).text = "Seed"
	seed_box = SpinBox.new()
	seed_box.max_value = 999999
	seed_box.value = 1234
	opts.add_child(seed_box)
	death_box = OptionButton.new()
	death_box.add_item("บาดเจ็บวิกฤตแทนตาย")
	death_box.add_item("ตายได้ มีสัญญาณเตือน")
	opts.add_child(death_box)
	auto_omen_box = CheckBox.new()
	auto_omen_box.text = "ส่งลางอัตโนมัติ"
	opts.add_child(auto_omen_box)
	pause_box = CheckBox.new()
	pause_box.text = "หยุดเมื่อมีเหตุการณ์สำคัญ"
	pause_box.button_pressed = pause_on_important
	pause_box.toggled.connect(func(on): pause_on_important = on)
	opts.add_child(pause_box)
	var restart := Button.new()
	restart.text = "เริ่มโลกใหม่"
	restart.pressed.connect(_new_world)
	opts.add_child(restart)

	var body := HSplitContainer.new()
	body.size_flags_vertical = Control.SIZE_EXPAND_FILL
	body.split_offset = 380
	root.add_child(body)
	var left := VBoxContainer.new()
	left.custom_minimum_size.x = 340
	left.add_theme_constant_override("separation", 8)
	body.add_child(left)
	_heading(left, "NPC")
	npc_list = VBoxContainer.new()
	left.add_child(npc_list)
	_heading(left, "ผู้นำปาร์ตี้คิดอย่างไร")
	why_label = RichTextLabel.new()
	why_label.bbcode_enabled = true
	why_label.fit_content = true
	why_label.size_flags_vertical = Control.SIZE_EXPAND_FILL
	left.add_child(why_label)
	var right := VBoxContainer.new()
	body.add_child(right)
	_heading(right, "พงศาวดาร")
	log_view = RichTextLabel.new()
	log_view.bbcode_enabled = true
	log_view.scroll_following = true
	log_view.size_flags_vertical = Control.SIZE_EXPAND_FILL
	log_view.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	right.add_child(log_view)


func _label(parent: Node) -> Label:
	var l := Label.new()
	parent.add_child(l)
	return l


func _heading(parent: Node, text: String) -> void:
	var l := Label.new()
	l.text = text
	l.add_theme_color_override("font_color", Color("#d9b56b"))
	parent.add_child(l)

class_name GameData
extends RefCounted
## Loads the world content (data/world.json, exported from Star Studio) and the balance numbers
## (data/balance.json — the only source of numbers; each entry keeps its number under "value").

const WORLD_PATH := "res://data/world.json"
const BALANCE_PATH := "res://data/balance.json"

var world: Dictionary
## Section -> key -> value, e.g. balance.influence.cap
var balance: Dictionary


static func load_default() -> GameData:
	var d := GameData.new()
	d.world = read_json(WORLD_PATH)
	d.balance = flatten_balance(read_json(BALANCE_PATH))
	return d


static func read_json(path: String) -> Dictionary:
	var text := FileAccess.get_file_as_string(path)
	var parsed: Variant = JSON.parse_string(text)
	assert(parsed is Dictionary, "อ่าน %s ไม่ได้" % path)
	return parsed


static func flatten_balance(raw: Dictionary) -> Dictionary:
	var out := {}
	for section: String in raw:
		if section.begins_with("_") or not raw[section] is Dictionary:
			continue
		var sec := {}
		for key: String in raw[section]:
			var entry: Variant = raw[section][key]
			if entry is Dictionary and entry.has("value"):
				sec[key] = entry["value"]
		out[section] = sec
	return out


func node(id: String) -> Dictionary:
	return _by_id(world.nodes, id)


func good(id: String) -> Dictionary:
	return _by_id(world.goods, id)


func npc(id: String) -> Dictionary:
	return _by_id(world.npcs, id)


func template_text(event: String) -> String:
	for t: Dictionary in world.templates:
		if t.event == event:
			return t.text
	return ""


static func _by_id(arr: Array, id: String) -> Dictionary:
	for x: Dictionary in arr:
		if x.id == id:
			return x
	return {}

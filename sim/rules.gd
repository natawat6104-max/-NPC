class_name Rules
extends RefCounted
## Game rules shared by the simulation and its previews — a line-by-line port of Star Studio
## (partyPower, monsterPower, decide, priceIndex, fillTemplate) so both give the same numbers.

const RISK_BONUS := {"low": 0.0, "mid": 10.0, "midhigh": 20.0, "high": 35.0}
const ACCEPT := "รับภารกิจทันที"
const PREPARE := "เตรียมของก่อน"
const REST := "พักหนึ่งช่วง"
const REFUSE := "ปฏิเสธภารกิจ"


## party_power = Σ(combat×w + equipment(40)×w + health_ratio×w + synergy×w)  (GDD เจาะลึก 8.3)
static func party_power(members: Array, injured: Dictionary, bal: Dictionary) -> float:
	var b: Dictionary = bal.party_combat
	var roles := {}
	for m: Dictionary in members:
		roles[m.role] = true
	var syn := 40.0 if roles.size() > 1 else 10.0
	var s := 0.0
	for m: Dictionary in members:
		s = s + float(m.skills.combat) * b.power_weight_combat_skill + 40.0 * b.power_weight_equipment + (0.5 if injured.has(m.id) else 1.0) * b.power_weight_health_ratio + syn * b.power_weight_role_synergy
	return s


static func monster_power(mon: Dictionary, data: GameData) -> float:
	var n := data.node(mon.habitat)
	return float(mon.threat) * ((float(mon.gmin) + float(mon.gmax)) / 2.0) + (RISK_BONUS[n.risk] if not n.is_empty() else 0.0)


## Utility AI for "a quest is open": scores four options from traits, skills and the situation,
## and explains the choice from the real score parts (ภาคผนวก AI).
## sc: {food (days of supplies), info (0-100), fatigue (0-100), threat (0-100)}
static func decide(n: Dictionary, sc: Dictionary) -> Dictionary:
	var t: Dictionary = n.traits
	var k: Dictionary = n.skills
	var bravery := float(t.bravery)
	var caution := float(t.caution)
	var generosity := float(t.generosity)
	var ambition := float(t.ambition)
	var food := float(sc.food)
	var fatigue := float(sc.fatigue)
	var risk := float(sc.threat) * (1.0 - bravery / 200.0) * (1.0 - float(sc.info) / 250.0)
	var unprep := (2.0 - food) * 15.0 if food < 2.0 else 0.0
	var options: Array = [
		{"name": ACCEPT, "parts": [["ตรงเป้าหมายช่วยหมู่บ้าน", 35.0 + ambition * 0.15 + generosity * 0.1], ["ทักษะเก็บของเหมาะ", float(k.gathering) * 0.15], ["ความเสี่ยงของเส้นทาง", -risk * 0.6], ["เสบียงยังไม่พร้อม", -unprep * 1.2], ["ความเหนื่อย", -fatigue * 0.25]]},
		{"name": PREPARE, "parts": [["ตรงเป้าหมายช่วยหมู่บ้าน", 28.0 + generosity * 0.08], ["ต้องเตรียมเสบียง", unprep * 1.4 + 8.0], ["นิสัยระมัดระวัง", caution * 0.18], ["ความเสี่ยงของเส้นทาง", -risk * 0.45], ["เสียเวลา", -10.0]]},
		{"name": REST, "parts": [["ได้พักฟื้น", fatigue * 0.55], ["นิสัยระมัดระวัง", caution * 0.08], ["เสียเวลา", -18.0], ["ยังคืบหน้าเป้าหมาย", 5.0]]},
		{"name": REFUSE, "parts": [["เลี่ยงภัย", risk * 0.5 * (caution / 100.0)], ["ขัดเป้าหมายช่วยหมู่บ้าน", -(25.0 + generosity * 0.15)]]},
	]
	for o: Dictionary in options:
		var s := 0.0
		for p: Array in o.parts:
			s = s + p[1]
		o["score"] = s
	var accept: Dictionary = options[0]
	options = stable_sorted(options, func(a, b): return b.score - a.score)
	var best: Dictionary = options[0]
	var pos := []
	for p: Array in stable_sorted(best.parts.filter(func(p): return p[1] > 0), func(a, b): return b[1] - a[1]).slice(0, 2):
		pos.append(p[0])
	var neg := []
	for p: Array in stable_sorted(accept.parts.filter(func(p): return p[1] < -5), func(a, b): return a[1] - b[1]).slice(0, 1):
		neg.append(p[0])
	var reason := "%sเลือก \"%s\" เพราะ%s" % [n.name, best.name, " และ".join(pos)]
	if neg.size() and best.name != ACCEPT:
		reason += " (ถ้าออกทันที ติดที่%s)" % neg[0]
	return {"options": options, "best": best, "reason": reason}


static func price_index(stock: float, target: float, bal: Dictionary) -> float:
	var e: Dictionary = bal.economy
	return clampf(pow(target / maxf(stock, 1.0), e.price_exponent), e.price_index_min, e.price_index_max)


## Replaces {key} with facts[key]; unknown keys stay as they are.
static func fill_template(text: String, facts: Dictionary) -> String:
	var re := RegEx.create_from_string("\\{(\\w+)\\}")
	var out := ""
	var last := 0
	for m: RegExMatch in re.search_all(text):
		out += text.substr(last, m.get_start() - last)
		var key := m.get_string(1)
		out += as_text(facts[key]) if facts.has(key) else m.get_string()
		last = m.get_end()
	return out + text.substr(last)


## Numbers print like JavaScript: 14.0 -> "14".
static func as_text(v: Variant) -> String:
	if v is float and v == floor(v) and absf(v) < 1e15:
		return str(int(v))
	return str(v)


## Array.sort in JavaScript is stable; Godot's sort_custom is not, so ties keep their order here.
## cmp(a, b) < 0 puts a first, like a JavaScript comparator.
static func stable_sorted(arr: Array, cmp: Callable) -> Array:
	var idx := range(arr.size())
	idx.sort_custom(func(i, j):
		var c: float = cmp.call(arr[i], arr[j])
		return c < 0 or (c == 0 and i < j))
	return idx.map(func(i): return arr[i])

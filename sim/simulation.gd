class_name Simulation
extends RefCounted
## The first playable loop (DECISIONS D6/D8/D10): the village medicine stock drains, the healer posts a
## herb quest, adventurers decide with Utility AI, travel to the forest, may meet monsters, and come back.
## The constellation can send an omen. Everything is a pure function of (world, balance, seed, options):
## no nodes or scenes, so it runs headless and in tests. One step = one game day.
##
## A line-by-line port of Star Studio's simulate(); tests/run_tests.gd checks both give the same chronicle.

const ADVENTURER_ROLES := ["นักผจญภัย", "นักธนู"]
const HEALER_ROLE := "ผู้รักษา"
const HERB := "ใบจันทร์ขาว"

## {seed: int, death: "warn" | "death" (D5), omen: bool — send an omen automatically when affordable}
var opts: Dictionary
var data: GameData
var bal: Dictionary
var rng: SimRng
var error := ""

var day := 0
## [[day, text], ...]
var chronicle: Array = []
var series := {"stock": [], "price": [], "inf": []}
var stats := {"quests": 0, "success": 0, "retreat": 0, "fail": 0, "injuries": 0, "deaths": 0, "shortageDays": 0, "omens": 0}

var village: Dictionary
var forest: Dictionary
var healer: Dictionary
var adventurers: Array = []
var monsters: Array = []
var medicine: Dictionary
var travel_days := 1
var target := 0.0
var stock := 0.0
var price := 0.0
var influence := 0.0
var omen_cost := 12.0
## npc id -> days left to heal
var injured := {}
var dead := {}
var quest: Variant = null
var level := ""
var refused_logged := false
## The player asked for an omen; spent when the next party leaves.
var omen_requested := false
## Something happened today that should pause the game (injury, death) — balance time.pause_on_important_event.
var important_today := false


func _init(game_data: GameData, options: Dictionary) -> void:
	data = game_data
	bal = data.balance
	opts = {"seed": 1234, "death": "warn", "omen": true}
	opts.merge(options, true)
	rng = SimRng.new(int(opts.seed))
	var w := data.world
	medicine = data.good("medicine")
	if medicine.is_empty():
		error = "ต้องมีสินค้า id 'medicine' ก่อนรันการจำลอง"
		return
	village = data.node(w.crisis.region)
	if village.is_empty():
		village = w.nodes[0]
	forest = data.node("forest")
	if forest.is_empty():
		for n: Dictionary in w.nodes:
			if n.type == "wild":
				forest = n
				break
	if village.is_empty() or forest.is_empty():
		error = "ต้องมีหมู่บ้านและพื้นที่ป่าในแผนที่"
		return
	var best_route: Variant = null
	for r: Dictionary in w.routes:
		if village.id in [r.a, r.b] and forest.id in [r.a, r.b] and (best_route == null or r.days < best_route.days):
			best_route = r
	travel_days = maxi(1, ceili(best_route.days if best_route != null else 2.0))
	for n: Dictionary in w.npcs:
		if n.role == HEALER_ROLE and healer.is_empty():
			healer = n
		if n.role in ADVENTURER_ROLES:
			adventurers.append(n)
	for m: Dictionary in w.monsters:
		if m.habitat == forest.id:
			monsters.append(m)
	target = float(medicine.daily) * bal.economy.target_stock_days
	omen_cost = float(bal.powers.omen.cost) if bal.powers.has("omen") else 12.0
	stock = roundf(target * 0.45)
	price = float(medicine.base) * Rules.price_index(stock, target, bal)
	influence = minf(bal.influence.cap, bal.influence.start)
	level = _level(stock)


func run(days: int) -> Dictionary:
	for i in days:
		step_day()
	return result()


func result() -> Dictionary:
	return {"log": chronicle, "series": series, "stats": stats, "target": target}


## Advances one game day; returns the chronicle lines written today.
func step_day() -> Array:
	var start := chronicle.size()
	day += 1
	important_today = false
	influence = minf(bal.influence.cap, influence + bal.influence.regen_per_day)
	for k: String in injured.keys():
		injured[k] -= 1
		if injured[k] <= 0:
			injured.erase(k)
	stock = maxf(0.0, stock - (float(medicine.daily) + injured.size()))
	var e: Dictionary = bal.economy
	var raw := float(medicine.base) * Rules.price_index(stock, target, bal)
	price = clampf(raw, price * (1.0 - e.price_daily_change_max), price * (1.0 + e.price_daily_change_max))
	var nl := _level(stock)
	if nl != level:
		_write("shortage_changed", {"good": "ยา", "place": village.name, "from": level, "to": nl})
		level = nl
	if stock / target < 0.3:
		stats.shortageDays += 1
	if quest == null and stock / target < 0.5 and not healer.is_empty() and not dead.has(healer.id):
		quest = {"state": "open", "amount": 10}
		stats.quests += 1
		refused_logged = false
		_write("quest_posted", {"issuer": healer.name, "item": HERB, "amount": 10, "place": forest.name})
	if quest != null and quest.state == "open":
		_try_depart()
	if quest != null and quest.state == "travel" and day >= quest.arrive:
		_resolve_trip()
	if quest != null and quest.state == "return" and day >= quest.back:
		stock += quest.herbs
		stats[quest.outcome] += 1
		var hurt_note := " แม้%sบาดเจ็บ%s" % [quest.hurt.name, quest.sev] if quest.hurt != null else ""
		var line := _text("party_returned", {"party_leader": quest.names[0], "place": forest.name, "item": HERB, "amount": quest.herbs, "injured_note": hurt_note})
		if quest.outcome == "retreat":
			line += " (ถอยกลับเพราะเจอ%s)" % quest.met
		chronicle.append([day, line])
		quest = null
	series.stock.append(stock)
	series.price.append(price)
	series.inf.append(influence)
	return chronicle.slice(start)


## What the quest leader thinks right now (for the "why" panel).
func leader_decision() -> Dictionary:
	var free := _free_adventurers()
	if free.is_empty():
		return {}
	return Rules.decide(free[0], _scene())


func npc_status(n: Dictionary) -> String:
	if dead.has(n.id):
		return "เสียชีวิต"
	if quest != null and quest.has("party") and quest.party.has(n) and quest.state != "open":
		return "เดินทางไป%s" % forest.name if quest.state == "travel" else "กำลังเดินทางกลับ"
	if injured.has(n.id):
		return "บาดเจ็บ (อีก %d วัน)" % injured[n.id]
	return "อยู่ที่%s" % village.name


func stock_level_text() -> String:
	return level


func _try_depart() -> void:
	var free := _free_adventurers()
	if free.is_empty():
		return
	var leader: Dictionary = free[0]
	var d := Rules.decide(leader, _scene())
	var choice: String = d.best.name
	if choice == Rules.REFUSE:
		if not refused_logged:
			chronicle.append([day, "%sปฏิเสธภารกิจ: %s" % [leader.name, d.reason.replace(leader.name + "เลือก ", "")]])
			refused_logged = true
	elif choice != Rules.REST:
		quest.party = free.slice(0, 2)
		quest.state = "travel"
		quest.prep = 1 if choice == Rules.PREPARE else 0
		quest.omen = false
		if (opts.omen or omen_requested) and influence >= omen_cost:
			influence -= omen_cost
			quest.omen = true
			omen_requested = false
			stats.omens += 1
			_write("omen_sent", {"party_leader": leader.name, "clue": "มีรอยฝูงมอนสเตอร์บนเส้นทางตรง"})
		quest.arrive = day + quest.prep + travel_days + (1 if quest.omen else 0)


func _resolve_trip() -> void:
	var party: Array = quest.party
	var names := party.map(func(p): return p.name)
	var herbs := 0
	var outcome := "success"
	var hurt: Variant = null
	var sev := "เล็กน้อย"
	var meet: bool = monsters.size() > 0 and rng.next_float() < (0.3 if quest.omen else 0.6)
	if meet:
		var mon: Dictionary = monsters[rng.range_int(0, monsters.size() - 1)]
		var r := Rules.monster_power(mon, data) / maxf(Rules.party_power(party, injured, bal), 1.0)
		var brave := 0.0
		for p: Dictionary in party:
			brave = brave + float(p.traits.bravery) - float(p.traits.caution)
		brave = brave / party.size()
		var retreat_at := 1.0 + brave / 200.0
		if r > retreat_at:
			outcome = "retreat"
			herbs = rng.range_int(0, 4)
			if rng.next_float() < 0.3:
				hurt = party[rng.range_int(0, party.size() - 1)]
		elif rng.next_float() < clampf(0.9 - (r - 0.5) * 0.45, 0.15, 0.95):
			herbs = rng.range_int(9, 14)
			if rng.next_float() < 0.25:
				hurt = party[rng.range_int(0, party.size() - 1)]
		else:
			outcome = "fail"
			herbs = rng.range_int(0, 3)
			hurt = party[rng.range_int(0, party.size() - 1)]
			sev = "หนัก"
		quest.met = mon.name
	else:
		herbs = rng.range_int(10, 14)
	quest.state = "return"
	quest.back = day + travel_days
	quest.herbs = herbs
	quest.outcome = outcome
	quest.hurt = hurt
	quest.sev = sev
	quest.names = names
	if hurt != null:
		important_today = true
		stats.injuries += 1
		injured[hurt.id] = 6 if sev == "หนัก" else 3
		var activity := "ปะทะ%sที่%s" % [quest.met, forest.name] if meet else "เก็บสมุนไพรที่%s" % forest.name
		_write("npc_injured", {"npc": hurt.name, "severity": sev, "activity": activity})
		if sev == "หนัก" and opts.death == "death" and rng.next_float() < 0.25:
			dead[hurt.id] = true
			stats.deaths += 1
			chronicle.append([day, "%sเสียชีวิตจากบาดแผล พงศาวดารบันทึกการจากไปและเพื่อนร่วมทางจดจำเหตุการณ์นี้" % hurt.name])


func _free_adventurers() -> Array:
	return adventurers.filter(func(n): return not injured.has(n.id) and not dead.has(n.id))


func _scene() -> Dictionary:
	var threat := 25.0 if forest.risk == "low" else (55.0 if forest.risk == "mid" else 75.0)
	return {"food": 1.5, "info": 40.0, "fatigue": 25.0, "threat": threat}


func _level(m: float) -> String:
	return "ปกติ" if m / target >= 0.6 else ("ตึงตัว" if m / target >= 0.3 else "วิกฤต")


func _text(event: String, facts: Dictionary) -> String:
	var t := data.template_text(event)
	return Rules.fill_template(t, facts) if t != "" else ""


func _write(event: String, facts: Dictionary) -> void:
	chronicle.append([day, _text(event, facts)])

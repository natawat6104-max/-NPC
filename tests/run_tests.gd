extends SceneTree
## Headless tests: godot --headless --path . --script res://tests/run_tests.gd
## Exit code 0 = all passed.

var failures := 0
var checks := 0


func _initialize() -> void:
	test_rng_matches_javascript()
	test_balance_matches_golden()
	test_matches_studio_simulation()
	test_deterministic()
	test_player_omen()
	print("\n%d checks, %d failed" % [checks, failures])
	quit(1 if failures else 0)


func check(ok: bool, what: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		print("FAIL ", what)


func golden() -> Dictionary:
	return GameData.read_json("res://tests/golden/studio_sim.json")


func test_rng_matches_javascript() -> void:
	# First values of mulberry32(1234) in JavaScript.
	var r := SimRng.new(1234)
	var got := []
	for i in 3:
		got.append(r.next_float())
	var want := [0.0732949781, 0.7034119898, 0.9028560191]
	for i in 3:
		check(absf(got[i] - want[i]) < 1e-9, "rng value %d: %s vs %s" % [i, got[i], want[i]])


func test_balance_matches_golden() -> void:
	# The golden logs were made with Studio's built-in numbers; data/balance.json must hold the same ones.
	var b := GameData.load_default().balance
	var s: Dictionary = golden().studio_balance
	for key in ["cap", "start", "regen_per_day"]:
		check(float(b.influence[key]) == float(s.influence[key]), "influence.%s" % key)
	check(float(b.powers.omen.cost) == float(s.powers.omen.cost), "powers.omen.cost")
	for key in ["target_stock_days", "price_exponent", "price_index_min", "price_index_max", "price_daily_change_max"]:
		check(float(b.economy[key]) == float(s.economy[key]), "economy.%s" % key)
	for key in ["power_weight_combat_skill", "power_weight_equipment", "power_weight_health_ratio", "power_weight_role_synergy"]:
		check(float(b.party_combat[key]) == float(s.party_combat[key]), "party_combat.%s" % key)


func test_matches_studio_simulation() -> void:
	for run: Dictionary in golden().runs:
		var sim := Simulation.new(GameData.load_default(), {"seed": int(run.seed), "death": run.death, "omen": run.omen})
		var res := sim.run(int(run.days))
		var want: Array = run.result.log
		var name := "seed %d, %d days, %s, omen %s" % [run.seed, run.days, run.death, run.omen]
		check(res.log.size() == want.size(), "%s: %d lines vs %d" % [name, res.log.size(), want.size()])
		for i in mini(res.log.size(), want.size()):
			var ok: bool = int(res.log[i][0]) == int(want[i][0]) and res.log[i][1] == want[i][1]
			check(ok, "%s line %d:\n  got  %s\n  want %s" % [name, i, res.log[i], want[i]])
			if not ok:
				break
		for k: String in run.result.stats:
			check(int(res.stats[k]) == int(run.result.stats[k]), "%s stats.%s: %s vs %s" % [name, k, res.stats[k], run.result.stats[k]])


func test_deterministic() -> void:
	var a := Simulation.new(GameData.load_default(), {"seed": 555, "death": "death"}).run(90)
	var b := Simulation.new(GameData.load_default(), {"seed": 555, "death": "death"}).run(90)
	check(JSON.stringify(a) == JSON.stringify(b), "same seed gives the same 90 days")
	var c := Simulation.new(GameData.load_default(), {"seed": 556, "death": "death"}).run(90)
	check(JSON.stringify(a.log) != JSON.stringify(c.log), "another seed gives another story")


func test_player_omen() -> void:
	# With automatic omens off, the player's request is spent on the next departure.
	var sim := Simulation.new(GameData.load_default(), {"seed": 1234, "omen": false})
	sim.omen_requested = true
	var before := sim.influence
	var sent := false
	for i in 10:
		for line: Array in sim.step_day():
			if "ส่งลาง" in line[1]:
				sent = true
		if sent:
			break
	check(sent, "player omen is written to the chronicle")
	check(not sim.omen_requested, "player omen request is used up")
	check(sim.stats.omens == 1, "one omen counted")
	check(sim.influence <= minf(100.0, before + 10.0 * sim.day) - 12.0 + 0.001, "omen costs influence")

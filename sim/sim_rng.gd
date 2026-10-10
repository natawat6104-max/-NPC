class_name SimRng
extends RefCounted
## Deterministic random numbers (mulberry32), bit-for-bit the same as Star Studio's simulate(),
## so a seed gives the same world in the studio, in tests and in the game (DECISIONS D1).

const MASK := 0xFFFFFFFF

var state: int


func _init(seed_value: int) -> void:
	state = seed_value & MASK


## Float in [0, 1).
func next_float() -> float:
	state = (state + 0x6D2B79F5) & MASK
	var t := _imul(state ^ (state >> 15), 1 | state)
	t = ((t + _imul(t ^ (t >> 7), 61 | t)) & MASK) ^ t
	return float((t ^ (t >> 14)) & MASK) / 4294967296.0


## Integer in [a, b].
func range_int(a: int, b: int) -> int:
	return a + int(floor(next_float() * (b - a + 1)))


## 32-bit multiply (Math.imul) without overflowing the 64-bit int.
static func _imul(a: int, b: int) -> int:
	return ((a & 0xFFFF) * b + ((((a >> 16) * b) & 0xFFFF) << 16)) & MASK

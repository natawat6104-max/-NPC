# พงศาวดารใต้ดวงดาว (Chronicles Beneath the Stars)

เกมจำลองโลกแฟนตาซีที่ NPC ใช้ชีวิตและผจญภัยเอง ผู้เล่นเป็น "กลุ่มดาว" ที่ชี้นำได้อย่างจำกัด

- เอกสารออกแบบ: [`docs/`](docs/README.md) — เริ่มที่ [`docs/DECISIONS.md`](docs/DECISIONS.md)
- ตัวเลขเกม (แหล่งเดียว): [`data/balance.json`](data/balance.json) → สรุปที่ [`docs/BALANCE.md`](docs/BALANCE.md)
  - หลังแก้ JSON ให้รัน `python3 tools/gen_balance_doc.py`

## โปรเจกต์ Godot (D17)
Godot 4.7 + GDScript — `project.godot` อยู่ที่โฟลเดอร์นี้

| โฟลเดอร์ | คืออะไร |
|---|---|
| `sim/` | แกนจำลอง (ไม่พึ่ง scene/node): `Simulation` `Rules` `SimRng` `GameData` |
| `game/` | หน้าจอต้นแบบ (D10): NPC · ปุ่มเวลา · ส่งลาง · พงศาวดาร |
| `tests/` | ทดสอบอัตโนมัติ — เทียบผลกับ Star Studio ทุกบรรทัด (`tests/golden/studio_sim.json`) |
| `data/` | `world.json` เนื้อหาโลก (จาก Star Studio) · `balance.json` ตัวเลข |
| `assets/` | ร่าง NPC (`models/char10-npc.glb`) และท่าทาง 425 ท่า (`animations/`) |

- เปิด: Godot 4.7 → Import → เลือก `project.godot` → กด ▶ (F5)
- ทดสอบ: `godot --headless --path . --script res://tests/run_tests.gd`
- สร้างผลเทียบใหม่หลังแก้ simulate() ใน Studio: `node tools/sim/studio_golden.js docs/mockups/star-studio.html <โฟลเดอร์ชั่วคราว> tests/golden/studio_sim.json`

สถานะ: ต้นแบบแรก — ระบบจำลอง + บันทึกข้อความ (D10)

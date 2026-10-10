# เอกสารออกแบบ — พงศาวดารใต้ดวงดาว

- [`DECISIONS.md`](DECISIONS.md) — การตัดสินใจที่ใช้ตัดสินเมื่อเอกสารขัดกัน **อ่านก่อน**
- [`GODOT-IMPORT.md`](GODOT-IMPORT.md) — นำร่างตัวละครเข้า Godot (ขนาด texture, จับคู่กระดูก)
- [`BALANCE.md`](BALANCE.md) — ตารางตัวเลขกลาง (สร้างจาก `data/balance.json`)
- `mockups/` — ต้นแบบหน้าจอ (เปิดในเบราว์เซอร์); `mockups/models/char10-base.glb` คือร่างพื้นฐานที่ Studio โหลดเอง; `mockups/samples/test-rig-mixamo.glb` คือโมเดลทดสอบ
- `gdd/` — GDD 15 ไฟล์ (แปลงจาก .docx; ต้นฉบับอยู่ใน `gdd/original/`)

## สถานะของแต่ละไฟล์

| ไฟล์ | เรื่อง | ใช้ใน MVP (เล่นคนเดียว) |
|---|---|---|
| [00](gdd/00-gdd-initial.md) | GDD ฉบับเริ่มต้น v0.1 | ✅ แนวคิดหลัก |
| [01](gdd/01-gdd-deep-dive.md) | GDD ฉบับเจาะลึก v0.2 | ✅ **เอกสารหลัก** (ตัวเลขพลังแทนด้วย D3) |
| [02](gdd/02-influence-cooldowns.md) | อิทธิพลและคูลดาวน์ | ⚠️ ใช้หลักการ/ต้นทุน; เวลาจริงและผู้เล่นหลายคน → ออนไลน์ |
| [03](gdd/03-npc-ai-behavior.md) | AI และพฤติกรรม NPC | ✅ ใช้ (ข้อ 16–17 เรื่องออนไลน์ → ภายหลัง) |
| [04](gdd/04-npc-economy.md) | เศรษฐกิจ NPC | ⚠️ ใช้แบบย่อตาม D6 |
| [05](gdd/05-social-factions.md) | เครือข่ายสังคมและฝ่ายอำนาจ | ⚠️ เฉพาะความสัมพันธ์หลายมิติ; กิลด์/Faction/รัฐ → ภายหลัง |
| [06](gdd/06-generation-legacy.md) | หลายรุ่นและมรดก | ⏸️ หลัง MVP (D7) |
| [07](gdd/07-ui-ux.md) | UI/UX | ✅ ใช้ ยกเว้นข้อ 1.1 (D2) มุมมองแผนที่ (D14: 3D มองเฉียงจากฟ้า) และร่างตัวละคร (D15) |
| [08](gdd/08-player-interaction.md) | ปฏิสัมพันธ์ระหว่างผู้เล่น | 🌐 ระยะออนไลน์ |
| [09](gdd/09-global-events.md) | เหตุการณ์ระดับโลก | ⏸️ หลัง MVP (MVP มีวิกฤตประจำบท 1 แบบ) |
| [10](gdd/10-raid-coop.md) | Constellation Raid | 🌐 ระยะออนไลน์ |
| [11](gdd/11-balance-anti-griefing.md) | Balance & Anti-Griefing | ⚠️ ใช้ safety floor/recovery; ส่วนผู้เล่นหลายคน → ออนไลน์ |
| [12](gdd/12-dynamic-chronicle.md) | Dynamic Chronicle | ✅ ใช้ (template อย่างเดียว) |
| [13](gdd/13-dynamic-audio.md) | Dynamic Audio | ⏸️ หลัง MVP (เสียงพื้นฐานตาม GDD เจาะลึก 13.2) |
| [14](gdd/14-playtest-roadmap.md) | Playtest Roadmap | ⚠️ ใช้ P0–P2 แบบเล่นคนเดียว |

✅ ใช้ · ⚠️ ใช้บางส่วน · ⏸️ เลื่อน · 🌐 เฉพาะออนไลน์

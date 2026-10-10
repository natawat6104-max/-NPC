# โมเดลตัวละคร

| ไฟล์ | คืออะไร |
|---|---|
| `char10-npc.glb` | **ร่าง NPC ที่ใช้ในเกม** (D16) — 12,000 สามเหลี่ยม, วัสดุ `Skin` `Shirt` `Pants` `Footwear`, texture ผิว 1024px, กระดูก 69 ชิ้น มีนิ้วครบ — สร้างจากต้นฉบับด้วย `tools/models/make_npc_body.py` |
| `Meshy_AI_Character_output_10.bonemap.json` / `.tres` | จับคู่กระดูกกับ `SkeletonProfileHumanoid` ของ Godot (`Hips` = `Bone_000`) — `.tres` โหลดใน Godot ได้ตรง ๆ |
| `source/Meshy_AI_Character_output_10.glb` | ต้นฉบับ (Meshy SmartRig) — 132,124 สามเหลี่ยม, texture 4096/4096/2048px |
| `source/Meshy_AI_fantasy_teen_bald_tpo_1010110431_image-to-3d-texture_obj.fbx` | ร่างตัวแรก (เลิกใช้แล้ว เก็บไว้อ้างอิง) — Mixamo, นิ้วแบบถุงมือ |
| [`../../docs/mockups/models/char10-base.glb`](../../docs/mockups/models/char10-base.glb) | ต้นฉบับย่อ texture 1024/1024/512px (ไม่ลดสามเหลี่ยม) |

โฟลเดอร์ `source/` มี `.gdignore` — Godot ไม่นำเข้าไฟล์ต้นฉบับ (ใหญ่และไม่ได้ใช้ในเกม)

วิธีนำเข้า Godot: [`docs/GODOT-IMPORT.md`](../../docs/GODOT-IMPORT.md)

# นำร่างพื้นฐานเข้า Godot 4

ร่างที่ใช้: [`assets/models/Meshy_AI_Character_output_10.glb`](../assets/models/Meshy_AI_Character_output_10.glb) (Meshy SmartRig, กระดูก 69 ชิ้น มีนิ้วครบ, สูง 1.7 เมตร, หันหน้า +Z) — ดู D15 ใน [`DECISIONS.md`](DECISIONS.md)

## 1. ขนาด texture (พื้นผิว)
ต้นฉบับมี texture 3 ภาพ: สีพื้น 4096px, normal 4096px, metallic/roughness 2048px (รวม ~12.9 MB) — มากเกินสำหรับ NPC ที่มองจากฟ้า

| ภาพ | ต้นฉบับ | ใช้ในเกม |
|---|---|---|
| สีพื้น (base color) | 4096 | **1024** |
| normal | 4096 | **1024** (หรือตัดทิ้งได้ เพราะมองจากไกล) |
| metallic/roughness | 2048 | **512** |

มี 2 ทาง:
- **ใช้ไฟล์ที่ย่อแล้ว** [`docs/mockups/models/char10-base.glb`](mockups/models/char10-base.glb) (5.6 MB, texture ตามตารางข้างบน, กระดูกและรูปทรงเหมือนต้นฉบับทุกอย่าง) — ง่ายที่สุด
- **ย่อใน Godot จากต้นฉบับ:** เลือกไฟล์ .glb ใน FileSystem → แท็บ Import → `GLTF > Embedded Image Handling` = `Extract Textures` → Reimport (ภาพจะแยกออกมาเป็นไฟล์ข้างโมเดล) → เลือกแต่ละภาพ → แท็บ Import → `Process > Size Limit` = 1024 (สีพื้นและ normal) หรือ 512 (metallic/roughness) → Reimport

## 2. จับคู่กระดูก (ให้ใช้ท่าทาง Humanoid ร่วมกันได้)
ชื่อกระดูกเป็น `Bone_000…` Godot เดาเองไม่ได้ ให้ใส่เอง:
1. ดับเบิลคลิกไฟล์ .glb → หน้าต่าง Advanced Import Settings → คลิก `Skeleton3D` ทางซ้าย
2. `Retarget > Bone Map` → New BoneMap → `Profile` = `SkeletonProfileHumanoid`
3. ใส่ตามตารางนี้ (ครบทุกตำแหน่งรวมนิ้วอยู่ใน [`assets/models/Meshy_AI_Character_output_10.bonemap.json`](../assets/models/Meshy_AI_Character_output_10.bonemap.json))

| Godot | กระดูกในไฟล์ |
|---|---|
| `Hips` | `Bone_001` |
| `Spine` | `Bone_005` |
| `Chest` | `Bone_003` |
| `UpperChest` | `Bone_002` |
| `Neck` | `Bone_018` |
| `Head` | `Bone_017` |
| `LeftShoulder` | `Bone_028` |
| `LeftUpperArm` | `Bone_027` |
| `LeftLowerArm` | `Bone_026` |
| `LeftHand` | `Bone_025` |
| `RightShoulder` | `Bone_023` |
| `RightUpperArm` | `Bone_022` |
| `RightLowerArm` | `Bone_021` |
| `RightHand` | `Bone_020` |
| `LeftUpperLeg` | `Bone_015` |
| `LeftLowerLeg` | `Bone_014` |
| `LeftFoot` | `Bone_013` |
| `LeftToes` | `Bone_012` |
| `RightUpperLeg` | `Bone_010` |
| `RightLowerLeg` | `Bone_009` |
| `RightFoot` | `Bone_008` |
| `RightToes` | `Bone_007` |

4. กด Reimport — แอนิเมชันจาก Mixamo หรือไฟล์อื่นที่จับคู่ Humanoid แล้วจะใช้กับร่างนี้ได้

ตารางนี้ได้จากหน้า "ร่างพื้นฐาน 3D" ใน Star Studio (จับคู่จากรูปร่างโครงกระดูก) — เปิดดู/แก้ได้ที่นั่น แล้วกด "ดู JSON" เพื่อเอาค่าล่าสุด

## 3. จำนวนสามเหลี่ยม
132,124 สามเหลี่ยม ยังมากไป: Godot สร้าง LOD ให้เอง (`Meshes > Generate LODs` เปิดอยู่แล้ว) ช่วยตอนมองไกล แต่ตอนซูมเข้าหมู่บ้านยังหนัก — ลดใน Blender (Decimate) เหลือ 8,000–15,000 ก่อนทำเกมจริง

> ขั้นตอนในหน้านี้เขียนตามเมนู Godot 4.x ยังไม่ได้ลองในโปรเจกต์ Godot จริง (ยังไม่ได้สร้างโปรเจกต์ ดู D4)

# นำร่างพื้นฐานเข้า Godot 4

ร่างที่ใช้ในเกม: **[`assets/models/char10-npc.glb`](../assets/models/char10-npc.glb)** (0.7 MB, 12,000 สามเหลี่ยม, วัสดุ `Skin` `Shirt` `Pants` `Footwear`, texture ผิว 1024px ชิ้นเดียว) — ทำจากต้นฉบับ [`Meshy_AI_Character_output_10.glb`](../assets/models/Meshy_AI_Character_output_10.glb) (Meshy SmartRig, กระดูก 69 ชิ้น มีนิ้วครบ, สูง 1.7 เมตร, หันหน้า +Z) ด้วย `tools/models/make_npc_body.py` — ดู D15/D16 ใน [`DECISIONS.md`](DECISIONS.md)

- เปลี่ยนสีชุด: ตั้ง `albedo_color` ของวัสดุ `Shirt` (สีหลัก) `Pants` (สีรอง) ต่อ NPC (ใช้ `material_override` หรือ `set_surface_override_material` กับสำเนาของวัสดุ) — `Skin` มี texture ที่ปรับให้สว่าง สีผิวมาจาก `albedo_color` เช่นกัน
- ข้อ 1 และ 3 ด้านล่างใช้กับต้นฉบับเท่านั้น `char10-npc.glb` ย่อ texture และลดสามเหลี่ยมแล้ว

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
ชื่อกระดูกเป็น `Bone_000…` Godot เดาเองไม่ได้ ให้ใส่เอง หรือใช้ไฟล์ที่ทำไว้แล้ว [`assets/models/Meshy_AI_Character_output_10.bonemap.tres`](../assets/models/Meshy_AI_Character_output_10.bonemap.tres) (ข้อ 2 เลือก `Bone Map` → Load แทน New BoneMap):
1. ดับเบิลคลิกไฟล์ .glb → หน้าต่าง Advanced Import Settings → คลิก `Skeleton3D` ทางซ้าย (ใน `char10-npc.glb` อยู่ที่ `SmartRigArmature/Skeleton3D`)
2. `Retarget > Bone Map` → New BoneMap → `Profile` = `SkeletonProfileHumanoid`
3. ใส่ตามตารางนี้ (ครบทุกตำแหน่งรวมนิ้วอยู่ใน [`assets/models/Meshy_AI_Character_output_10.bonemap.json`](../assets/models/Meshy_AI_Character_output_10.bonemap.json))

| Godot | กระดูกในไฟล์ |
|---|---|
| `Hips` | `Bone_000` |
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

4. กด Reimport — โครงกระดูกจะเปลี่ยนชื่อเป็น `GeneralSkeleton` และกระดูกเป็นชื่อมาตรฐาน (`Hips`, `LeftUpperArm` …) แล้วใช้ท่าในข้อ 4 ได้

> **`Hips` ต้องเป็น `Bone_000`** (กระดูกรากที่อยู่ระดับสะโพก) ไม่ใช่ `Bone_001` — ท่าทางเก็บความสูงสะโพกแบบนับจากรากโครงกระดูก ถ้าใส่ `Bone_001` ตัวจะลอยสูงขึ้นราว 1 เมตร (ทดสอบแล้ว)

ตารางนี้ได้จากหน้า "ร่างพื้นฐาน 3D" ใน Star Studio (จับคู่จากรูปร่างโครงกระดูก) — เปิดดู/แก้ได้ที่นั่น แล้วกด "ดู JSON" เพื่อเอาค่าล่าสุด

## 3. จำนวนสามเหลี่ยม
132,124 สามเหลี่ยม ยังมากไป: Godot สร้าง LOD ให้เอง (`Meshes > Generate LODs` เปิดอยู่แล้ว) ช่วยตอนมองไกล แต่ตอนซูมเข้าหมู่บ้านยังหนัก — ลดใน Blender (Decimate) เหลือ 8,000–15,000 ก่อนทำเกมจริง

## 4. ท่าทาง (AnimationLibrary + Retarget)
ท่าทั้งหมดอยู่ใน [`assets/animations/`](../assets/animations/) (425 ท่า ไฟล์ละ 1 ท่า มีแค่กระดูก + ท่า ดู [`README.md`](../assets/animations/README.md)) ทุกท่าใช้กระดูก Mixamo หรือ Meshy จึงต้อง **นำเข้าเป็น AnimationLibrary พร้อม BoneMap** เพื่อแปลงชื่อกระดูกเป็นชื่อมาตรฐานแบบเดียวกับร่างพื้นฐาน

BoneMap ที่ทำไว้แล้ว (ใน [`assets/animations/godot/`](../assets/animations/godot/)):

| `skeleton` ใน index.json | BoneMap | หมายเหตุ |
|---|---|---|
| `mixamorig` (41 / 65 / 133 กระดูก) | `bonemap_mixamo.tres` | Godot เปลี่ยน `mixamorig:Hips` เป็น `mixamorig_Hips` ตอนนำเข้า BoneMap ต้องใช้ชื่อแบบ `_` |
| `mixamorig_meshy` (28 กระดูก) | `bonemap_mixamo.tres` | ไม่มีนิ้ว |
| `meshy_api` (24 กระดูก, ท่าหอก) | `bonemap_meshy_api.tres` | `Spine02`→Spine, `Spine01`→Chest, `Spine`→UpperChest |

### ทางลัด: ตั้งค่าทั้ง 425 ไฟล์ด้วยสคริปต์ (แนะนำ)
1. คัดลอก `assets/animations/` ทั้งโฟลเดอร์ (รวม `godot/`) ไปไว้ในโปรเจกต์ เช่น `res://animations/`
2. รัน `python tools/godot/make_anim_imports.py <โฟลเดอร์โปรเจกต์> <โฟลเดอร์โปรเจกต์>/animations` — สร้างไฟล์ `.import` ให้ทุกท่า: นำเข้าแบบ `Animation Library`, ใส่ BoneMap ตามชนิดกระดูก, ตัด track ของกระดูกที่ไม่ได้จับคู่, ตั้งวนซ้ำให้ท่าที่ `loop: true`
3. เปิด Godot (หรือ `godot --headless --import`) ให้นำเข้าใหม่

### ทำเองทีละไฟล์ (ใน Editor)
1. เลือกไฟล์ท่า .glb → แท็บ Import → `Import As` = **Animation Library** → Reimport
2. ดับเบิลคลิกไฟล์ → Advanced Import Settings → คลิก `Skeleton3D` → `Retarget > Bone Map` = Load `bonemap_mixamo.tres` (หรือ `bonemap_meshy_api.tres`) → เปิด `Remove Tracks > Unmapped Bones`
3. ท่าที่วนซ้ำ: คลิกชื่อท่าใต้ `AnimationPlayer` → `Settings > Loop Mode` = Linear → Reimport

### ใช้กับ NPC
```gdscript
var body := preload("res://assets/models/char10-npc.glb").instantiate()   # ร่างที่ตั้ง BoneMap แล้ว (ข้อ 2)
add_child(body)
var ap := AnimationPlayer.new()
body.add_child(ap)                                              # root_node = ".." คือตัว body
ap.add_animation_library("walk", load("res://animations/general/female_walking.glb"))
ap.play("walk/female_walking")                                  # "<ชื่อคลัง>/<clip_name ใน index.json>"
```
- track ในท่าเป็น `%GeneralSkeleton:<ชื่อมาตรฐาน>` จึงใช้กับทุกร่างที่ตั้ง BoneMap แล้ว (ร่างชาย/เด็กในอนาคตก็ใช้ชุดเดียวกัน)
- ท่าที่ `root_motion: true` สะโพกเคลื่อนที่ไปจริง — NPC ในเกมควรให้ระบบเดินเลื่อนตัวเอง แล้วใช้ท่าแบบอยู่กับที่ (ท่าเดิน/วิ่งตรงส่วนใหญ่อยู่กับที่แล้ว) หรือใช้ `AnimationTree` + Root Motion ภายหลัง
- **อย่าตั้งชื่อท่าลงท้ายด้วย `_loop` / `_cycle`** Godot จะตัดคำนั้นออกจากชื่อเอง

### ผลทดสอบ (Godot 4.7.2, ทำแบบ headless)
- นำเข้าร่างพื้นฐาน (`char10-base.glb` และ `char10-npc.glb`) + ท่าทั้ง 425 ไฟล์ด้วยวิธีทางลัด: ไม่มี error
- เล่นทุกท่าบนร่างพื้นฐาน: track ผูกกับกระดูกครบทุกท่า, เท้าอยู่ระดับพื้น (ยกเว้นท่าตก/กระโดดที่ลอยจริง), ท่าวน 167/167 ตั้งค่าถูก
- ตัวอย่าง: ยืน (มือห้อยลงจาก T-pose ถูกต้อง) · คุกเข่า (สะโพกลดจาก 0.99 เหลือ 0.50 ม.) · เดิน (เท้าสลับยก)

> ข้อ 1 (ย่อ texture) และข้อ 3 (LOD) เขียนตามเมนู Godot 4.x ยังไม่ได้ลองจริง — ยังไม่ได้สร้างโปรเจกต์เกม (D4)

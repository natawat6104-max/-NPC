# ส่งต่องาน — พงศาวดารใต้ดวงดาว

เอกสารนี้สรุปทุกอย่างที่ทำมาแล้วและงานที่ค้าง สำหรับ Claude Code ที่รับงานต่อ (เช่นบนเครื่อง PC ของผู้ใช้) อ่านไฟล์นี้ก่อน แล้วอ่าน [`DECISIONS.md`](DECISIONS.md)

## วิธีทำงานกับผู้ใช้
- **คุยภาษาไทยทั้งหมด** รวมข้อความแจ้งความคืบหน้าระหว่างทำงาน
- **อธิบายสั้นและง่าย** ถ้ายาวผู้ใช้จะงง ให้ขั้นตอนเป็นข้อ ๆ ไม่เกินที่จำเป็น
- ผู้ใช้ชอบให้ **ทำให้เลย** มากกว่าถามเยอะ; ถ้าต้องตัดสินใจเรื่องออกแบบ ให้เสนอเป็นตัวเลือกให้กดเลือก พร้อมบอกว่าแนะนำข้อไหน
- พอผู้ใช้ตัดสินใจแล้ว บันทึกเป็นข้อใหม่ใน `DECISIONS.md` (ข้อถัดไปคือ D16)
- ผู้ใช้ใช้ Windows; ไฟล์ของผู้ใช้อยู่ที่ `C:\Users\Jame\Downloads`

## กติกา repo
- ทำงานบน branch `ccr-a2c4e75d-gm4mpx` และ push ขึ้น branch นี้ (`git push -u origin ccr-a2c4e75d-gm4mpx`)
- ไม่เปิด Pull Request จนกว่าผู้ใช้จะขอ
- ห้ามใส่ชื่อรุ่นโมเดล AI ใน commit หรือไฟล์ใน repo
- ตัวเลข balance มีที่เดียวคือ `data/balance.json`; แก้แล้วรัน `python tools/gen_balance_doc.py` เพื่อสร้าง `docs/BALANCE.md` ใหม่ (`--check` ไว้ตรวจว่าตรงกัน)
- GDD ทั้ง 15 ไฟล์อยู่ใน `docs/gdd/` (ต้นฉบับ .docx ใน `docs/gdd/original/`); ถ้า GDD ขัดกับ `DECISIONS.md` ให้ถือ `DECISIONS.md`

## ภาพรวมเกม (ย่อ)
- NPC ใช้ชีวิตเอง (Utility AI + Behavior Tree, จำลองด้วย seed ทำซ้ำได้, อธิบายเหตุผลการตัดสินใจได้)
- ผู้เล่นเป็น "กลุ่มดาว" เฝ้ามองจากฟ้าและชี้นำด้วยอิทธิพลจำกัด
- เล่นคนเดียวก่อน (D1), หยุด/เร่งเวลาได้ (D2), Godot (D4), ภาพ 3D มองเฉียงจากฟ้าแบบ Godus (D14)
- ต้นแบบแรก: ระบบจำลอง + บันทึกข้อความ (D10)

## สิ่งที่มีแล้ว
| ไฟล์ | คืออะไร |
|---|---|
| `docs/DECISIONS.md` | ข้อตัดสินใจ D1–D15 + เรื่องที่ยังไม่ตัดสิน |
| `docs/BALANCE.md`, `data/balance.json`, `tools/gen_balance_doc.py` | ตัวเลขกลางของเกม |
| `docs/mockups/star-watcher-3d.html` | ต้นแบบมุมมองกลุ่มดาว 3D (อวกาศ → ภูมิภาค → หมู่บ้าน) |
| `docs/mockups/star-studio.html` | **Star Studio** — editor เนื้อหาเกม (ดูหัวข้อถัดไป) |
| `assets/models/Meshy_AI_Character_output_10.glb` | **ร่างพื้นฐานของ NPC ทุกตัว** (D15) Meshy SmartRig กระดูก 69 ชิ้น `Bone_000…Bone_068` มีนิ้วครบ สูง 1.7 m หันหน้า +Z, 132k สามเหลี่ยม, texture 4096 |
| `assets/models/Meshy_AI_Character_output_10.bonemap.json` | จับคู่กระดูกกับ `SkeletonProfileHumanoid` ของ Godot (ตรวจแล้ว ครบ 52 ตำแหน่ง) |
| `docs/mockups/models/char10-base.glb` | ร่างพื้นฐานฉบับย่อ texture 1024/1024/512 (Studio โหลดตัวนี้) |
| `docs/GODOT-IMPORT.md` | วิธีนำร่างและท่าทางเข้า Godot (ขนาด texture, bone map, AnimationLibrary) — ส่วนท่าทางทดสอบกับ Godot 4.7.2 แล้ว |
| `assets/animations/` | **ท่าทาง 425 ท่า** (.glb มีแค่กระดูก + ท่า, 34.6 MB) แบ่ง `general/ work/ guard/ combat/ other/` + `index.json` + `README.md` (ภาษาไทย) + BoneMap ของ Godot ใน `godot/` |
| `tools/animations/` | สคริปต์แปลงท่าจาก Downloads ด้วย Blender (รันซ้ำได้ ดู README ในโฟลเดอร์) |
| `tools/godot/make_anim_imports.py` | สร้างไฟล์ `.import` ให้ท่าทั้งหมดใน Godot (AnimationLibrary + BoneMap + loop) |
| `assets/models/Meshy_AI_fantasy_teen_bald_…fbx` | ร่างตัวแรก เลิกใช้แล้ว |

## Star Studio (`docs/mockups/star-studio.html`)
- ไฟล์ HTML เดียว ใช้ three.js r128 จาก CDN (cdnjs + jsdelivr: GLTFLoader, FBXLoader, fflate, SkeletonUtils) — ต้องเปิดผ่านเว็บเซิร์ฟเวอร์**ที่โฟลเดอร์หลักของ repo** (`python -m http.server` แล้วเปิด `http://localhost:8000/docs/mockups/star-studio.html`) เพราะท่าทางโหลดจาก `../../assets/animations/` ถ้าเปิดเป็นไฟล์ตรง ๆ จะโหลดโมเดลตัวอย่างและท่าไม่ได้
- หน้า: ภาพรวม · แผนที่และเส้นทาง · ตัวละคร NPC · รูปลักษณ์ตัวละคร · **ร่างพื้นฐาน 3D** · มอนสเตอร์ · สินค้าและราคา · แม่แบบภารกิจ · วิกฤตประจำบท · แม่แบบพงศาวดาร · พลังกลุ่มดาว · ตัวเลข Balance · ทดสอบจำลอง
- โครงโค้ด: state `S` (บันทึกร่างใน localStorage `star-studio-draft-v1`), `ui`, แต่ละหน้าคือฟังก์ชันใน `SEC_FN`, `render()`/`derived()`, event แบบ delegate ด้วย `data-*`, ตรวจข้อมูลใน `issues()`, จำลองย่อใน `simulate()`
- รูปลักษณ์: `n.look` ต่อ NPC (ผม หมวก เครา สีผิว ชุด ของถือ สีตามอาชีพ สัดส่วน `body`) — ชิ้นหมวก/ผม/ของถือสร้างใน `headParts/torsoParts/handParts`
- ร่างพื้นฐาน: `S.bodies` เก็บแค่ค่าตั้ง (bone map, วัสดุ→สี, ทิศ, ขนาดหมวก) ไฟล์โมเดลเก็บใน IndexedDB; จับคู่กระดูกด้วยชื่อ (`autoMapBones`) ถ้าไม่ได้ใช้รูปร่างโครง (`structuralMap`); ท่าเดิน/ทำงาน/ยืนทำเองใน `animImported` (หมุนกระดูกตามกรอบของตัวละคร) และกำมือตอนถือเครื่องมือ
- **ท่าจริง:** `loadAnimIndex()` อ่าน `assets/animations/index.json`, `animClip()` โหลดทีละท่าตอนใช้, `bakeClip()` สุ่มท่าที่ 30 fps เป็นการหมุนของกระดูกแต่ละตำแหน่ง (Humanoid) เทียบท่ายืนต้นแบบ, `bindClip()` หมุนกระดูกของร่างให้ชี้ทางเดียวกับต้นแบบก่อน (ท่า T-pose ใช้กับร่าง A-pose ได้), `playClip()` เล่นแบบอยู่กับที่; กิจกรรม `ACTIVITIES` (ยืน เดิน ตีเหล็ก เก็บเกี่ยว แบกของ รักษา คุย นั่ง ยาม) ผูกท่าใน `S.animSet` (ค่าเริ่มต้น `DEFAULT_ANIM_SET`) และปุ่ม "ทำงาน" เล่นท่าตามอาชีพ (`ROLE_WORK`); ระหว่างโหลดหรือบนร่างหัวโตใช้ท่าที่ทำเองใน `animImported` เหมือนเดิม
- โมเดลตัวอย่าง: `SAMPLE_BODY` (v3 — จับคู่ `Hips` = `Bone_000`) โหลด `models/char10-base.glb` อัตโนมัติ (บน claude.ai ใช้ `models/char10-base.glb.b64.txt` เพราะ artifact เสิร์ฟ .glb ไม่ได้)
- มีฉบับเผยแพร่ที่ claude.ai (artifact ส่วนตัวของผู้ใช้) — ไฟล์ใน repo คือต้นฉบับ

## งานที่ค้าง (เรียงตามลำดับ)
ทำเสร็จแล้ว (2026-10-10): ~~ท่าทางใน Downloads~~ → `assets/animations/` · ~~ใส่ท่าจริงใน Star Studio~~ · ~~คู่มือ Godot ส่วนท่าทาง~~

1. **ท่าที่ยังขาด** — ตอกค้อน/ตีเหล็ก, นั่งเก้าอี้, นั่งพื้น, นอน, กิน/ดื่ม, ถือตะเกียง, โบกมือ, สวดภาวนา (ตอนนี้ใช้ท่าฟันขวานลงแทนตีเหล็ก และคุกเข่าแทนนั่ง) — ถ้าผู้ใช้โหลดจาก Mixamo มาเพิ่ม: เพิ่มใน `LOOSE`/`PACKS` ของ `tools/animations/mkjobs.py` แล้วรันสคริปต์ตาม `tools/animations/README.md`
2. **ร่างพื้นฐานก่อนทำเกมจริง** — ลดใน Blender (Decimate) จาก 132k เหลือ 8k–15k สามเหลี่ยม; ยังไม่มีเสื้อผ้าและมีวัสดุชิ้นเดียว จึงเปลี่ยนสีชุดตามอาชีพไม่ได้ (ต้องมีชุดเป็นชิ้นหรือแยกวัสดุ) — ถามผู้ใช้ก่อนว่าจะทำชุดอย่างไร
3. **เริ่มโปรเจกต์ Godot** — ยังไม่ได้ตัดสิน (D4): เวอร์ชัน (เครื่องผู้ใช้มี Godot 4.7.2), GDScript หรือ C#, โครงสร้างโฟลเดอร์, เริ่มจากระบบจำลอง (D10) หรือจากภาพ — **คุยกับผู้ใช้ก่อน** ผู้ใช้เคยบอกว่า "เดี๋ยวคุยก่อน"
4. ฉบับเผยแพร่ของ Star Studio บน claude.ai ยังไม่มีท่าจริง (artifact เสิร์ฟ .glb ไม่ได้ ต้องแปลงเป็น base64 แบบ `char10-base.glb.b64.txt`) — ทำเมื่อผู้ใช้ขอ
5. เรื่องที่ยังไม่ตัดสินอื่น ๆ อยู่ท้าย `DECISIONS.md`

## ข้อควรรู้
- ไฟล์ FBX จาก Meshy/Mixamo มักตั้งสีพื้นวัสดุเป็นดำ (texture จะดำ) — Studio แก้ให้เอง ใน Godot ต้องตั้ง albedo เป็นขาว
- ทรงผมสั้นจากชิ้นส่วนยังไม่พอดีหัวของร่างใหม่ ปรับได้ด้วยแถบ "ขนาดหมวก/ผม" / "ยกหมวกขึ้นลง"
- ในไฟล์ bone map ของร่างพื้นฐาน `Hips` = `Bone_000` (กระดูกรากระดับสะโพก) — ถ้าใส่ `Bone_001` ท่าใน Godot จะทำให้ตัวลอยขึ้น ~1 ม.
- Godot เปลี่ยน `mixamorig:` เป็น `mixamorig_` ในชื่อกระดูก และตัด `_loop`/`_cycle` ท้ายชื่อท่า
- เครื่องผู้ใช้มี Blender 5.2 (`C:/Program Files/Blender Foundation/Blender 5.2/blender.exe`) และ Godot 4.7.2 (ติดตั้งผ่าน winget) ใช้แบบ headless ได้

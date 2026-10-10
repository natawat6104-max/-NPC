# สคริปต์สร้างท่าทาง (`assets/animations/`)

แปลงท่าจาก `C:\Users\Jame\Downloads` → ไฟล์ .glb ที่มีแค่กระดูก + ท่า ด้วย Blender (รันแบบไม่เปิดหน้าต่าง)

ต้องมี: Blender 5.x, Python 3 + numpy · `WORK` = โฟลเดอร์ชั่วคราวใดก็ได้ (ไม่ใช่ใน repo)

```bash
python tools/animations/extract_packs.py WORK            # แตก .zip ชุดท่า Mixamo
python tools/animations/mkjobs.py WORK WORK/out          # เลือกท่า ตั้งชื่อ แบ่งกลุ่ม → WORK/jobs_0..3.json
blender -b --factory-startup --python tools/animations/convert_blender.py -- WORK/jobs_0.json WORK/res_0.json   # ทำ 0..3 (รันพร้อมกันได้)
python tools/animations/analyze.py WORK                  # อ่านไฟล์ที่ได้: ความยาว กระดูก วนได้ไหม เคลื่อนที่ไหม
python tools/animations/build_index.py WORK .            # คัดลอกเข้า assets/animations/ + index.json + README.md
```

- เพิ่ม/ตัดชุดท่า: แก้ `PACKS` และ `LOOSE` ใน `mkjobs.py`
- คำอธิบายภาษาไทย: `thai.py` (แก้ทีละท่าได้ใน `OVERRIDE`)
- กฎ `loop`: `LOOP_KW` / `ONCE_KW` ใน `build_index.py`

import json, os, re, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from thai import thai, PREFIX
SP, REPO = sys.argv[1], sys.argv[2]
DEST = REPO + '/assets/animations'
a = json.load(open(SP + '/analysis.json', encoding='utf-8'))

PREFIXES = sorted([p for p in PREFIX if p], key=len, reverse=True)
LOOP_KW = re.compile(r'idle|walk|run|strafe|sneak|sprint|jog|breathing|crawl|dance|loop|falling_idle|watering|'
                     r'milking|pick_fruit|wheelbarrow_walk|holding_walk|box_walk|crouching|charge|biting')
ONCE_KW = re.compile(r'(^|_)to_|turn|stop|start|_end$|death|dying|dead|land|equip|disarm|draw|sheath|jump|'
                     r'react|impact|cover|attack|slash|kick|punch|stab|dive|dodge|trip|get_up|dump|plant|pull_plant|'
                     r'cast|power_up|taunt|block(?!_idle)|scream|fall_a_land|falling_to_roll|hard_landing|recoil|overdraw|_arrow')
LOOP_EXTRA = {'farm_dig_and_plant_seeds', 'farm_pull_plant', 'farm_pull_plant_2', 'talk_weight_shift'}

SKEL_NOTE = {
    ('mixamorig', 65): 'mixamorig 65 (มีนิ้ว)',
    ('mixamorig', 41): 'mixamorig 41 (ไม่มีนิ้ว)',
    ('mixamorig', 133): 'mixamorig 133 (มีนิ้ว + กระดูกผม Hair* ของตัวนินจา ไม่ต้องใช้)',
    ('mixamorig_meshy', 28): 'mixamorig 28 (Meshy v6 ไม่มีนิ้ว)',
    ('meshy_api', 24): 'Meshy API 24 (Hips, Spine02…)',
}

def prefix_of(clip):
    return next((p for p in PREFIXES if clip.startswith(p + '_')), '')

index = []
if os.path.isdir(DEST):
    for g in ('general', 'work', 'guard', 'combat', 'other'):
        shutil.rmtree(os.path.join(DEST, g), ignore_errors=True)
for x in sorted(a, key=lambda x: (['general', 'work', 'guard', 'combat', 'other'].index(x['group']), x['clip'])):
    clip = x['clip']
    loop = clip in LOOP_EXTRA or (bool(LOOP_KW.search(clip)) and not ONCE_KW.search(clip) and x['loop_err_deg'] <= 20)
    rel = f"{x['group']}/{clip}.glb"
    os.makedirs(os.path.join(DEST, x['group']), exist_ok=True)
    shutil.copyfile(x['out'], os.path.join(DEST, rel))
    index.append({
        'file': rel,
        'original_file': x['original_file'],
        'clip_name': clip,
        'group': x['group'],
        'duration_s': round(x['duration_s'], 3),
        'frames': x['frames'],
        'loop': loop,
        'root_motion': x['root_motion_ratio'] > 0.3,
        'skeleton': x['skeleton'],
        'bones': x['bones'],
        'size_bytes': os.path.getsize(os.path.join(DEST, rel)),
        'description_th': thai(clip, prefix_of(clip)),
    })

meta = {
    'note': 'ท่าทางตัดตัวโมเดลออกแล้ว เหลือกระดูก + ท่า; ชื่อกระดูกเหมือนไฟล์ต้นฉบับ (ต้อง retarget ไปที่ร่าง Bone_000… ผ่าน bone map)',
    'skeletons': {k[0] + '_' + str(k[1]): v for k, v in SKEL_NOTE.items()},
    'groups': {'general': 'ทั่วไป', 'work': 'งาน', 'guard': 'ยาม/ถืออาวุธ', 'combat': 'ต่อสู้', 'other': 'อื่น ๆ'},
    'root_motion': 'true = สะโพกเคลื่อนที่ไปจริงในท่า (ถ้าจะให้เดินอยู่กับที่ ให้ตัดแกนแนวนอนของ Hips ออก)',
    'clips': index,
}
json.dump(meta, open(DEST + '/index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(index), 'clips', sum(c['size_bytes'] for c in index) / 1e6, 'MB')
for c in index:
    print(c['group'][:3], c['clip_name'].ljust(36), 'L' if c['loop'] else '-', 'R' if c['root_motion'] else '-',
          f"{c['duration_s']:6.2f}", c['description_th'])

# ---- README (Thai) ----
GROUP_TH = [('general', 'ทั่วไป', 'ยืน เดิน วิ่ง หัน กระโดด ตก'),
            ('work', 'งาน', 'ทำไร่ เก็บเกี่ยว แบกของ เข็นรถ ท่าประกอบการคุย'),
            ('guard', 'ยาม / ถืออาวุธ', 'ยืน เดิน วิ่ง ขณะถืออาวุธ ชัก/เก็บอาวุธ — ใช้กับยามและนักผจญภัยตอนเดินทาง'),
            ('combat', 'ต่อสู้', 'โจมตี ป้องกัน โดนตี ล้มตาย ร่ายเวท'),
            ('other', 'อื่น ๆ', 'บาดเจ็บ เมา หลบซ่อน เต้นรำ มอนสเตอร์ ซอมบี้')]
from collections import Counter
cnt = Counter(c['group'] for c in index)
size = sum(c['size_bytes'] for c in index)
by = {c['clip_name']: c for c in index}
L = []
L.append('# ท่าทาง (Animations)\n')
L.append(f'ท่าทางทั้งหมด **{len(index)} ท่า** ขนาดรวม {size/1e6:.1f} MB — ตัดตัวโมเดลและ texture ออกแล้ว เหลือแค่กระดูก + ท่า (ไฟล์ .glb ไฟล์ละ 1 ท่า)\n')
L.append('ข้อมูลทุกท่าอยู่ใน [`index.json`](index.json): `file`, `original_file`, `clip_name`, `group`, `duration_s`, `frames`, `loop`, `root_motion`, `skeleton`, `bones`, `size_bytes`, `description_th`\n')
L.append('## สิ่งที่ต้องรู้ก่อนใช้')
L.append('- **ไม่มีท่าไหนใช้กระดูก `Bone_000…` ของร่างพื้นฐาน** — ทุกท่าต้อง retarget ผ่าน bone map ([`../models/Meshy_AI_Character_output_10.bonemap.json`](../models/Meshy_AI_Character_output_10.bonemap.json))')
L.append('- ชนิดกระดูก (`skeleton` + `bones`):')
for k, v in SKEL_NOTE.items():
    n = sum(1 for c in index if c['skeleton'] == k[0] and c['bones'] == k[1])
    L.append(f'  - {v} — {n} ท่า')
L.append('- ชื่อกระดูกเหมือนไฟล์ต้นฉบับ (`mixamorig:Hips` …) — three.js GLTFLoader จะตัด `:` ออกเหลือ `mixamorigHips`')
L.append('- `loop` = ท่าวนซ้ำได้ (ยืน เดิน วิ่ง ทำงานซ้ำ ๆ) · `false` = เล่นครั้งเดียว (โจมตี หัน ล้ม)')
L.append('- `root_motion` = สะโพกเคลื่อนที่ไปจริงในท่า (เดินเบี่ยงข้าง ล้ม เลี้ยว) ถ้าจะให้อยู่กับที่ให้ตัดแกนแนวนอนของ Hips — ท่าเดิน/วิ่งตรงส่วนใหญ่อยู่กับที่อยู่แล้ว')
L.append('- ความเร็ว: Mixamo 30 fps, Meshy 24 fps')
L.append('- ใช้ใน Star Studio: หน้า "ร่างพื้นฐาน 3D" → การ์ด "ท่าทางของกิจกรรม" (ต้องเปิดเว็บเซิร์ฟเวอร์ที่โฟลเดอร์หลักของ repo)')
L.append('- นำเข้า Godot: [`docs/GODOT-IMPORT.md`](../../docs/GODOT-IMPORT.md) ข้อ 4 — BoneMap อยู่ใน [`godot/`](godot/) และสคริปต์ตั้งค่าทุกไฟล์ `tools/godot/make_anim_imports.py`\n')
L.append('## ท่าแนะนำสำหรับกิจกรรม NPC\n')
L.append('| กิจกรรม | ท่าที่ใช้ได้ | หมายเหตุ |')
L.append('|---|---|---|')
REC = [
    ('ยืนพัก', ['idle', 'female_idle', 'adv_idle'], ''),
    ('เดิน', ['female_walking', 'adv_walking', 'meshy_casual_walk'], ''),
    ('วิ่ง', ['female_running', 'run'], ''),
    ('ตีเหล็ก', ['axe_attack_downward'], '**ยังไม่มีท่าตอกค้อนจริง** ใช้ท่าฟันขวานลงแทนชั่วคราว'),
    ('ขุด / ปลูก', ['farm_dig_and_plant_seeds', 'farm_plant_tree'], ''),
    ('เก็บเกี่ยว', ['farm_pull_plant', 'farm_pick_fruit'], ''),
    ('แบกของ', ['farm_box_idle', 'farm_box_walk_arc', 'farm_holding_walk', 'farm_wheelbarrow_walk'], ''),
    ('รักษา', ['magic_1h_cast_spell_01', 'farm_kneeling_idle'], 'ร่ายเวทมือเดียว / คุกเข่าข้างผู้ป่วย'),
    ('คุย', ['talk_weight_shift', 'talk_head_nod_yes', 'talk_happy_hand'], ''),
    ('นั่ง', ['farm_kneeling_idle', 'farm_cow_milking'], '**ยังไม่มีท่านั่งจริง** ใช้คุกเข่าแทน'),
    ('ยาม', ['spear_walk_inplace', 'sword_shield_idle', 'bow_idle_02_looking', 'axe_idle_looking_v_1'], ''),
    ('บาดเจ็บ', ['injured_walk', 'injured_hurting_idle'], ''),
    ('ล้ม / ลุก', ['trip_fall', 'get_up_from_ground'], 'เช่น โทมะลื่นล้มขากลับ (D8)'),
    ('ต่อสู้', ['sword_shield_slash', 'bow_draw_arrow', 'magic_2h_attack_01'], ''),
]
for act, clips, note in REC:
    L.append(f"| {act} | {' · '.join('`' + c + '`' for c in clips if c in by)} | {note} |")
L.append('\n**ยังขาด** (ถ้าต้องการ ดาวน์โหลดเพิ่มจาก Mixamo): ตอกค้อน/ตีเหล็ก (Hammering), นั่งเก้าอี้ (Sitting Idle, Sitting Talking), นั่งพื้น, นอน/หลับ (Sleeping), กิน/ดื่ม (Drinking), ถือตะเกียง, โบกมือทักทาย (Waving), สวดภาวนา (Praying)\n')
for g, th, desc in GROUP_TH:
    L.append(f'## {th} (`{g}/`) — {cnt[g]} ท่า')
    L.append(f'{desc}\n')
    L.append('| ไฟล์ | คำอธิบาย | วินาที | วน | เคลื่อนที่ | กระดูก |')
    L.append('|---|---|---:|:-:|:-:|---:|')
    for c in index:
        if c['group'] != g: continue
        L.append(f"| `{c['clip_name']}` | {c['description_th']} | {c['duration_s']:.2f} | {'✓' if c['loop'] else ''} | {'✓' if c['root_motion'] else ''} | {c['bones']} |")
    L.append('')
L.append('## ที่มาของไฟล์')
L.append(r'- ต้นฉบับอยู่ใน `C:\Users\Jame\Downloads` (ไม่ได้แก้ไฟล์ต้นฉบับ) — ชื่อไฟล์เดิมดูได้จาก `original_file` ใน `index.json`')
L.append('- ชุด Mixamo ที่ใช้: Action Adventure, Female Basic Locomotion, Male Locomotion, Farming, Gestures Basic, Male Drunk, Male Injured, Great Sword, Pro Sword and Shield, Pro Melee Axe, Pro Longbow, Pro Magic, Creature, Scary Zombie + ไฟล์ .fbx เดี่ยว 18 ไฟล์')
L.append('- Meshy: `Meshy_AI_v6_biped` (14 ท่า) และท่าหอก `Meshy_Spear_Walk_2_Variants` (2 ท่า)')
L.append('- **ไม่ได้ใส่** (ไม่เข้ากับเกม หรือซ้ำ): ชุดปืนทั้งหมด (Rifle, Shooter, Pistol), Breakdance, Capoeira, Soccer, Hip Hop, Free Test, ชุด Lite/ชุดย่อยที่ซ้ำกับชุด Pro, Action Adventure ฉบับซ้ำ (1)(2)(3), Great Sword (1), Locomotion/Basic Locomotion/Female Locomotion (ซ้ำกับชุดที่ใช้), Creature NPC, Not So Scary Zombie — ถ้าต้องการเพิ่ม รันสคริปต์ใน `tools/animations/` ใหม่ได้')
L.append('- ไฟล์ตัวโมเดลที่ไม่ใช่ท่า (มังกร ก็อบลิน เสือ ตัวละคร Meshy ฯลฯ) ไม่ได้นำมา')
open(DEST + '/README.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')

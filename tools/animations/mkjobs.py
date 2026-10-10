"""Build the conversion job list: which source clips go in, their short name and group."""
import glob, os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
DL = 'C:/Users/Jame/Downloads'
SP = sys.argv[1].replace(os.sep, '/')
OUT = sys.argv[2].replace(os.sep, '/')
EX = SP + '/extract'

COMBAT_KW = ('attack', 'slash', 'kick', 'punch', 'block', 'impact', 'death', 'dying', 'react', 'casting', 'cast',
             'power up', 'stab', 'combo', 'draw arrow', 'aim recoil', 'overdraw', 'dodge', 'dive', 'taunt', 'spell',
             'magic', 'charge', 'skill', 'dead', 'fight', 'swiping', 'roaring', 'flexing')
GUARD_KW = ('idle', 'walk', 'run', 'strafe', 'turn', 'crouch', 'jump', 'draw', 'sheath', 'equip', 'disarm', 'aim',
            'sprint', 'land', 'fall')

def weapon_group(name):
    n = name.lower()
    if any(k in n for k in COMBAT_KW):
        return 'combat'
    return 'guard'

# pack folder -> (prefix, strip words, group or function)
PACKS = {
    'Action Adventure Pack': ('adv', [], lambda n: 'other' if ('cover' in n or 'sneak' in n) else 'general'),
    'Female Basic Locomotion Pack': ('female', [], 'general'),
    'Male Locomotion Pack': ('male', [], 'general'),
    'Farming Pack': ('farm', [], 'work'),
    'Gestures Pack Basic': ('talk', [' gesture'], 'work'),
    'Male Drunk Pack': ('drunk', ['drunk '], 'other'),
    'Male Injured Pack': ('injured', ['injured '], 'other'),
    'Great Sword Pack': ('greatsword', ['a great sword', 'great sword ', 'two handed sword '], weapon_group),
    'Pro Sword and Shield Pack': ('sword_shield', ['sword and shield '], weapon_group),
    'Pro Melee Axe Pack': ('axe', ['standing melee ', 'standing '],
                           lambda n: 'general' if n.startswith('unarmed') and 'equip' not in n else weapon_group(n)),
    'Pro Longbow Pack': ('bow', ['standing '],
                         lambda n: 'general' if n.startswith(('unarmed', 'fall')) else weapon_group(n)),
    'Pro Magic Pack': ('magic', ['standing ', ' magic'], weapon_group),
    'Creature Pack': ('mutant', ['mutant '], 'other'),
    'Scary Zombie Pack': ('zombie', ['zombie '], 'other'),
}
SKIP_IN_PACK = {'X Bot', 'Y Bot', 'ninja-character-for-mixamo', 'ChibiWizard_Mixamo_OBJ_v001'}

# loose files kept (others are character models, guns, soccer, hip-hop, or duplicates of pack clips)
LOOSE = {
    'Idle.fbx': ('idle', 'general'),
    'Running.fbx': ('run', 'general'),
    'Slow Jog Backwards.fbx': ('jog_backwards', 'general'),
    'Jumping Down.fbx': ('jump_down', 'general'),
    'เวท/Idle To Sprint.fbx': ('idle_to_sprint', 'general'),
    'Fight Idle.fbx': ('fight_idle', 'combat'),
    'Punching.fbx': ('punch', 'combat'),
    'Punch Combo.fbx': ('punch_combo', 'combat'),
    'Mma Kick.fbx': ('kick_mma', 'combat'),
    'Double Dagger Stab.fbx': ('dagger_double_stab', 'combat'),
    'Sheath A Great Sword 2.fbx': ('greatsword_sheath_2', 'guard'),
    'Soccer Trip.fbx': ('trip_fall', 'other'),
    'Zombie Stand Up.fbx': ('get_up_from_ground', 'other'),
    'Dancing.fbx': ('dance', 'other'),
    'Strut Walking.fbx': ('strut_walk', 'other'),
    'Catwalk Idle To Twist R.fbx': ('catwalk_idle_twist_r', 'other'),
    'เวท/Catwalk Walk Forward 03.fbx': ('catwalk_walk_03', 'other'),
    'เวท/Catwalk Walk Forward Turn 90R.fbx': ('catwalk_walk_turn_90r', 'other'),
}

MESHY_V6 = DL + '/Meshy_AI_v6_biped/Meshy_AI_v6_biped'
MESHY_GROUP = {'Running': 'general', 'Walking': 'general', 'Casual_Walk': 'general', 'Walk_Turn_Left': 'general',
               'Walk_Turn_Right': 'general', 'Walk_Turn_Left_with_Weapon': 'guard', 'Walk_Fight_Forward': 'guard'}

def slug(s):
    s = s.lower().replace('ver.', 'v').replace('degrees', 'deg')
    s = re.sub(r'\((\d+)\)', r' \1', s)
    s = re.sub(r'[^a-z0-9]+', '_', s).strip('_')
    return s

jobs, used = [], set()
def add(src, name, group, pack, original, pick=None):
    base = name
    k = 2
    while name in used:
        name = f'{base}_{k}'; k += 1
    used.add(name)
    jobs.append({'src': src, 'out': f'{OUT}/{group}/{name}.glb', 'clip': name, 'group': group,
                 'pack': pack, 'original_file': original, 'pick': pick})

for p, (name, group) in LOOSE.items():
    add(f'{DL}/{p}', name, group, None, p)

for pack, (prefix, strip, grp) in PACKS.items():
    for f in sorted(glob.glob(f'{EX}/{pack}/*.fbx')):
        raw = os.path.splitext(os.path.basename(f))[0]
        if raw in SKIP_IN_PACK:
            continue
        n = raw.lower()
        for w in strip:
            n = n.replace(w, ' ')
        g = grp(raw.lower()) if callable(grp) else grp
        add(f.replace(os.sep, '/'), f'{prefix}_{slug(n)}', g, pack + '.zip', f'{pack}.zip/{os.path.basename(f)}')

for f in sorted(glob.glob(MESHY_V6 + '/*_withSkin.glb')):
    act = re.match(r'.*_Animation_(.+)_withSkin\.glb', f.replace(os.sep, '/')).group(1)
    add(f.replace(os.sep, '/'), 'meshy_' + slug(act), MESHY_GROUP.get(act, 'combat'), 'Meshy_AI_v6_biped.zip',
        'Meshy_AI_v6_biped/' + os.path.basename(f), pick=act)

sp = DL + '/Meshy_ท่าหอก/Meshy_Spear_Walk_2_Variants.glb'
add(sp, 'spear_walk', 'guard', None, 'Meshy_ท่าหอก/Meshy_Spear_Walk_2_Variants.glb', pick='Spear_Walk')
add(sp, 'spear_walk_inplace', 'guard', None, 'Meshy_ท่าหอก/Meshy_Spear_Walk_2_Variants.glb', pick='Spear_Walk_inplace')

json.dump(jobs, open(SP + '/jobs_all.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
from collections import Counter
print(len(jobs), Counter(j['group'] for j in jobs))
# split into 4 chunks for parallel Blender runs
for i in range(4):
    json.dump(jobs[i::4], open(f'{SP}/jobs_{i}.json', 'w', encoding='utf-8'), ensure_ascii=False)

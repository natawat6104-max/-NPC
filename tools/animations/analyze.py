"""Read exported GLBs: duration, bones, loop/root-motion detection. Writes analysis.json."""
import json, struct, sys, os, glob
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
SP = sys.argv[1]
jobs = json.load(open(SP + '/jobs_all.json', encoding='utf-8'))
res = {}
for i in range(4):
    for r in json.load(open(f'{SP}/res_{i}.json', encoding='utf-8')):
        res[r['out']] = r

CT = {5126: ('f', 4), 5123: ('H', 2), 5121: ('B', 1), 5125: ('I', 4)}
NC = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}

def load(p):
    b = open(p, 'rb').read()
    l = struct.unpack_from('<I', b, 12)[0]
    j = json.loads(b[20:20 + l])
    o = 20 + l
    bl = struct.unpack_from('<I', b, o)[0]
    bin_ = b[o + 8:o + 8 + bl]
    def acc(i):
        a = j['accessors'][i]; bv = j['bufferViews'][a['bufferView']]
        fmt, sz = CT[a['componentType']]; n = NC[a['type']]
        off = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
        arr = np.frombuffer(bin_, dtype='<' + fmt, count=a['count'] * n, offset=off).astype(np.float64)
        return arr.reshape(a['count'], n)
    return j, acc

def qang(a, b):
    d = abs(float(np.dot(a / np.linalg.norm(a), b / np.linalg.norm(b))))
    return np.degrees(2 * np.arccos(min(1.0, d)))

out = []
for job in jobs:
    p = job['out']
    r = res.get(p, {})
    e = dict(job)
    e['error'] = r.get('error')
    if not os.path.exists(p):
        e['error'] = e['error'] or 'missing output'
        out.append(e); continue
    j, acc = load(p)
    nodes = j['nodes']
    names = [n.get('name', '') for n in nodes]
    joints = [names[k] for k in j['skins'][0]['joints']] if j.get('skins') else names
    e['size_bytes'] = os.path.getsize(p)
    e['bones'] = len(joints)
    e['has_mesh'] = bool(j.get('meshes'))
    e['images'] = len(j.get('images', []))
    if any(n.startswith('mixamorig:') for n in joints):
        e['skeleton'] = 'mixamorig' if len(joints) > 30 else 'mixamorig_meshy'
    elif 'Hips' in joints and 'Spine02' in joints:
        e['skeleton'] = 'meshy_api'
    elif any(n.startswith('Bone_') for n in joints):
        e['skeleton'] = 'meshy_smartrig'
    else:
        e['skeleton'] = 'unknown'
    anims = j.get('animations', [])
    e['clip_names'] = [a.get('name') for a in anims]
    if not anims:
        e['error'] = e['error'] or 'no animation'
        out.append(e); continue
    a = anims[0]
    tmax, loop_err, hips = 0, 0, None
    for ch in a['channels']:
        s = a['samplers'][ch['sampler']]
        t = acc(s['input'])[:, 0]; v = acc(s['output'])
        tmax = max(tmax, float(t[-1]))
        tgt = names[ch['target']['node']]
        if ch['target']['path'] == 'rotation' and len(v) > 1:
            loop_err = max(loop_err, qang(v[0], v[-1]))
        if ch['target']['path'] == 'translation' and tgt.endswith('Hips'):
            hips = v
    e['duration_s'] = round(tmax, 3)
    e['frames'] = len(acc(a['samplers'][0]['input']))
    e['loop_err_deg'] = round(loop_err, 1)
    hn = next((n for n in nodes if n.get('name', '').endswith('Hips')), None)
    rest = np.array(hn.get('translation', [0, 0, 0])) if hn else np.zeros(3)
    hh = float(np.linalg.norm(rest)) or 1.0
    if hips is not None and len(hips) > 1:
        # hips local space: Mixamo hips translation is in armature space (Y up after export)
        d = hips[-1] - hips[0]
        horiz = float(np.hypot(d[0], d[2]))
        e['root_motion_ratio'] = round(horiz / hh, 2)  # horizontal travel / hips height
        e['hips_drop_ratio'] = round(float((hips[:, 1].min() - rest[1]) / hh), 2)
    else:
        e['root_motion_ratio'] = 0.0
    out.append(e)

json.dump(out, open(SP + '/analysis.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
errs = [x for x in out if x.get('error')]
print('total', len(out), 'errors', len(errs))
for x in errs: print('ERR', x['clip'], x['error'][-200:])
from collections import Counter
print(Counter((x.get('skeleton'), x.get('bones')) for x in out))
print('size MB', sum(x.get('size_bytes', 0) for x in out) / 1e6, 'max', max(x.get('size_bytes', 0) for x in out))
print('mesh', [x['clip'] for x in out if x.get('has_mesh') or x.get('images')])
print('clipname mismatch', [(x['clip'], x['clip_names']) for x in out if x.get('clip_names') != [x['clip']]][:10])
for x in sorted(out, key=lambda x: -x.get('root_motion_ratio', 0))[:25]:
    print('RM', x['clip'], x.get('root_motion_ratio'), x.get('duration_s'), x.get('loop_err_deg'))

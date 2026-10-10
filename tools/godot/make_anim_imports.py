"""Write Godot .import files so every clip in assets/animations imports as a retargeted AnimationLibrary.

usage: python tools/godot/make_anim_imports.py <godot project dir> [<animations dir inside the project>]

The animations folder (with index.json) and the BoneMap files (bonemap_mixamo.tres, bonemap_meshy_api.tres)
must already be copied into the project. Existing .import files are overwritten; open the editor or run
`godot --headless --import` afterwards to (re)import.
"""
import json, os, struct, sys

proj = os.path.abspath(sys.argv[1])
anim_dir = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(proj, 'animations')
maps_dir = os.path.join(anim_dir, 'godot')
BONEMAP = {'mixamorig': 'bonemap_mixamo.tres', 'mixamorig_meshy': 'bonemap_mixamo.tres', 'meshy_api': 'bonemap_meshy_api.tres'}

def res_path(p):
    return 'res://' + os.path.relpath(p, proj).replace(os.sep, '/')

def top_node(glb):
    b = open(glb, 'rb').read()
    j = json.loads(b[20:20 + struct.unpack_from('<I', b, 12)[0]])
    return j['nodes'][j['scenes'][0]['nodes'][0]]['name']

index = json.load(open(os.path.join(anim_dir, 'index.json'), encoding='utf-8'))
n = 0
for c in index['clips']:
    glb = os.path.join(anim_dir, c['file'])
    bm = res_path(os.path.join(maps_dir, BONEMAP[c['skeleton']]))
    skel = top_node(glb) + '/Skeleton3D'
    loop = ', "animations": {"%s": {"settings/loop_mode": 1}}' % c['clip_name'] if c['loop'] else ''
    sub = '{"nodes": {"PATH:%s": {"retarget/bone_map": Resource("%s"), "retarget/remove_tracks/unmapped_bones": true}}%s}' % (skel, bm, loop)
    with open(glb + '.import', 'w', encoding='utf-8', newline='\n') as f:
        f.write('[remap]\n\nimporter="animation_library"\nimporter_version=1\ntype="AnimationLibrary"\n\n')
        f.write('[deps]\n\nsource_file="%s"\n\n' % res_path(glb))
        f.write('[params]\n\nanimation/fps=30\nanimation/trimming=false\nanimation/remove_immutable_tracks=true\n')
        f.write('_subresources=%s\n' % sub)
    n += 1
print('wrote', n, '.import files')

"""Blender (headless): turn the Meshy base body into the in-game NPC body (D16).

- splits the surface into Skin / Shirt / Pants / Footwear materials from the skin weights
  (long sleeves, trousers, boots) so outfit colours can follow role and look
- decimates to about 12,000 triangles
- keeps one 1024px colour texture on Skin, brightened so the tint sets the skin tone
  (painted face details stay); clothes are flat colours

usage: blender -b --factory-startup --python tools/models/make_npc_body.py -- <in.glb> <bonemap.json> <out.glb> [target_tris]
"""
import bpy, bmesh, json, sys, os
import numpy as np

argv = sys.argv[sys.argv.index('--') + 1:]
src, bonemap_path, out = argv[0], argv[1], argv[2]
target = int(argv[3]) if len(argv) > 3 else 12000

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
sc = bpy.context.scene
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)  # importer's bone-shape helper
body = next(o for o in sc.objects if o.type == 'MESH')
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
slot_bone = json.load(open(bonemap_path, encoding='utf-8'))['bone_map']

REGION_OF_SLOT = {}
for s in ('Head', 'Neck'):
    REGION_OF_SLOT[s] = 'Skin'
for s in ('Spine', 'Chest', 'UpperChest'):
    REGION_OF_SLOT[s] = 'Shirt'
REGION_OF_SLOT['Hips'] = 'Pants'
for side in ('Left', 'Right'):
    for s in ('Shoulder', 'UpperArm', 'LowerArm'):
        REGION_OF_SLOT[side + s] = 'Shirt'
    REGION_OF_SLOT[side + 'Hand'] = 'Skin'
    for s in ('UpperLeg', 'LowerLeg'):
        REGION_OF_SLOT[side + s] = 'Pants'
    for s in ('Foot', 'Toes'):
        REGION_OF_SLOT[side + s] = 'Footwear'
for slot, b in slot_bone.items():
    if slot not in REGION_OF_SLOT and ('Thumb' in slot or 'Index' in slot or 'Middle' in slot or 'Ring' in slot or 'Little' in slot):
        REGION_OF_SLOT[slot] = 'Skin'

# every bone -> region of its nearest mapped ancestor (or itself)
region_of_bone = {}
bone_slot = {b: s for s, b in slot_bone.items()}
for bone in arm.data.bones:
    b = bone
    while b and b.name not in bone_slot:
        b = b.parent
    region_of_bone[bone.name] = REGION_OF_SLOT.get(bone_slot[b.name], 'Shirt') if b else 'Pants'

ORDER = ['Skin', 'Shirt', 'Pants', 'Footwear']
me = body.data
gi_region = {g.index: ORDER.index(region_of_bone.get(g.name, 'Shirt')) for g in body.vertex_groups}
vreg = np.zeros((len(me.vertices), len(ORDER)))
for v in me.vertices:
    for g in v.groups:
        if g.group in gi_region:
            vreg[v.index, gi_region[g.group]] += g.weight
vz = np.array([(body.matrix_world @ v.co).z for v in me.vertices])

# boots reach above the ankle
mw = arm.matrix_world
ankle = min((mw @ arm.data.bones[slot_bone[s]].head_local).z for s in ('LeftFoot', 'RightFoot'))
knee = min((mw @ arm.data.bones[slot_bone[s]].head_local).z for s in ('LeftLowerLeg', 'RightLowerLeg'))
boot_top = ankle + (knee - ankle) * 0.35
print('ankle %.3f knee %.3f boot_top %.3f' % (ankle, knee, boot_top))

mats = {}
for name, col, tex in [('Skin', (1, 1, 1, 1), True), ('Shirt', (0.8, 0.8, 0.8, 1), False), ('Pants', (0.5, 0.5, 0.5, 1), False), ('Footwear', (0.16, 0.10, 0.06, 1), False)]:
    m = bpy.data.materials.new(name); m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    bsdf.inputs['Base Color'].default_value = col
    bsdf.inputs['Roughness'].default_value = 0.85
    bsdf.inputs['Metallic'].default_value = 0.0
    mats[name] = (m, bsdf)

# skin texture: original colour map at 1024px, divided by the typical skin colour so the material tint becomes the tone
old = me.materials[0]
img = next(n.image for n in old.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image and n.outputs['Color'].links and
           any(l.to_socket.name == 'Base Color' for l in n.outputs['Color'].links))
img.scale(1024, 1024)
px = np.array(img.pixels[:], dtype=np.float32).reshape(-1, 4)
rgb = px[:, :3]
lum = rgb.mean(axis=1)
ref = np.median(rgb[(lum > np.percentile(lum, 20)) & (lum < np.percentile(lum, 95))], axis=0)
px[:, :3] = np.clip(rgb / ref, 0, 1)
skin_img = bpy.data.images.new('SkinTone', 1024, 1024)
skin_img.pixels[:] = px.ravel()
skin_img.file_format = 'JPEG'
skin_img.pack()
m, bsdf = mats['Skin']
tn = m.node_tree.nodes.new('ShaderNodeTexImage'); tn.image = skin_img
m.node_tree.links.new(tn.outputs['Color'], bsdf.inputs['Base Color'])

me.materials.clear()
for n in ORDER:
    me.materials.append(mats[n][0])
for p in me.polygons:
    votes = vreg[list(p.vertices)].sum(axis=0)
    r = int(np.argmax(votes))
    zc = vz[list(p.vertices)].mean()
    if ORDER[r] in ('Pants', 'Footwear') and zc < boot_top:
        r = ORDER.index('Footwear')
    elif ORDER[r] == 'Footwear' and zc >= boot_top:
        r = ORDER.index('Pants')
    p.material_index = r
# clean the borders: a face whose neighbours mostly belong to one other region joins it
edge_faces = {}
for p in me.polygons:
    for ek in p.edge_keys:
        edge_faces.setdefault(ek, []).append(p.index)
for _ in range(2):
    idx = np.array([p.material_index for p in me.polygons])
    for p in me.polygons:
        nb = [f for ek in p.edge_keys for f in edge_faces[ek] if f != p.index]
        if not nb:
            continue
        c = np.bincount(idx[nb], minlength=4)
        if c.max() >= 2 and int(np.argmax(c)) != idx[p.index]:
            p.material_index = int(np.argmax(c))
counts = np.bincount([p.material_index for p in me.polygons], minlength=4)
print('faces per region', dict(zip(ORDER, counts.tolist())))

# decimate (before the armature deform); vertices on region borders are protected so necklines and cuffs stay clean
border = set()
for ek, fs in edge_faces.items():
    if len({me.polygons[f].material_index for f in fs}) > 1:
        border.update(ek)
keep = body.vertex_groups.new(name='_decimate')
keep.add([v.index for v in me.vertices if v.index not in border], 1.0, 'REPLACE')
keep.add(list(border), 0.0, 'REPLACE')
bpy.context.view_layer.objects.active = body
body.select_set(True)
tris0 = sum(len(p.vertices) - 2 for p in me.polygons)
dec = body.modifiers.new('Decimate', 'DECIMATE')
dec.decimate_type = 'COLLAPSE'
dec.ratio = min(1.0, target / tris0)
dec.use_collapse_triangulate = True
dec.vertex_group = keep.name
dec.vertex_group_factor = 1000.0
while body.modifiers[0] != dec:
    bpy.ops.object.modifier_move_up(modifier=dec.name)
bpy.ops.object.modifier_apply(modifier=dec.name)
tris1 = sum(len(p.vertices) - 2 for p in me.polygons)
print('tris %d -> %d' % (tris0, tris1))
bpy.ops.mesh.customdata_custom_splitnormals_clear()
for p in me.polygons:
    p.use_smooth = True
body.vertex_groups.remove(body.vertex_groups['_decimate'])
counts = np.bincount([p.material_index for p in me.polygons], minlength=4)
print('faces after decimate', dict(zip(ORDER, counts.tolist())))

for o in list(bpy.data.materials):
    if o.users == 0:
        bpy.data.materials.remove(o)
for im in list(bpy.data.images):
    if im.users == 0:
        bpy.data.images.remove(im)

os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', export_skins=True, export_animations=False,
                          export_morph=False, export_image_format='JPEG', export_jpeg_quality=88, export_yup=True)
print('wrote', out, os.path.getsize(out))

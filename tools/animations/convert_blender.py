# Blender headless: import animation file, strip meshes/textures, export bones+anim GLB.
# usage: blender -b --factory-startup --python convert.py -- jobs.json results.json
import bpy, json, sys, os, traceback

argv = sys.argv[sys.argv.index('--') + 1:]
jobs = json.load(open(argv[0], encoding='utf-8'))
res_path = argv[1]
results = []

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def do_import(p):
    ext = os.path.splitext(p)[1].lower()
    if ext == '.fbx':
        bpy.ops.import_scene.fbx(filepath=p, automatic_bone_orientation=False, ignore_leaf_bones=False, use_anim=True)
    else:
        bpy.ops.import_scene.gltf(filepath=p)

for job in jobs:
    info = {'src': job['src'], 'out': job.get('out')}
    try:
        reset()
        do_import(job['src'])
        scn = bpy.context.scene
        arms = [o for o in scn.objects if o.type == 'ARMATURE']
        meshes = [o for o in scn.objects if o.type == 'MESH']
        info['meshes'] = len(meshes)
        info['tris'] = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in meshes)
        info['images'] = len(bpy.data.images)
        info['armatures'] = len(arms)
        info['fps'] = scn.render.fps / scn.render.fps_base
        if arms:
            a = arms[0]
            info['bones'] = len(a.data.bones)
            info['bone_names'] = [b.name for b in a.data.bones]
        info['actions'] = []
        for act in bpy.data.actions:
            fr = act.frame_range
            info['actions'].append({'name': act.name, 'f0': fr[0], 'f1': fr[1], 'users': act.users})
        if arms and bpy.data.actions:
            a = arms[0]
            act = (a.animation_data.action if a.animation_data and a.animation_data.action else None)
            if job.get('pick') and bpy.data.actions.get(job['pick']):
                act = bpy.data.actions.get(job['pick'])
                if not a.animation_data: a.animation_data_create()
                a.animation_data.action = act
            if act:
                f0, f1 = int(round(act.frame_range[0])), int(round(act.frame_range[1]))
                root = next((b for b in a.pose.bones if b.parent is None), a.pose.bones[0])
                def snap(f):
                    scn.frame_set(f)
                    return (a.matrix_world @ root.head).copy(), [pb.matrix_basis.to_quaternion() for pb in a.pose.bones], [ (a.matrix_world @ pb.head).copy() for pb in a.pose.bones]
                p0, q0, h0 = snap(f0); p1, q1, h1 = snap(f1)
                d = p1 - p0
                info['root_disp_m'] = [round(d.x, 3), round(d.y, 3), round(d.z, 3)]
                import math
                info['loop_err_deg'] = round(max(math.degrees(x.rotation_difference(y).angle) for x, y in zip(q0, q1)), 1)
                # height of the root above lowest bone at frame 0 (crouch/lying detection)
                info['root_h0_m'] = round(p0.z - min(h.z for h in h0), 3)
        if job.get('out') and arms:
            a = arms[0]
            # choose action: requested clip or the one on the armature
            acts = list(bpy.data.actions)
            pick = None
            if job.get('pick'):
                pick = bpy.data.actions.get(job['pick'])
            if pick is None and a.animation_data and a.animation_data.action:
                pick = a.animation_data.action
            if pick is None and acts:
                pick = max(acts, key=lambda x: x.frame_range[1] - x.frame_range[0])
            for o in meshes:
                bpy.data.objects.remove(o, do_unlink=True)
            for o in list(scn.objects):
                if o.type not in ('ARMATURE', 'EMPTY'):
                    bpy.data.objects.remove(o, do_unlink=True)
            for act in list(bpy.data.actions):
                if act != pick:
                    bpy.data.actions.remove(act)
            for img in list(bpy.data.images):
                bpy.data.images.remove(img)
            if pick:
                pick.name = job['clip']
                if not a.animation_data:
                    a.animation_data_create()
                a.animation_data.action = pick
                fr = pick.frame_range
                scn.frame_start, scn.frame_end = int(round(fr[0])), int(round(fr[1]))
                info['clip_frames'] = [fr[0], fr[1]]
                info['duration_s'] = (fr[1] - fr[0]) / info['fps']
            os.makedirs(os.path.dirname(job['out']), exist_ok=True)
            bpy.ops.export_scene.gltf(
                filepath=job['out'], export_format='GLB', export_animations=True,
                export_animation_mode='ACTIONS', export_materials='NONE',
                export_morph=False, export_skins=True, export_optimize_animation_size=True,
                export_frame_range=False, export_force_sampling=True, export_def_bones=False,
                export_yup=True)
            info['size_bytes'] = os.path.getsize(job['out'])
    except Exception as e:
        info['error'] = traceback.format_exc()
    results.append(info)
    json.dump(results, open(res_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

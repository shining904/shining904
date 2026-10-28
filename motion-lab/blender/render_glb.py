"""Render a GLB (e.g. a Meshy model from Magnific) as a transparent PNG sequence with Blender.

Runs headless through the `bpy` module (pip install bpy), Cycles on CPU:

    python3 render_glb.py --glb model.glb --out frames/ --frames 120 --size 1080x1080 \
        --preset turntable --samples 48

Presets (camera/object motion over the clip):
    turntable  object spins 360° once, camera fixed slightly above
    reveal     camera dollies in and orbits 60° while the object turns 90° (hero shot)
    float      object bobs and sways gently, camera orbits 25° (loop-friendly B-roll)
    cruise     long object (ship, submarine, train) glides past a low 3/4 camera, no floor;
               pass --bow=-x if the model's nose points to -X

The background is transparent (film_transparent) with a shadow-catcher floor, so the frames
drop straight onto any HyperFrames / p5 / canvas background. Encode with encode_alpha.sh.
"""
import argparse
import math
import os
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--frames", type=int, default=120)
ap.add_argument("--fps", type=int, default=30)
ap.add_argument("--size", default="1080x1080")
ap.add_argument("--preset", default="turntable", choices=["turntable", "reveal", "float", "cruise"])
ap.add_argument("--samples", type=int, default=48)
ap.add_argument("--still", type=int, help="render only this frame (look check)")
ap.add_argument("--key", default="1.0,0.92,0.82", help="key light colour r,g,b")
ap.add_argument("--rim", default="0.75,0.85,1.0", help="rim light colour r,g,b")
ap.add_argument("--bow", default="+x", choices=["+x", "-x"], help="cruise: which way the nose points")
ap.add_argument("--world", type=float, default=0.6, help="ambient world light strength")
a = ap.parse_args(argv)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
w, h = (int(v) for v in a.size.split("x"))

# --- model: import, centre, scale to ~2 units tall/wide, parent to a pivot ---------------
bpy.ops.import_scene.gltf(filepath=a.glb)
meshes = [o for o in sc.objects if o.type == "MESH"]
lo = Vector((1e9, 1e9, 1e9))
hi = Vector((-1e9, -1e9, -1e9))
for o in meshes:
    for c in o.bound_box:
        p = o.matrix_world @ Vector(c)
        lo = Vector(map(min, lo, p))
        hi = Vector(map(max, hi, p))
size = max(hi - lo)
pivot = bpy.data.objects.new("pivot", None)
sc.collection.objects.link(pivot)
for o in sc.objects:
    if o.parent is None and o is not pivot and o.type in {"MESH", "EMPTY"}:
        o.parent = pivot
s = 2.0 / size
pivot.scale = (s, s, s)
centre = (lo + hi) / 2
pivot.location = (-centre.x * s, -centre.y * s, -lo.z * s)  # sit on the floor at z=0
if a.preset == "cruise":  # floats mid-water: centre the model on the origin instead
    pivot.location = (-centre.x * s, -centre.y * s, -centre.z * s)
height = (hi.z - lo.z) * s
for o in meshes:
    for poly in o.data.polygons:
        poly.use_smooth = True

# --- floor that only catches shadows ------------------------------------------------------
if a.preset != "cruise":
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
    bpy.context.object.is_shadow_catcher = True

# --- lights: warm key, cool rim, soft fill; dim neutral world -----------------------------
def area(name, loc, energy, color, size_):
    d = bpy.data.lights.new(name, "AREA")
    d.energy, d.size = energy, size_
    d.color = tuple(float(c) for c in color.split(","))
    ob = bpy.data.objects.new(name, d)
    sc.collection.objects.link(ob)
    ob.location = loc
    ob.rotation_euler = (Vector((0, 0, height / 2)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return ob

area("key", (3.5, -3.0, 4.0), 900, a.key, 3.0)
area("rim", (-3.0, 3.5, 3.0), 700, a.rim, 2.0)
area("fill", (-4.0, -3.0, 1.5), 180, "1,1,1", 4.0)
world = bpy.data.worlds.new("w")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.05, 0.06, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = a.world
sc.world = world

# --- camera + motion preset ---------------------------------------------------------------
cam_data = bpy.data.cameras.new("cam")
cam_data.lens = 55
cam = bpy.data.objects.new("cam", cam_data)
sc.collection.objects.link(cam)
sc.camera = cam
target = bpy.data.objects.new("target", None)
sc.collection.objects.link(target)
target.location = (0, 0, height * 0.48)
trk = cam.constraints.new("TRACK_TO")
trk.target, trk.track_axis, trk.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"
rig = bpy.data.objects.new("rig", None)  # camera orbits by rotating this
sc.collection.objects.link(rig)
cam.parent = rig
aspect = w / h
dist = 6.2 if aspect <= 1 else 5.4

sc.frame_start, sc.frame_end = 1, a.frames
sc.render.fps = a.fps
F = a.frames


def key(ob, path, frame, value, interp="BEZIER"):
    # new keys take the preference's interpolation (avoids poking the 5.x layered-action API)
    bpy.context.preferences.edit.keyframe_new_interpolation_type = interp
    getattr(ob, path)[:] = value
    ob.keyframe_insert(path, frame=frame)


if a.preset == "turntable":
    cam.location = (0, -dist, height * 0.9)
    key(pivot, "rotation_euler", 1, (0, 0, 0), "LINEAR")
    key(pivot, "rotation_euler", F + 1, (0, 0, math.tau), "LINEAR")
elif a.preset == "reveal":
    key(cam, "location", 1, (0, -dist * 1.5, height * 0.4))
    key(cam, "location", F, (0, -dist * 0.95, height * 1.05))
    key(rig, "rotation_euler", 1, (0, 0, math.radians(-40)))
    key(rig, "rotation_euler", F, (0, 0, math.radians(20)))
    key(pivot, "rotation_euler", 1, (0, 0, 0))
    key(pivot, "rotation_euler", F, (0, 0, math.radians(90)))
elif a.preset == "cruise":
    target.location = (0, 0, 0)
    d = 1 if a.bow == "+x" else -1   # camera starts ahead of the bow and drifts aft
    key(cam, "location", 1, (d * 3.0, -1.9, -0.45), "LINEAR")
    key(cam, "location", F, (d * 0.9, -2.5, -0.1), "LINEAR")
    key(target, "location", 1, (d * 0.35, 0, 0), "LINEAR")
    key(target, "location", F, (d * -0.15, 0, 0), "LINEAR")
else:  # float
    cam.location = (0, -dist, height * 0.8)
    for f, z, r in ((1, 0.0, -0.08), (F // 2, 0.12, 0.08), (F, 0.0, -0.08)):
        key(pivot, "location", f, (pivot.location.x, pivot.location.y, -lo.z * s + z))
        key(pivot, "rotation_euler", f, (r * 0.3, r, r * 2))
    key(rig, "rotation_euler", 1, (0, 0, math.radians(-12)))
    key(rig, "rotation_euler", F, (0, 0, math.radians(12)))

# --- render settings ----------------------------------------------------------------------
r = sc.render
r.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = a.samples
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6
sc.cycles.use_adaptive_sampling = True
r.film_transparent = True
r.resolution_x, r.resolution_y = w, h
r.image_settings.file_format = "PNG"
r.image_settings.color_mode = "RGBA"
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "AgX - Medium High Contrast"
os.makedirs(a.out, exist_ok=True)
if a.still:
    sc.frame_set(a.still)
    r.filepath = os.path.join(a.out, f"still_{a.still:04d}.png")
    bpy.ops.render.render(write_still=True)
else:
    r.filepath = os.path.join(a.out, "f_")
    bpy.ops.render.render(animation=True)
print("done", a.out)

"""
Scute Swarm — Blender procedural model
Limpet / gecko / army-ant inspired SAR climber
"""
import bpy
import math
from mathutils import Vector

# ---------------------------------------------------------------------------
# Reset scene
# ---------------------------------------------------------------------------
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for block in (bpy.data.meshes, bpy.data.materials, bpy.data.collections):
    for b in list(block):
        block.remove(b)


def make_mat(name, color, roughness=0.45, metallic=0.05, transmission=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if "Transmission Weight" in bsdf.inputs:
        bsdf.inputs["Transmission Weight"].default_value = transmission
    elif "Transmission" in bsdf.inputs:
        bsdf.inputs["Transmission"].default_value = transmission
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def smooth(obj):
    for poly in obj.data.polygons:
        poly.use_smooth = True
    mod = obj.modifiers.new("Subsurf", "SUBSURF")
    mod.levels = 2
    mod.render_levels = 2


def apply_boolean(obj, cutter, operation="DIFFERENCE"):
    mod = obj.modifiers.new("Bool", "BOOLEAN")
    mod.operation = operation
    mod.object = cutter
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


# Materials
mat_shell = make_mat("ScuteShell", (0.22, 0.38, 0.32), roughness=0.55)
mat_soft = make_mat("SoftRim", (0.15, 0.22, 0.20), roughness=0.7)
mat_pad = make_mat("GripPad", (0.08, 0.08, 0.10), roughness=0.35)
mat_sensor = make_mat("SensorEye", (0.05, 0.55, 0.75), roughness=0.15, metallic=0.4)
mat_latch = make_mat("Latch", (0.55, 0.55, 0.52), roughness=0.3, metallic=0.85)
mat_led = make_mat("StatusLED", (0.9, 0.35, 0.05), roughness=0.2)
mat_flap = make_mat("CrawlFlap", (0.18, 0.28, 0.24), roughness=0.65)

collection = bpy.data.collections.new("Scute_Robot")
bpy.context.scene.collection.children.link(collection)


def link(obj):
    for c in obj.users_collection:
        c.objects.unlink(obj)
    collection.objects.link(obj)


# ---------------------------------------------------------------------------
# 1. Main shield / limpet shell (flattened dome)
# ---------------------------------------------------------------------------
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0, location=(0, 0, 0.15))
shell = bpy.context.active_object
shell.name = "Shell"
shell.scale = (1.35, 1.05, 0.42)
bpy.ops.object.transform_apply(scale=True)

# Flatten underside — cut bottom half-ish so it sits like a limpet
bpy.ops.mesh.primitive_cube_add(size=4, location=(0, 0, -1.7))
cutter = bpy.context.active_object
apply_boolean(shell, cutter, "DIFFERENCE")
shell.data.materials.append(mat_shell)
smooth(shell)
link(shell)

# ---------------------------------------------------------------------------
# 2. Soft rim bumper (torus-like ring under edge)
# ---------------------------------------------------------------------------
bpy.ops.mesh.primitive_torus_add(
    major_segments=48,
    minor_segments=16,
    major_radius=1.15,
    minor_radius=0.12,
    location=(0, 0, 0.06),
)
rim = bpy.context.active_object
rim.name = "SoftRim"
rim.scale = (1.12, 0.88, 0.7)
bpy.ops.object.transform_apply(scale=True)
rim.data.materials.append(mat_soft)
smooth(rim)
link(rim)

# ---------------------------------------------------------------------------
# 3. Grip pads (suction / gecko array on underside)
# ---------------------------------------------------------------------------
pad_positions = []
for i in range(3):
    for j in range(3):
        x = (i - 1) * 0.45
        y = (j - 1) * 0.35
        if abs(x) + abs(y) * 0.8 < 0.95:
            pad_positions.append((x, y))

# center cluster denser
for ang in range(0, 360, 45):
    r = 0.28
    pad_positions.append((math.cos(math.radians(ang)) * r, math.sin(math.radians(ang)) * r * 0.75))

pad_positions.append((0, 0))

for idx, (x, y) in enumerate(pad_positions):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16, radius=0.11, depth=0.04, location=(x, y, 0.02)
    )
    pad = bpy.context.active_object
    pad.name = f"GripPad_{idx:02d}"
    pad.data.materials.append(mat_pad)
    smooth(pad)
    link(pad)
    # small concave tip suggestion — second thinner disc
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16, radius=0.07, depth=0.015, location=(x, y, 0.005)
    )
    cup = bpy.context.active_object
    cup.name = f"SuctionCup_{idx:02d}"
    cup.data.materials.append(mat_pad)
    link(cup)

# ---------------------------------------------------------------------------
# 4. Crawl flaps around rim (gecko-toe / limpet fringe)
# ---------------------------------------------------------------------------
for i in range(10):
    ang = i * (2 * math.pi / 10)
    x = math.cos(ang) * 1.25
    y = math.sin(ang) * 0.95
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.05))
    flap = bpy.context.active_object
    flap.name = f"Flap_{i:02d}"
    flap.scale = (0.22, 0.08, 0.035)
    # point outward
    flap.rotation_euler = (0, 0, ang)
    # slight droop
    flap.rotation_euler[1] = math.radians(12)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    flap.data.materials.append(mat_flap)
    smooth(flap)
    link(flap)

# ---------------------------------------------------------------------------
# 5. Sensor "eye" dome on top-front
# ---------------------------------------------------------------------------
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.22, location=(0.55, 0, 0.38))
eye = bpy.context.active_object
eye.name = "SensorEye"
eye.scale = (1.1, 1.0, 0.7)
bpy.ops.object.transform_apply(scale=True)
eye.data.materials.append(mat_sensor)
smooth(eye)
link(eye)

# lens
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.1, location=(0.72, 0, 0.40))
lens = bpy.context.active_object
lens.name = "Lens"
lens.scale = (0.5, 1, 1)
bpy.ops.object.transform_apply(scale=True)
lens.data.materials.append(make_mat("LensGlass", (0.1, 0.7, 0.9), roughness=0.05, transmission=0.6))
smooth(lens)
link(lens)

# ---------------------------------------------------------------------------
# 6. Status LED
# ---------------------------------------------------------------------------
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(-0.55, 0, 0.42))
led = bpy.context.active_object
led.name = "StatusLED"
led.data.materials.append(mat_led)
smooth(led)
link(led)

# ---------------------------------------------------------------------------
# 7. Mechanical dorsal latch (army-ant bridge clip) — NOT magnets
# ---------------------------------------------------------------------------
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.52))
base = bpy.context.active_object
base.name = "LatchBase"
base.scale = (0.35, 0.22, 0.06)
bpy.ops.object.transform_apply(scale=True)
base.data.materials.append(mat_latch)
link(base)

# hook arm
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.28, 0, 0.62))
hook = bpy.context.active_object
hook.name = "LatchHook"
hook.scale = (0.18, 0.08, 0.05)
bpy.ops.object.transform_apply(scale=True)
hook.data.materials.append(mat_latch)
link(hook)

bpy.ops.mesh.primitive_cube_add(size=1, location=(0.38, 0, 0.55))
tip = bpy.context.active_object
tip.name = "LatchTip"
tip.scale = (0.06, 0.08, 0.12)
bpy.ops.object.transform_apply(scale=True)
tip.data.materials.append(mat_latch)
link(tip)

# ventral receptacle slot (underside rear) for chaining
bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.7, 0, 0.12))
slot = bpy.context.active_object
slot.name = "LatchReceptacle"
slot.scale = (0.2, 0.16, 0.08)
bpy.ops.object.transform_apply(scale=True)
slot.data.materials.append(mat_latch)
link(slot)

# ---------------------------------------------------------------------------
# 8. Tiny antenna / IR beacon receiver bumps
# ---------------------------------------------------------------------------
for side in (-1, 1):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=8, radius=0.025, depth=0.18, location=(0.2, side * 0.55, 0.35)
    )
    ant = bpy.context.active_object
    ant.name = f"Antenna_{side}"
    ant.rotation_euler = (math.radians(25 * side), math.radians(15), 0)
    ant.data.materials.append(mat_latch)
    link(ant)

# ---------------------------------------------------------------------------
# Ground reference plane (arena floor hint)
# ---------------------------------------------------------------------------
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "ArenaFloor"
floor.data.materials.append(make_mat("Floor", (0.35, 0.33, 0.30), roughness=0.9))
link(floor)

# Wall board for climb context
bpy.ops.mesh.primitive_cube_add(size=1, location=(-2.2, 0, 1.5))
wall = bpy.context.active_object
wall.name = "ClimbWall"
wall.scale = (0.08, 3, 1.5)
bpy.ops.object.transform_apply(scale=True)
wall.data.materials.append(make_mat("Wall", (0.75, 0.72, 0.68), roughness=0.85))
link(wall)

# ---------------------------------------------------------------------------
# Camera + light for nice default view
# ---------------------------------------------------------------------------
bpy.ops.object.camera_add(location=(3.8, -3.2, 2.4), rotation=(math.radians(65), 0, math.radians(50)))
cam = bpy.context.active_object
cam.name = "ScuteCam"
bpy.context.scene.camera = cam

bpy.ops.object.light_add(type="SUN", location=(2, -2, 5))
sun = bpy.context.active_object
sun.data.energy = 3.0

bpy.ops.object.light_add(type="AREA", location=(-1, 2, 3))
fill = bpy.context.active_object
fill.data.energy = 50
fill.data.size = 3

# ---------------------------------------------------------------------------
# Empty parent for easy transform
# ---------------------------------------------------------------------------
bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
root = bpy.context.active_object
root.name = "Scute_ROOT"
link(root)

robot_parts = [
    o
    for o in collection.objects
    if o.name
    not in ("ArenaFloor", "ClimbWall", "Scute_ROOT", "ScuteCam")
    and o.type == "MESH"
]
for o in robot_parts:
    o.parent = root

# Scale root to ~15 cm long (shell is ~2.7 units wide → scale so length ≈ 0.15 m if 1 BU = 1 m)
# Keep artistic scale: 1 Blender unit ≈ 10 cm → robot ~27 cm. Optional note in text.
root["design"] = "Scute Swarm v1"
root["inspiration"] = "limpet + gecko + army ant"
root["length_approx_cm"] = 27

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out_blend = r"d:\robots\scute_swarm.blend"
out_glb = r"d:\robots\scute_swarm.glb"
out_stl = r"d:\robots\scute_swarm.stl"

bpy.ops.wm.save_as_mainfile(filepath=out_blend)

# Export GLB (whole scene useful for preview)
bpy.ops.export_scene.gltf(filepath=out_glb, export_format="GLB")

# Export STL of robot only (no floor/wall) for 3D print experiments
bpy.ops.object.select_all(action="DESELECT")
for o in robot_parts:
    o.select_set(True)
bpy.context.view_layer.objects.active = robot_parts[0]
bpy.ops.export_mesh.stl(filepath=out_stl, use_selection=True)

print("Saved:", out_blend)
print("Saved:", out_glb)
print("Saved:", out_stl)
print("Parts:", len(robot_parts))

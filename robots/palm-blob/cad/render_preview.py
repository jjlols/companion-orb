"""Render the current v5 Wonder Sphere cage from exported STLs."""
from pathlib import Path
import math
import bpy

ROOT = Path(__file__).resolve().parent.parent
STL = ROOT / "stl"
OUT = ROOT / "preview_now.png"


def reset():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for cam in list(bpy.data.cameras):
        bpy.data.cameras.remove(cam)
    for light in list(bpy.data.lights):
        bpy.data.lights.remove(light)
    for mat in list(bpy.data.materials):
        bpy.data.materials.remove(mat)
    for mesh in list(bpy.data.meshes):
        bpy.data.meshes.remove(mesh)


def mat(name, color, roughness=0.35, metallic=0.15, transmission=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    key = "Transmission Weight" if "Transmission Weight" in bsdf.inputs else "Transmission"
    if key in bsdf.inputs:
        bsdf.inputs[key].default_value = transmission
    return m


def import_stl(name, material, loc=(0, 0, 0)):
    path = STL / name
    bpy.ops.wm.stl_import(filepath=str(path))
    obj = bpy.context.selected_objects[0]
    obj.location = loc
    obj.data.materials.append(material)
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


reset()

cage = mat("cage", (0.12, 0.42, 0.95), roughness=0.22, metallic=0.35)
inside = mat("inside", (0.18, 0.20, 0.24), roughness=0.45, metallic=0.05)
wheel = mat("wheel", (0.08, 0.08, 0.08), roughness=0.6)

import_stl("shell_bottom.stl", cage)
import_stl("shell_top.stl", cage)
ch = import_stl("chassis.stl", inside, loc=(0, 0, -19.2))

# simple stand-in wheels for the photo (not in STL)
for y in (-34.0, 34.0):
    bpy.ops.mesh.primitive_cylinder_add(radius=17.0, depth=7.0, location=(0, y, -11.0), vertices=48)
    w = bpy.context.active_object
    w.rotation_euler[0] = math.radians(90)
    w.data.materials.append(wheel)

# world / lights
world = bpy.data.worlds["World"]
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.93, 0.94, 0.96, 1)
bg.inputs[1].default_value = 1.2

bpy.ops.object.light_add(type="AREA", location=(40, -50, 70))
key = bpy.context.active_object
key.data.energy = 1200
key.data.size = 40
key.rotation_euler = (math.radians(50), 0, math.radians(20))

bpy.ops.object.light_add(type="AREA", location=(-50, 20, 30))
fill = bpy.context.active_object
fill.data.energy = 400
fill.data.size = 50

bpy.ops.object.camera_add(location=(130, -95, 55))
cam = bpy.context.active_object
cam.rotation_euler = (math.radians(72), 0, math.radians(54))
bpy.context.scene.camera = cam

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 32
scene.render.resolution_x = 1280
scene.render.resolution_y = 960
scene.render.filepath = str(OUT)
scene.render.film_transparent = False
bpy.ops.render.render(write_still=True)
print("RENDERED", OUT)

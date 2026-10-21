"""Render a preview of the Scute model."""
import bpy

bpy.ops.wm.open_mainfile(filepath=r"d:\robots\scute_swarm.blend")

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.filepath = r"d:\robots\scute_swarm_preview.png"
scene.render.image_settings.file_format = "PNG"

# Prefer Eevee next naming on 4.x if needed
try:
    scene.render.engine = "BLENDER_EEVEE_NEXT"
except Exception:
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 64

bpy.ops.render.render(write_still=True)
print("Rendered:", scene.render.filepath)

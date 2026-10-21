"""
Palm Blob v5 — Wonder Sphere cage (dense lat/long grid) + hamster-drive chassis.

Looks like the flying-orb toy: many meridians, many parallels, thick equator hoop,
polar hub. Printed as thick bars (not a thin solid wall) so it survives drops.

Shell (per half):
  - 100 mm OD, 3.2 mm radial bars, 2.8 mm bar width
  - 16 meridians + 5 latitude hoops per half + polar hub
  - proud equator hoop (~8 mm tall) like the toy
  - inner cylindrical wheel rails at y = ±34 for Ø34 wheels (r = 28)
  - lip + 4 magnet pairs at the seam
  - speaker grill in the bottom pole

Chassis is unchanged (still drops in free). Charge by lifting the top half.

Run:
  & "C:\\Program Files\\Blender Foundation\\Blender 4.1\\blender.exe" --background --python export_blender.py
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parent.parent
STL = ROOT / "stl"
STL.mkdir(parents=True, exist_ok=True)

# ---------------- ball envelope ----------------
OD = 100.0
WALL = 3.2  # bar thickness radially (durable FDM)
R_O = OD / 2
R_I = R_O - WALL  # 46.8
CLEAR = 0.4

RIB = 2.8          # bar width — dense Wonder Sphere grid, still printable
BAND_H = 8.0       # visible equator hoop (toy-like, not a fat belt)
BAND_INNER_R = 43.5
LAT_Z = (14.0, 23.0, 32.0, 40.0, 45.5)  # 5 parallels per half
CAP_Z = 46.5       # solid polar hub
# each plane makes two meridians → 8 angles = 16 meridians
LON_ANGLES = (0.0, 22.5, 45.0, 67.5, 90.0, 112.5, 135.0, 157.5)

MAGNET_D, MAGNET_H = 6.0, 2.0
BUTTON_D = 6.5

# ---------------- drive parts ----------------
N20_L, N20_W, N20_H = 26.5, 12.4, 10.4   # body (shaft adds 10 mm)
WHEEL_D, WHEEL_W = 34.0, 7.0
AXLE_Y = 34.0      # wheel centre; motor face sits 5 mm inboard (29), motor backs 5 mm apart
WHEEL_SETBACK = 5.0
TRACK_W = 10.0     # rail width in y (wheel is 7)
R_RAIL = 28.0      # inner radius of the cylindrical wheel track (about Y axis)
# magnets live in 2 thickened band bosses at ±X (r 41 → 50, |x| ≥ BOSS_X, |y| ≤ 10)
BOSS_X = 34.0
BOSS_R_IN = 41.0
MAGNET_POS = tuple((sx * 45.2, sy * 5.0) for sx in (-1, 1) for sy in (-1, 1))

BATTERY_L, BATTERY_W, BATTERY_H = 38.0, 26.0, 8.0   # 702535 + clearance
ESP_L, ESP_W = 24.5, 21.5
DRV_L, DRV_W = 22.0, 18.0
TP_L, TP_W = 27.0, 18.0
LED_RING_OD, LED_RING_ID = 50.0, 31.0
SPEAKER_D = 20.0
MIC_L, MIC_W = 16.0, 14.0

DECK_T = 2.6
DECK_X, DECK_Y = 32.0, 24.0
DECK_ROUND_R = 39.0                                # deck corners trimmed to this radius
AXLE_CHASSIS_Z = DECK_T + N20_H / 2 + 0.4          # 8.2
AXLE_SHELL_Z = -R_RAIL + WHEEL_D / 2               # -11
CHASSIS_ORIGIN_Z = AXLE_SHELL_Z - AXLE_CHASSIS_Z   # -19.2 : where chassis z=0 sits in the shell
SKID_X = 28.0
SHELF_Z = 14.9                                     # shelf plate centre (chassis coords)
RING_Z = SHELF_Z + 17.0                            # LED tray centre -> shell z ≈ +11.7 (above band)

# ---------------- wearable ring ----------------
FINGER_ID = 18.5
BAND_W = 8.0
BAND_T = 2.4
JEWEL_L, JEWEL_W, JEWEL_H = 28.0, 22.0, 14.0


# ======================= helpers =======================
def reset():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.objects, bpy.data.collections):
        for b in list(block):
            try:
                block.remove(b)
            except Exception:
                pass


def apply_boolean(obj, other, op="DIFFERENCE"):
    mod = obj.modifiers.new(name="bool", type="BOOLEAN")
    mod.operation = op
    mod.solver = "EXACT"
    mod.object = other
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(other, do_unlink=True)
    return obj


def union(obj, other):
    return apply_boolean(obj, other, "UNION")


def export(obj, name):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    path = STL / name
    bpy.ops.wm.stl_export(filepath=str(path), export_selected_objects=True, ascii_format=False)
    print("Exported", path)


def add_cube(loc, half, rot_z_deg=0.0):
    # size=2 -> unit half-extents, so scaling by `half` gives true half-extents
    bpy.ops.mesh.primitive_cube_add(size=2, location=loc)
    o = bpy.context.active_object
    o.scale = half
    if rot_z_deg:
        o.rotation_euler[2] = math.radians(rot_z_deg)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    return o


def add_cyl(radius, depth, loc, rot_x_deg=0.0):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=loc, vertices=96)
    o = bpy.context.active_object
    if rot_x_deg:
        o.rotation_euler[0] = math.radians(rot_x_deg)
        bpy.ops.object.transform_apply(rotation=True)
    return o


def add_sphere(radius, segs=96, rings=48):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, segments=segs, ring_count=rings, location=(0, 0, 0))
    return bpy.context.active_object


def half_cube(upper):
    """Big cube covering z>0 (upper) or z<0."""
    s = 1 if upper else -1
    return add_cube((0, 0, s * 60), (70, 70, 60))


def hemisphere(radius, upper):
    sph = add_sphere(radius)
    return apply_boolean(sph, half_cube(upper), "INTERSECT")


def clip_half(obj, upper):
    return apply_boolean(obj, half_cube(upper), "INTERSECT")


# ======================= cage pieces =======================
def cage_mask(upper):
    """Union of slabs: where the spherical shell is KEPT (Wonder Sphere grid)."""
    s = 1 if upper else -1
    m = add_cube((0, 0, 0), (70, 70, BAND_H / 2 + 0.6))
    for y in (-AXLE_Y, AXLE_Y):
        m = union(m, add_cube((0, y, 0), (70, TRACK_W / 2, 70)))
    for z in LAT_Z:
        m = union(m, add_cube((0, 0, s * z), (70, 70, RIB / 2)))
    for a in LON_ANGLES:
        m = union(m, add_cube((0, 0, 0), (70, RIB / 2, 70), rot_z_deg=a))
    m = union(m, add_cube((0, 0, s * (CAP_Z + 8)), (70, 70, 8)))
    return m


def cage_shell(upper):
    shell = hemisphere(R_O, upper)
    shell = apply_boolean(shell, hemisphere(R_I, upper), "DIFFERENCE")
    shell = apply_boolean(shell, cage_mask(upper), "INTERSECT")
    return shell


def equator_band(upper):
    """Proud hoop like the toy's equator ring, plus inner magnet bosses."""
    s = 1 if upper else -1
    z = s * BAND_H / 4
    band = add_cyl(R_O + 1.6, BAND_H / 2, (0, 0, z))
    band = apply_boolean(band, add_cyl(BAND_INNER_R, BAND_H / 2 + 2, (0, 0, z)), "DIFFERENCE")
    for sx in (-1, 1):
        boss = add_cube((sx * (BOSS_X + 10), 0, s * 3.0), (10, 10, 3.0))
        boss = apply_boolean(boss, add_cyl(BOSS_R_IN, 10, (0, 0, s * 3.0)), "DIFFERENCE")
        band = union(band, boss)
    # keep the hoop slightly proud — clip only the inner/outer extremes, not the proud rim
    band = apply_boolean(band, add_sphere(R_O + 1.7), "INTERSECT")
    return band


def wheel_rails(upper):
    """Two solid rails about the Y axis; inner surface is a cylinder r=R_RAIL."""
    rails = None
    for y in (-AXLE_Y, AXLE_Y):
        r = add_cyl(R_I + 1.5, TRACK_W, (0, y, 0), rot_x_deg=90)
        r = apply_boolean(r, add_cyl(R_RAIL, TRACK_W + 2, (0, y, 0), rot_x_deg=90), "DIFFERENCE")
        r = apply_boolean(r, add_sphere(R_O), "INTERSECT")
        r = clip_half(r, upper)
        rails = r if rails is None else union(rails, r)
    return rails


LIP_R_IN = BAND_INNER_R - 3.0   # 40
LIP_R_OUT = BAND_INNER_R - 0.4  # 42.6 (0.4 mm clearance inside the top band)


def lip_ring():
    """Bottom-shell lip: r 40 → 42.6 sticking up 3 mm above the seam, fused to the band by a
    flange (r 40 → 43.5, z -3 → 0). Gaps where the rails/wheels pass."""
    lip = add_cyl(LIP_R_OUT, 3.0, (0, 0, 1.5))
    lip = union(lip, add_cyl(BAND_INNER_R + 0.5, 3.0, (0, 0, -1.5)))
    lip = apply_boolean(lip, add_cyl(LIP_R_IN, 8.0, (0, 0, 0)), "DIFFERENCE")
    for y in (-AXLE_Y, AXLE_Y):                      # gaps for the rails / wheels
        lip = apply_boolean(lip, add_cube((0, y, 0), (70, TRACK_W / 2 + 1.5, 5)), "DIFFERENCE")
    for sx in (-1, 1):                               # gaps for the top half's magnet bosses
        lip = apply_boolean(lip, add_cube((sx * (BOSS_X - 0.5 + 20), 0, 1.5), (20, 11, 3)), "DIFFERENCE")
    return lip


def magnet_pockets(obj, upper):
    """4 pockets in the band bosses' seam faces; open at the seam."""
    s = 1 if upper else -1
    depth = MAGNET_H + 0.6
    for x, y in MAGNET_POS:
        obj = apply_boolean(
            obj, add_cyl(MAGNET_D / 2 + 0.15, depth + 1.0, (x, y, s * (depth - 1.0) / 2)), "DIFFERENCE"
        )
    return obj


# ======================= ball halves =======================
def make_shell_bottom():
    reset()
    shell = cage_shell(upper=False)
    shell = union(shell, equator_band(upper=False))
    shell = union(shell, wheel_rails(upper=False))
    shell = union(shell, lip_ring())
    shell.name = "shell_bottom"

    shell = magnet_pockets(shell, upper=False)

    # speaker grill: 8 holes on a Ø12 circle around the bottom pole
    for i in range(8):
        a = math.radians(i * 45 + 22.5)
        shell = apply_boolean(shell, add_cyl(1.1, 8, (6 * math.cos(a), 6 * math.sin(a), -R_I - 1.0)), "DIFFERENCE")

    export(shell, "shell_bottom.stl")


def make_shell_top():
    reset()
    shell = cage_shell(upper=True)
    shell = union(shell, equator_band(upper=True))
    shell = union(shell, wheel_rails(upper=True))
    shell.name = "shell_top"
    shell = magnet_pockets(shell, upper=True)
    export(shell, "shell_top.stl")


# ======================= chassis =======================
def make_chassis():
    reset()

    # ---- deck (corners rounded to r=39 so it drops through the lip opening r=40) ----
    body = add_cube((0, 0, DECK_T / 2), (DECK_X, DECK_Y, DECK_T / 2))
    body = apply_boolean(body, add_cyl(DECK_ROUND_R, DECK_T + 2, (0, 0, DECK_T / 2)), "INTERSECT")
    body.name = "chassis"

    # side walls (deck -> shelf) at y = ±23
    for y in (-DECK_Y + 1.0, DECK_Y - 1.0):
        body = union(body, add_cube((0, y, (DECK_T + SHELF_Z) / 2), (DECK_X - 4, 1.0, (SHELF_Z - DECK_T) / 2 + 0.4)))

    # ---- battery tray hanging UNDER the deck (open at the -X end; slide battery in) ----
    tray_h = BATTERY_H + 1.4
    body = union(body, add_cube((0, 0, -tray_h / 2 + 0.2), (BATTERY_L / 2 + 1.5, BATTERY_W / 2 + 1.5, tray_h / 2)))
    body = apply_boolean(
        body, add_cube((-1.5, 0, -BATTERY_H / 2 + 0.2), (BATTERY_L / 2 + 1.5, BATTERY_W / 2, BATTERY_H / 2)), "DIFFERENCE"
    )

    # ---- speaker pocket under the tray (speaker faces the pole grill) ----
    tray_bottom = -tray_h + 0.2
    body = union(body, add_cyl(SPEAKER_D / 2 + 1.2, 5.0, (0, 0, tray_bottom - 2.5 + 0.2)))
    body = apply_boolean(body, add_cyl(SPEAKER_D / 2 + 0.3, 4.6, (0, 0, tray_bottom - 2.5 - 0.5)), "DIFFERENCE")

    # ---- motor cradle: one box, both N20s back-to-back, shafts ±Y ----
    cradle_top = SHELF_Z - 0.7                       # fuses with the shelf plate
    motor_face = AXLE_Y - WHEEL_SETBACK               # |y| of the motor front faces (29)
    motor_back = motor_face - N20_L                   # |y| of the motor back faces (2.5)
    body = union(body, add_cube((0, 0, (DECK_T + cradle_top) / 2), (N20_W / 2 + 1.7, motor_face + 1.0, (cradle_top - DECK_T) / 2)))
    cav_half_z = N20_H / 2 + CLEAR / 2
    body = apply_boolean(body, add_cube((0, 0, DECK_T + 0.2 + cav_half_z), (N20_W / 2 + CLEAR / 2, AXLE_Y, cav_half_z)), "DIFFERENCE")
    # floor stop between the two motor backs (tabs/wires stay clear above it)
    body = union(body, add_cube((0, 0, DECK_T + 0.2 + 0.75), (N20_W / 2 + CLEAR / 2, motor_back, 0.75)))

    # ---- electronics shelf above the motors ----
    body = union(body, add_cube((0, 0, SHELF_Z), (30.0, 23.5, 0.9)))
    # ESP32-C3 pro mini corner posts (board 23.6 x 20.3; sits on 4 posts, hot-glue or tape)
    esp_c = (-17.5, 11.75)
    for dx in (-ESP_L / 2 + 1.2, ESP_L / 2 - 1.2):
        for dy in (-ESP_W / 2 + 1.2, ESP_W / 2 - 1.2):
            body = union(body, add_cube((esp_c[0] + dx, esp_c[1] + dy, SHELF_Z + 0.9 + 1.5), (1.2, 1.2, 1.5)))
    # DRV8833 + TP4056 raised pads (double-sided tape on top)
    body = union(body, add_cube((17.0, 13.0, SHELF_Z + 0.9 + 0.6), (DRV_L / 2, DRV_W / 2, 0.6)))
    body = union(body, add_cube((15.5, -14.0, SHELF_Z + 0.9 + 0.6), (TP_L / 2, TP_W / 2, 0.6)))
    # mic pad
    body = union(body, add_cube((-22.0, -17.5, SHELF_Z + 0.9 + 0.6), (MIC_L / 2, MIC_W / 2, 0.6)))
    # wire holes: motor leads up through the shelf centre, battery leads up beside the TP4056
    body = apply_boolean(body, add_cube((0, 0, SHELF_Z), (4.0, 6.0, 3.0)), "DIFFERENCE")
    body = apply_boolean(body, add_cube((-3.0, -14.0, SHELF_Z), (3.0, 4.0, 3.0)), "DIFFERENCE")
    body = apply_boolean(body, add_cube((-24.0, 0, DECK_T / 2), (3.0, 4.0, 3.0)), "DIFFERENCE")   # deck slot above tray end

    # ---- LED ring tray on 3 standoffs (ring sits above the equator band) ----
    tray = add_cyl(LED_RING_OD / 2 + 1.4, 2.2, (0, 0, RING_Z))
    tray = apply_boolean(tray, add_cyl(LED_RING_ID / 2 - 1.0, 2.6, (0, 0, RING_Z)), "DIFFERENCE")
    body = union(body, tray)
    for x, y in ((0.0, 16.0), (-16.0, -8.0), (16.0, -1.0)):
        body = union(body, add_cyl(2.3, RING_Z - SHELF_Z, (x, y, (RING_Z + SHELF_Z) / 2)))

    # ---- skids: rounded feet at ±X, 0.5 mm off the inner cage ----
    # closest approach of the ball to the shell is along the radial line, so put the ball
    # centre on a sphere of radius (R_I - gap - skid_r)
    skid_r = 3.5
    ball_c_shell = -math.sqrt((R_I - 0.5 - skid_r) ** 2 - SKID_X**2)
    ball_c = ball_c_shell - CHASSIS_ORIGIN_Z
    tip_chassis_z = ball_c - skid_r
    for x in (-SKID_X, SKID_X):
        body = union(body, add_cyl(skid_r, -ball_c, (x, 0, ball_c / 2)))
        bpy.ops.mesh.primitive_uv_sphere_add(radius=skid_r, segments=32, ring_count=16, location=(x, 0, ball_c))
        body = union(body, bpy.context.active_object)

    export(body, "chassis.stl")
    print(f"  chassis origin sits at shell z = {CHASSIS_ORIGIN_Z:.1f}; axle z = {AXLE_SHELL_Z:.1f}; "
          f"skid tip (shell) = {tip_chassis_z + CHASSIS_ORIGIN_Z:.1f}; LED tray (shell) = {RING_Z + CHASSIS_ORIGIN_Z:.1f}")


# ======================= small parts =======================
def make_small_parts():
    reset()
    hub = add_cyl(4.2, 5.0, (0, 0, 2.5))
    export(apply_boolean(hub, add_cyl(1.55, 5.5, (0, 0, 2.5)), "DIFFERENCE"), "wheel_spacer.stl")


def make_ring():
    reset()
    band = add_cyl(FINGER_ID / 2 + BAND_T, BAND_W, (0, 0, 0))
    export(apply_boolean(band, add_cyl(FINGER_ID / 2, BAND_W + 1, (0, 0, 0)), "DIFFERENCE"), "ring_band.stl")

    reset()
    box = add_cube((0, 0, JEWEL_H / 2), (JEWEL_L / 2, JEWEL_W / 2, JEWEL_H / 2))
    box = apply_boolean(box, add_cube((0, 0, JEWEL_H / 2 + 0.6), (JEWEL_L / 2 - 1.2, JEWEL_W / 2 - 1.2, JEWEL_H / 2)), "DIFFERENCE")
    box = apply_boolean(box, add_cube((0, JEWEL_W / 2, 5), (5, 3, 2.2)), "DIFFERENCE")
    export(union(box, add_cyl(4.0, 3.0, (0, 0, -1.5))), "ring_jewel_bottom.stl")

    reset()
    lid = add_cube((0, 0, 0.7), (JEWEL_L / 2 + 0.4, JEWEL_W / 2 + 0.4, 0.7))
    export(union(lid, add_cube((0, 0, -0.6), (JEWEL_L / 2 - 1.4, JEWEL_W / 2 - 1.4, 0.7))), "ring_jewel_lid.stl")


if __name__ == "__main__":
    print(f"Palm Blob v5 Wonder Sphere  OD={OD} wall={WALL} rib={RIB} meridians=16 rail_r={R_RAIL}")
    make_shell_bottom()
    make_shell_top()
    make_chassis()
    make_small_parts()
    make_ring()
    print("ALL DONE ->", STL)

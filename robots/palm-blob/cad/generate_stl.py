"""
Palm Blob v1 — watertight-ish printable STLs (mm).
Option D blob: 64 mm OD, hamster-drive chassis, no face.

  py -3 generate_stl.py
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from stl import mesh

OUT_DIR = Path(__file__).resolve().parent.parent / "stl"

OD = 64.0
WALL = 1.8
ID = OD - 2 * WALL
CLEAR = 0.35

MAGNET_D, MAGNET_H = 6.0, 2.0
LED_D = 8.0
BUTTON_D = 6.5
USB_W, USB_H = 9.2, 3.6
N20_L, N20_W, N20_H = 26.0, 12.2, 10.2
BATTERY_L, BATTERY_W, BATTERY_H = 40.0, 25.0, 8.5
WEIGHT_D, WEIGHT_H = 22.0, 4.0
XIAO_L, XIAO_W = 21.0, 17.5
DRV_L, DRV_W = 18.0, 16.0


def write_stl(path: Path, vertices: np.ndarray, faces: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    m = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            m.vectors[i][j] = vertices[f[j]]
    m.save(str(path))
    print(f"Wrote {path.name} ({len(faces)} tris)")


def combine(parts):
    vs, fs, off = [], [], 0
    for v, f in parts:
        vs.append(v)
        fs.append(f + off)
        off += len(v)
    return np.vstack(vs), np.vstack(fs)


def translate(v, dx=0, dy=0, dz=0):
    o = v.copy()
    o[:, 0] += dx
    o[:, 1] += dy
    o[:, 2] += dz
    return o


def box(x0, x1, y0, y1, z0, z1):
    v = np.array(
        [
            [x0, y0, z0],
            [x1, y0, z0],
            [x1, y1, z0],
            [x0, y1, z0],
            [x0, y0, z1],
            [x1, y0, z1],
            [x1, y1, z1],
            [x0, y1, z1],
        ],
        float,
    )
    f = np.array(
        [
            [0, 2, 1],
            [0, 3, 2],
            [4, 5, 6],
            [4, 6, 7],
            [0, 1, 5],
            [0, 5, 4],
            [1, 2, 6],
            [1, 6, 5],
            [2, 3, 7],
            [2, 7, 6],
            [3, 0, 4],
            [3, 4, 7],
        ],
        int,
    )
    return v, f


def cyl(r, z0, z1, n=32, solid=True):
    th = np.linspace(0, 2 * math.pi, n, endpoint=False)
    bot = np.c_[r * np.cos(th), r * np.sin(th), np.full(n, z0)]
    top = np.c_[r * np.cos(th), r * np.sin(th), np.full(n, z1)]
    if not solid:
        # open tube walls only
        v = np.vstack([bot, top])
        f = []
        for j in range(n):
            a, b = j, (j + 1) % n
            f += [[a, b, n + b], [a, n + b, n + a]]
        return v, np.array(f, int)
    cb = np.array([[0.0, 0.0, z0]])
    ct = np.array([[0.0, 0.0, z1]])
    v = np.vstack([bot, top, cb, ct])
    ib, it = 2 * n, 2 * n + 1
    f = []
    for j in range(n):
        a, b = j, (j + 1) % n
        f += [[a, b, n + b], [a, n + b, n + a], [ib, b, a], [it, n + a, n + b]]
    return v, np.array(f, int)


def hollow_hemisphere(r_o, r_i, upper=True, n_lat=24, n_lon=48):
    """Closed hollow hemisphere solid (outer + inner + equator ring)."""

    def rings(radius, flip_normal):
        # phi: 0 at +Z pole, pi at -Z
        if upper:
            phis = np.linspace(0.0, math.pi / 2, n_lat + 1)
        else:
            phis = np.linspace(math.pi / 2, math.pi, n_lat + 1)
        ths = np.linspace(0, 2 * math.pi, n_lon, endpoint=False)
        verts = []
        for phi in phis:
            for th in ths:
                verts.append(
                    [
                        radius * math.sin(phi) * math.cos(th),
                        radius * math.sin(phi) * math.sin(th),
                        radius * math.cos(phi),
                    ]
                )
        verts = np.array(verts, float)
        faces = []
        for i in range(n_lat):
            for j in range(n_lon):
                a = i * n_lon + j
                b = i * n_lon + (j + 1) % n_lon
                c = (i + 1) * n_lon + j
                d = (i + 1) * n_lon + (j + 1) % n_lon
                if flip_normal:
                    faces += [[a, c, b], [b, c, d]]
                else:
                    faces += [[a, b, c], [b, d, c]]
        return verts, np.array(faces, int), phis, ths

    vo, fo, phis, ths = rings(r_o, flip_normal=False)
    vi, fi, _, _ = rings(r_i, flip_normal=True)

    # equator join: outer rim <-> inner rim at z~0
    # outer rim is last ring for upper? For upper, last phi = pi/2; for lower, first phi = pi/2
    if upper:
        outer_rim = vo[n_lat * n_lon : (n_lat + 1) * n_lon]
        inner_rim = vi[n_lat * n_lon : (n_lat + 1) * n_lon]
    else:
        outer_rim = vo[0:n_lon]
        inner_rim = vi[0:n_lon]

    # build rim verts as new block
    rim_v = np.vstack([outer_rim, inner_rim])
    rim_f = []
    for j in range(n_lon):
        a, b = j, (j + 1) % n_lon
        c, d = n_lon + j, n_lon + ((j + 1) % n_lon)
        # outward-ish for lower/upper
        if upper:
            rim_f += [[a, b, d], [a, d, c]]
        else:
            rim_f += [[a, d, b], [a, c, d]]
    rim_f = np.array(rim_f, int)

    return combine([(vo, fo), (vi, fi), (rim_v, rim_f)])


def shell_bottom():
    r_o, r_i = OD / 2, ID / 2
    parts = [hollow_hemisphere(r_o, r_i, upper=False)]

    # rim lip up
    lip_o, _ = cyl(r_o, 0, 2.2, n=48, solid=False)
    # approximate lip as solid ring using boxy tube via outer-inner cylinders stacked
    # solid annulus wall
    th = np.linspace(0, 2 * math.pi, 48, endpoint=False)
    ro, ri = r_o, r_i - 1.2
    ob = np.c_[ro * np.cos(th), ro * np.sin(th), np.zeros(48)]
    ot = np.c_[ro * np.cos(th), ro * np.sin(th), np.full(48, 2.2)]
    ib = np.c_[ri * np.cos(th), ri * np.sin(th), np.zeros(48)]
    it = np.c_[ri * np.cos(th), ri * np.sin(th), np.full(48, 2.2)]
    v = np.vstack([ob, ot, ib, it])
    f = []
    n = 48
    for j in range(n):
        a, b = j, (j + 1) % n
        f += [[a, b, n + b], [a, n + b, n + a]]  # outer
        f += [[2 * n + a, 3 * n + a, 3 * n + b], [2 * n + a, 3 * n + b, 2 * n + b]]  # inner
        f += [[n + a, n + b, 3 * n + b], [n + a, 3 * n + b, 3 * n + a]]  # top
        f += [[a, 2 * n + b, b], [a, 2 * n + a, 2 * n + b]]  # bottom
    parts.append((v, np.array(f, int)))

    # pegs
    for ang in (0, 120, 240):
        pv, pf = cyl(1.4, 2.2, 4.4, n=16)
        rad = (r_o + r_i - 1.2) / 2
        parts.append((translate(pv, rad * math.cos(math.radians(ang)), rad * math.sin(math.radians(ang))), pf))

    # chassis posts
    for x in (-12.0, 12.0):
        pv, pf = cyl(2.0, -r_i + 6.0, -r_i + 10.0, n=16)
        parts.append((translate(pv, x, 0, 0), pf))

    # magnet holders (inward bosses)
    for ang in (45, 135, 225, 315):
        mv, mf = cyl(MAGNET_D / 2 + 0.8, 0.0, MAGNET_H + 0.6, n=20)
        rad = r_i - 2.0
        parts.append((translate(mv, rad * math.cos(math.radians(ang)), rad * math.sin(math.radians(ang))), mf))

    # USB notch marker bay (drill/cut after print if mesh doesn't boolean)
    parts.append((box(-USB_W / 2, USB_W / 2, -r_o, -r_i + 1.5, -6.0, -6.0 + USB_H), np.array([[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]], int)))

    # button boss
    bv, bf = cyl(BUTTON_D / 2 + 1.3, 0, 3.2, n=24)
    # rotate to +Y wall: build along Z then rotate via coordinate remap
    # simpler: place a horizontal cylinder as box tunnel guide on +Y
    parts.append((box(-BUTTON_D / 2 - 1, BUTTON_D / 2 + 1, r_i - 3.5, r_i - 0.2, -7.0, -3.0), np.array([[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]], int)))

    return combine(parts)


def shell_top():
    r_o, r_i = OD / 2, ID / 2
    parts = [hollow_hemisphere(r_o, r_i, upper=True)]

    # collar down
    th = np.linspace(0, 2 * math.pi, 48, endpoint=False)
    ro, ri = r_o - 0.35, r_i - 1.0
    ob = np.c_[ro * np.cos(th), ro * np.sin(th), np.full(48, -2.0)]
    ot = np.c_[ro * np.cos(th), ro * np.sin(th), np.zeros(48)]
    ib = np.c_[ri * np.cos(th), ri * np.sin(th), np.full(48, -2.0)]
    it = np.c_[ri * np.cos(th), ri * np.sin(th), np.zeros(48)]
    v = np.vstack([ob, ot, ib, it])
    f = []
    n = 48
    for j in range(n):
        a, b = j, (j + 1) % n
        f += [[a, b, n + b], [a, n + b, n + a]]
        f += [[2 * n + a, 3 * n + a, 3 * n + b], [2 * n + a, 3 * n + b, 2 * n + b]]
        f += [[n + a, n + b, 3 * n + b], [n + a, 3 * n + b, 3 * n + a]]
        f += [[a, 2 * n + b, b], [a, 2 * n + a, 2 * n + b]]
    parts.append((v, np.array(f, int)))

    # peg receivers (solid rings)
    for ang in (0, 120, 240):
        # outer tube solid approx
        pv, pf = cyl(1.55 + CLEAR + 0.8, -2.0, 0.1, n=16)
        hole_v, hole_f = cyl(1.55 + CLEAR, -2.0, 0.1, n=16)  # kept as guide post; drill if fused
        rad = (ro + ri) / 2
        parts.append((translate(pv, rad * math.cos(math.radians(ang)), rad * math.sin(math.radians(ang))), pf))

    for ang in (45, 135, 225, 315):
        mv, mf = cyl(MAGNET_D / 2 + 0.8, -MAGNET_H - 0.6, 0.0, n=20)
        rad = r_i - 2.0
        parts.append((translate(mv, rad * math.cos(math.radians(ang)), rad * math.sin(math.radians(ang))), mf))

    # LED socket ring near +Z
    sock_v, sock_f = cyl(LED_D / 2 + 1.2, r_i - 4.0, r_i - 2.2, n=24)
    parts.append((sock_v, sock_f))
    # diffuser ledge
    ledge_v, ledge_f = cyl(LED_D / 2 + 0.2, r_i - 3.2, r_i - 2.8, n=24)
    parts.append((ledge_v, ledge_f))

    return combine(parts)


def chassis():
    parts = []
    deck_t = 2.2
    parts.append(box(-18, 18, -14, 14, 0, deck_t))
    for y in (-14.0, 12.0):
        parts.append(box(-18, 18, y, y + 2, 0, 10))
    for x in (-18.0, 16.0):
        parts.append(box(x, x + 2, -14, 14, 0, 8))

    # battery keepers
    for x in (-BATTERY_L / 2 - 0.5, BATTERY_L / 2 - 1.0):
        parts.append(box(x, x + 1.5, -BATTERY_W / 2, BATTERY_W / 2, deck_t, deck_t + BATTERY_H))

    # weight cup
    parts.append(cyl(WEIGHT_D / 2 + 0.9, -WEIGHT_H - 1.4, 0.05, n=28))
    parts.append(cyl(WEIGHT_D / 2 + 0.15, -WEIGHT_H - 1.4, -WEIGHT_H + 0.5, n=24))

    # motor cradles
    for y in (-8.5, 8.5):
        parts.append(
            box(
                -N20_L / 2 - 0.4,
                N20_L / 2 + 0.4,
                y - N20_W / 2 - 0.3,
                y + N20_W / 2 + 0.3,
                deck_t,
                deck_t + N20_H + 0.5,
            )
        )
        parts.append(box(-N20_L / 2 - 1.6, -N20_L / 2 - 0.2, y - 4, y + 4, deck_t, deck_t + N20_H))
        parts.append(box(N20_L / 2 + 0.2, N20_L / 2 + 1.6, y - 4, y + 4, deck_t, deck_t + N20_H))

    # electronics shelf
    parts.append(box(-17.5, -17.5 + XIAO_L + 2, -XIAO_W / 2 - 1, XIAO_W / 2 + 1, deck_t + BATTERY_H + 0.5, deck_t + BATTERY_H + 1.7))
    for dx, dy in ((0, -XIAO_W / 2), (0, XIAO_W / 2 - 1.5), (XIAO_L - 1.5, -XIAO_W / 2), (XIAO_L - 1.5, XIAO_W / 2 - 1.5)):
        parts.append(box(-17 + dx, -17 + dx + 1.5, dy, dy + 1.5, deck_t + BATTERY_H + 0.5, deck_t + BATTERY_H + 4.0))

    parts.append(box(8, 8 + DRV_L, -DRV_W / 2, DRV_W / 2, deck_t + BATTERY_H + 0.5, deck_t + BATTERY_H + 1.6))

    for x in (-12.0, 12.0):
        hv, hf = cyl(2.3, -0.8, deck_t + 0.2, n=16, solid=False)
        # solid ring post hole using thin wall solid
        parts.append((translate(hv, x), hf))

    return combine(parts)


def led_window():
    return cyl(LED_D / 2 - 0.15, 0, 1.2, n=32)


def button_cap():
    return combine([cyl(BUTTON_D / 2 - 0.35, 0, 4.5, n=24), cyl(BUTTON_D / 2 + 1.0, 4.5, 5.5, n=24)])


def wheel_spacer():
    return cyl(4.0, 0, 5.0, n=24, solid=False)  # tube; OK as spacer blank


def bumper():
    # TPU ring
    th = np.linspace(0, 2 * math.pi, 64, endpoint=False)
    ro, ri = OD / 2 + 1.2, OD / 2 - 0.2
    n = 64
    ob = np.c_[ro * np.cos(th), ro * np.sin(th), np.full(n, -4)]
    ot = np.c_[ro * np.cos(th), ro * np.sin(th), np.full(n, 4)]
    ib = np.c_[ri * np.cos(th), ri * np.sin(th), np.full(n, -4)]
    it = np.c_[ri * np.cos(th), ri * np.sin(th), np.full(n, 4)]
    v = np.vstack([ob, ot, ib, it])
    f = []
    for j in range(n):
        a, b = j, (j + 1) % n
        f += [[a, b, n + b], [a, n + b, n + a]]
        f += [[2 * n + a, 3 * n + a, 3 * n + b], [2 * n + a, 3 * n + b, 2 * n + b]]
        f += [[n + a, n + b, 3 * n + b], [n + a, 3 * n + b, 3 * n + a]]
        f += [[a, 2 * n + b, b], [a, 2 * n + a, 2 * n + b]]
    return v, np.array(f, int)


def main():
    jobs = {
        "shell_bottom.stl": shell_bottom,
        "shell_top.stl": shell_top,
        "chassis.stl": chassis,
        "led_window.stl": led_window,
        "button_cap.stl": button_cap,
        "wheel_spacer.stl": wheel_spacer,
        "bumper_ring_tpu.stl": bumper,
    }
    for name, fn in jobs.items():
        v, f = fn()
        write_stl(OUT_DIR / name, v, f)
    print(f"Done -> {OUT_DIR}")
    print(f"OD={OD}mm ID~={ID:.1f}mm wall={WALL}mm")


if __name__ == "__main__":
    main()

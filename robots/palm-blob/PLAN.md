# Plan: glowing ball + follow-me ring

## What you are building

Two friends:

1. **The ball** — 100 mm glowing blob that rolls.
2. **The ring** — chunky “jewel” on your finger. When **you move**, it tells the ball “I’m awake.” The ball **rolls toward the ring**.

Mic + speaker get **pockets now**, wire them later.

---

## How “follow the ring” works (honest)

Bluetooth **cannot see direction** like a magnet. The ring shouts “here I am.” The ball hears **how loud** that shout is (RSSI).

When the ring’s IMU says **moving**:

1. Ball turns a little, rolls, checks: louder? keep going. Quieter? turn the other way.
2. It wiggles toward you on a desk (~1–2 m). It will **not** hunt you across a house like a dog.

If the ring is still (you’re sitting), the ball **stays** (sleep glow). Optional: tap the ring jewel USB-side later for “come here even if I’m still.”

---

## Glowing ball (v4 cage: light comes out through the gaps)

| Trick | Do this |
|--------|---------|
| **Open lattice shell** (wonder-sphere style) | No walls to shine through — the LED ring is simply visible between the ribs, from every side |
| **12-LED WS2812 ring inside** | Sits on 3 standoffs **above** the equator band, so it isn't hidden behind the solid band |
| **Any filament colour** | Dark PETG looks great: black cage, coloured glow inside |
| **Softer look** (optional) | Slip a ping-pong-ball-ish white diffuser over the LED ring, or print the ring tray in white |

Chassis has a **tray** for the LED ring so it sits above the boards and shines out.

---

## Build order (you’re traveling)

**Now (order parts):** ring electronics + LED ring + mic/speaker + solder  
**After the plane:** print v3 STLs, solder, firmware  

Don’t wait to assemble the ball until prints exist. Ring can be tested on a table: wiggle ring → phone/nRF app sees BLE, later the ball follows.

### Firmware later (not today)
- Ring: if shake/move → BLE advertise `BLOB-RING`
- Ball: scan RSSI → drive motors (gradient climb) + glow brighter as it gets closer

---

## 3D files (v4)

### Ball (`stl/`)
| File | Print |
|------|--------|
| `shell_bottom.stl` | **PETG**, 4 perimeters, tree supports — cage + band + lip + wheel rails + pole speaker grill |
| `shell_top.stl` | Same — cage + band + wheel rails, magnet pockets |
| `chassis.stl` | PLA/PETG — battery tray under, motor cradle, shelf, LED ring tray on standoffs, skids |
| `wheel_spacer.stl` | If needed |

Print once the halves, test-fit the chassis: wheels into the two rails, skids on the smooth centre ring. If the lip is tight in the band, sand the lip (0.4 mm designed clearance).

### Ring (`stl/`)
| File | Print |
|------|--------|
| `ring_band.stl` | Finger hole **18.5 mm**. Scale X/Y in slicer if tight/loose |
| `ring_jewel_bottom.stl` | Holds SuperMini + battery + MPU, USB notch |
| `ring_jewel_lid.stl` | **Translucent** so the ring can glow too (one WS2812 later) |

Glue jewel onto the band (the peg under the box).

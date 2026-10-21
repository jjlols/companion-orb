# Palm Blob v5 — Wonder Sphere cage

Dense **latitude / longitude cage** like the flying-orb toy. Same insides (Ø34 wheels, ESP32, battery).

## Why this shell

The earlier **solid thin ball** cracked easily. This one is a **bar cage**:

- **16 meridians** + **5 hoops** per half + polar hub  
- **3.2 mm** thick bars, **2.8 mm** wide — impact goes into the grid, not a paper-thin wall  
- **Proud equator hoop** like the toy  
- **Inner wheel rails** so the Ø34 tires still have a track to push on (hamster drive)  
- Light from the LED ring shines out through the holes  

Print **PETG** (or PLA+). Do not use brittle basic PLA if you can avoid it.

## Print

| File | Settings |
|------|----------|
| `shell_bottom.stl` / `shell_top.stl` | **PETG**, **4–5 perimeters**, 0.2 mm, 25–40% infill, tree supports, equator **flat on the bed** |
| `chassis.stl` | PLA/PETG, 40–60% infill |
| `wheel_spacer.stl` | optional |
| Ring STLs | same as before |

## Fit (unchanged)

- Wheels **Ø34** ride rails at y = ±34, inner radius 28 mm  
- Chassis drops in free — no screws to the cage  
- 4 magnet pairs in the equator bosses  
- Lift the top to charge  

## Assembly

1. Glue magnets so halves **attract**.  
2. Battery under chassis deck; motors in the cradle; wheels on.  
3. Drop chassis into the **bottom** cage — tires in the two rails.  
4. Snap the top cage on.

## Re-export

```powershell
& "C:\Program Files\Blender Foundation\Blender 4.1\blender.exe" --background --python "d:\robots\palm-blob\cad\export_blender.py"
```

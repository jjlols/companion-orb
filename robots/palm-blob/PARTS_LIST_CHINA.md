# Palm Blob — China buy list (AliExpress / Taobao)

Hand-sized **64 mm** rolling sphere desk pet (no face).  
Designed around the STLs in `stl/` and `cad/palm_blob.scad`.

**Currency:** CNY estimates for buying *in China* (domestic Taobao/1688) or AliExpress from China sellers.  
CAD prices are typically **2–4×** higher for the same parts.

---

## Buy this cart (one robot)

| # | Part | Exact-ish search keywords (中文 / EN) | Spec to match | Qty | Est. CNY | Est. USD |
|---|------|--------------------------------------|---------------|-----|----------|----------|
| 1 | Main board | `XIAO ESP32-C3` / `Seeed XIAO ESP32C3` | Seeed XIAO ESP32-C3 (USB-C) | 1 | 18–28 | $2.50–4 |
| 2 | Battery | `聚合物锂电池 3.7V 600mAh` / `LiPo 3.7V 600mAh` | **3.7 V, 500–800 mAh**, size ≤ **40×25×8 mm**, with JST-PH 2.0 if possible | 1 | 8–15 | $1–2 |
| 3 | Charger module | `TP4056 Type-C 带保护` / `TP4056 USB-C protection` | TP4056 **with battery protection**, USB-C | 1 | 2–4 | $0.30–0.60 |
| 4 | Motor driver | `DRV8833 模块` / `DRV8833 dual motor` | DRV8833 breakout (2-channel) | 1 | 3–6 | $0.40–0.90 |
| 5 | Gear motors | `N20减速电机 3V 150rpm` / `N20 geared motor 3V 150RPM` | **N20**, **3–6 V**, **~100–200 RPM**, **3 mm D-shaft** | **2** | 10–18 | $1.50–2.50 |
| 6 | Wheels | `N20电机轮子 14mm` / `N20 motor wheel 14mm` | **Ø12–15 mm**, width ~6 mm, fits 3 mm shaft | **2** | 4–8 | $0.60–1.20 |
| 7 | IMU | `MPU6050 模块` / `MPU-6050 GY-521` | GY-521 / MPU6050 3.3–5 V | 1 | 3–6 | $0.40–0.90 |
| 8 | RGB LED | `WS2812B 5050 灯珠` / `WS2812 5050 LED` | WS2812B (single LEDs or 2-pack) | **2** | 1–3 | $0.20–0.40 |
| 9 | Vibration motor | `硬币震动马达 10mm` / `coin vibration motor 10mm` | Ø10 mm coin vibe, 3 V | 1 | 2–4 | $0.30–0.60 |
| 10 | Buzzer (optional) | `无源蜂鸣器 5V 12mm` / `passive buzzer 5V` | Passive 5 V (or 3.3 V compatible) | 1 | 1–2 | $0.15–0.30 |
| 11 | Buttons | `轻触开关 6x6x5` / `tactile switch 6×6×5` | 6×6 mm, height 5–9 mm | **2** | 1–2 | $0.15–0.30 |
| 12 | Magnets | `钕磁铁 6x2` / `neodymium disc 6x2` | **Ø6 × 2 mm** N35+ | **8** (4 per hemisphere) | 3–6 | $0.40–0.90 |
| 13 | Weight | `配重铁片 20mm` / `steel disc 20mm` or fishing sinker | Steel disc ~**Ø20–22 mm**, 3–5 mm thick **or** M10 nuts | 1 set | 2–5 | $0.30–0.70 |
| 14 | Wire | `硅胶线 28AWG 混色` / `silicone wire 28AWG` | 28–30 AWG, mixed colors, 5 m | 1 | 5–10 | $0.70–1.40 |
| 15 | Header pins | `杜邦线 公对母 20cm` / `Dupont jumper M-F` | 40-pc DuPont set (for prototyping) | 1 | 3–6 | $0.40–0.90 |
| 16 | Heat shrink | `热缩管 套装` / `heat shrink assortment` | Small kit | 1 | 3–6 | $0.40–0.90 |
| 17 | Screws (optional) | `KM螺丝 M2x6` / `M2x6 screws` | M2×4–8 mm + nuts | 10 | 2–4 | $0.30–0.60 |
| 18 | Velcro / tape | `3M双面胶 强力` / `3M double sided tape` | For battery + boards | 1 | 3–8 | $0.40–1.10 |

### Optional (nice, not required for v1)

| Part | Search | Qty | Est. CNY |
|------|--------|-----|----------|
| Soft bumper filament | `TPU 95A 白色` (print `bumper_ring_tpu.stl`) | 1 spool share | 40–70 (whole spool) |
| Translucent filament | `透明PETG` or clear PLA for `led_window.stl` | scraps OK | — |
| Second battery | same as #2 | 1 | 8–15 |
| USB-C pigtail | `Type-C 母座 带线` if you want a panel port | 1 | 2–5 |

---

## Cart totals (1 robot)

| | CNY | USD (approx) |
|--|-----|--------------|
| **Electronics + hardware only** | **~70–130 ¥** | **~$10–18** |
| **+ magnets/wire/tape kit buffer** | **~90–160 ¥** | **~$13–22** |
| **Buy spares (extra motor, LED, vibe)** | **~110–190 ¥** | **~$15–27** |

Filament for the shell (PLA, ~30–40 g): **~3–6 ¥** if you already have a spool.

---

## Double-check notes (read before you click buy)

1. **XIAO ESP32-C3** — confirm it is the **Seeed XIAO** form factor (~21×17.5 mm), not a random “ESP32-C3 mini” of different size (chassis is sized for XIAO).
2. **Motors** — get **two identical** N20s, same RPM. Prefer **3 V–6 V**. Avoid 1000+ RPM (too spinny, poor torque).
3. **Wheels** — must fit **3 mm D-shaft**. If only round-hole wheels, also buy / print `wheel_spacer.stl` and use set-screw hubs.
4. **Battery size** — must fit **40×25×8.5 mm** tray. Measure the listing. Include a **protected** pack or use TP4056 **with protection**.
5. **TP4056** — buy the board that says **过充过放保护 / with protection**. Bare TP4056 alone is not enough for a LiPo.
6. **DRV8833** — 3.3 V logic OK with XIAO. Don’t buy L298N (too big/hot).
7. **Magnets 6×2** — buy **8** so top + bottom shells snap. Glue with CA; **match polarity** (attract across the seam).
8. **No face parts** — you do **not** need an OLED for Option D.

---

## What each part plugs into (sanity map)

```
LiPo --> TP4056 --> 3.3/5V rail --> XIAO ESP32-C3
                              |-> DRV8833 --> 2x N20 + wheels
                              |-> WS2812 LED(s)
                              |-> vibe motor (via MOSFET/NPN or GPIO + transistor)
                              |-> button(s)
                              |-> MPU6050 (I2C: SDA/SCL)
```

BLE “say hi to other blobs” needs **no extra radio parts**.

---

## Print vs buy

| Print (`stl/`) | Buy |
|----------------|-----|
| `shell_bottom.stl` | all electronics above |
| `shell_top.stl` | magnets, weight |
| `chassis.stl` | wheels, motors |
| `led_window.stl` | — |
| `button_cap.stl` | switches |
| `wheel_spacer.stl` | only if needed |
| `bumper_ring_tpu.stl` | optional TPU |

---

## Suggested AliExpress / Taobao order strategy

1. One cart: items **1–13** + wire kit (**14–16**).  
2. Choose sellers with **≥4.8** and recent motor/board sales.  
3. If shipping to Canada later: still order this China list; expect **+shipping**. Domestic China pickup/shipping is cheapest.

**Ready to buy now:** yes — this list matches the 64 mm design envelopes in the CAD.

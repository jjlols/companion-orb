# Full parts list — ball + follow ring + glow + future audio

You already own the **drive kit**. This list is **everything to finish v3**, including extras to buy now.

Prices ≈ China / Taobao. Qty is for **1 ball + 1 ring**.

---

## A. You should already have (don’t rebuy unless making a second ball)

| Qty | Part | Notes |
|-----|------|--------|
| 1 | ESP32C3-Pro mini (pins soldered) | Ball brain |
| 2 | N20 motor, 10 mm shaft, no rack | |
| 2 | Ø34 mm N20 wheels | |
| 1 | DRV8833 board, pins soldered | |
| 1 | TP4056 Type-C 充电+保护 | Pads, not pins — need solder |
| 1 | 702535 3.7V 600mAh LiPo | |
| 1 | MPU6050 直针向上 | Ball tilt |
| 5 | WS2812B 4-leg beads | Spare / ring jewel LED |
| 5 | 1027 vibe motor | Use 1 |
| 8+ | Magnets Ø6×2 | |
| 1+ | Button 6×6×5 | |
| 1 | Soldering iron | Buy **焊锡丝** |

---

## B. Buy now — glowing ball

| Qty | Part | Search | Why |
|-----|------|--------|-----|
| 1 | **WS2812 12灯圆环** ~50 mm | `WS2812 12位 灯环 50mm` | Whole-ball glow |
| 1 | **焊锡丝 0.8mm 带松香** | `焊锡丝 0.8mm` | You have no solder |
| 1 | Ø20×3 iron disc (if missing) | `铁圆片 20mm 3mm` | Balance / roll |
| 1 | White or **透光 PLA** (print shop) | Tell shop: natural/white/translucent, **not black** | Lantern shell |

---

## C. Buy now — follow-me ring

| Qty | Part | Search | Spec |
|-----|------|--------|------|
| 1 | **ESP32-C3 SuperMini** | `ESP32-C3 SuperMini` | Jewel brain + BLE. Pins **optional**; no-pin or cut short fits better |
| 1 | **MPU6050 直针向上** | same as ball | Detects *you moved* |
| 1 | Tiny LiPo **3.7V 80–150mAh** | `聚合物电池 3.7V 100mAh` | Must fit ~**25×15×6 mm** or smaller |
| 1 | Mini **TP4056 Type-C 带保护** | same as ball, or charge via SuperMini USB only | If SuperMini USB is in the notch, you can skip extra TP4056 |
| 1 | 1× WS2812 bead | you have extras | Optional ring glow |

Ring is **chunky on purpose**. A skinny fashion ring cannot hold a battery + ESP32.

---

## D. Buy now — future mic + speaker (pockets already in chassis)

| Qty | Part | Search | Notes |
|-----|------|--------|------|
| 1 | **MAX98357 I2S 功放** | `MAX98357 模块` | Easy with ESP32 |
| 1 | Speaker **8Ω 1W Ø20 mm** | `20mm 8欧 喇叭 1W` | Faces bottom grill |
| 1 | Mic **INMP441** (I2S) **or** `MAX9814` | `INMP441` / `MAX9814 模块` | INMP441 = cleaner; MAX9814 = analog, easier |

Wire these **after** follow + glow work.

---

## E. Nice extras

| Qty | Part | Search |
|-----|------|--------|
| 1 | TTP223 touch | Pet the ball |
| 1 | BH1750 light | Night lantern |
| 1 | Heat shrink (if missing) | `热缩管` |
| 1 | 杜邦线 公对母 | Prototyping |

---

## F. Do **not** buy

- 3W power LEDs  
- Extra 12V motors  
- SMD-only buzzers if you won’t solder tiny pads  
- GPS / camera  

---

## Money ballpark (new stuff only)

| Bundle | CNY |
|--------|-----|
| Solder + 12-LED ring | ~8–20 |
| Ring (SuperMini + tiny LiPo + MPU) | ~25–45 |
| Mic + speaker + MAX98357 | ~15–30 |
| **New cart total** | **~50–95 ¥** |

---

## What plugs into what (later)

**Ball:** LiPo → TP4056 → ESP32-Pro + DRV8833 + LED ring + (later) MAX98357 + mic  
**Ring:** tiny LiPo → SuperMini (USB charge) + MPU6050  

Follow = **BLE only**. No extra radio parts.

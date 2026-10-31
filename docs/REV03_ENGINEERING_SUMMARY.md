# ABK-20 Revision 0.3: Engineering & Architecture Summary

This document records all architectural decisions, circuit modifications, PCB routing strategies, and fabrication details discussed and implemented during the transition from **Revision 0.2** to **Revision 0.3**.

---

## 1. Version Baselines & Git Workflow

### Revision 0.2 (Baseline)
* **Hardware Status**: Flipped backside audio jacks (`Jack1`, `Jack2`), hand-etched, populated, soldered, and verified working.
* **Trace Width Baseline**: All 484 trace segments unified to **$0.40\text{ mm}$** for reliable DIY chemical etching.
* **Git Milestone**: Staged and committed on `main`, tagged with annotated tag [`rev-0.2`](file:///home/dusjagr/Documents/8bit_Mixtape/ABK-20).
* **Branch**: Created and checked out dedicated branch **`rev-0.3`** for all upcoming iterations.

---

## 2. Star Grounding & Audio Isolation (`GNDA`)

### The Problem (NeoPixel Common-Impedance Coupling)
* In Rev 0.2, the 20× NeoPixels switch at an internal $\approx 1.2\text{ kHz}$ PWM frequency, drawing heavy return pulses through the single shared ground copper plane back to the USB-C port.
* Because the headphone jack (`Jack2`) and volume pot (`POT3-Vol1`) were tapped along that shared copper, this switching current caused an audible high-pitched AC buzz in headphones, even with volume set to zero.

### The Rev 0.3 Solution: Two Ground Nets & Net-Tie (`NT1`)
* Divided ground into two distinct electrical domains:
  1. **`GND` (Digital & Power Ground)**: For ATtiny85 MCU, 20× NeoPixels, 7805 regulator, USB-C shield, and bulk capacitors.
  2. **`GNDA` (Analog Audio Ground)**: Isolated exclusively for sensitive audio circuitry.
* **Net-Tie (`NT1`)**:
  - Symbol: `Device:NetTie_2` (Pin 1 = `GND`, Pin 2 = `GNDA`).
  - Footprint: `NetTie:NetTie-2_SMD_Pad2.0mm`.
  - **Physical Location**: Placed directly at $(X=122.10\text{ mm}, Y=32.84\text{ mm})$ right next to the USB-C ground entry (`J5`). Anchoring `NT1` at the power source ensures the cleanest, lowest-impedance reference before digital return currents enter the plane.

### Components Assigned to `GNDA`
| Component | Pin | Function |
| :--- | :---: | :--- |
| **`Jack2`** (PJ-317) | Pin 1 | Headphone / Audio Out Sleeve Ground |
| **`POT3-Vol1`** | Pin 3 | Volume Thumbwheel Potentiometer Ground |
| **`C3`** | Pin 2 | PWM Audio Low-Pass Filter Ground ($100\text{nF}$) |
| **`U2`** (PAM8002) | Pins 1 & 7 | Audio Power Amplifier Ground & Shutdown |
| **`C6`** | Pin 2 | PAM8002 Pin 2 DC Reference Bypass ($1\,\mu\text{F}$) |
| **`C9`** | Pin 2 | PAM8002 Local High-Frequency Decoupling ($100\text{nF}$) |
| **`NT1`** | Pin 2 | Star Point Bridge to Main Ground |

### Routing Topology & Layer Transition
* **Zero Closed Loops (Tree Topology)**: `GNDA` radiates as open branches without looping back, preventing inductive loop antenna pickup from the NeoPixel matrix.
* **Component-Pin-as-Via Trick**:
  - `Jack2` (Pad 1) is a through-hole pad with copper rings on both `F.Cu` and `B.Cu`.
  - `GNDA` connects on `B.Cu` from `NT1` across the top to `Jack2` Pad 1.
  - The through-hole pin of `Jack2` solders on **both sides**, serving as the vertical layer transition to **`F.Cu` (Top Copper)**.
  - On `F.Cu`, `GNDA` runs straight South along the empty right margin, avoiding congested horizontal bus lines on `B.Cu`, and drops down into `POT3-Vol1` and `C3`.
* **DRC Result**: **0 unconnected items, 0 electrical shorts, 0 clearance errors**.

---

## 3. Power Decoupling Architecture: C7, C8, and C9

| Capacitor | Value | Ground Net | Physical Location | Design Role |
| :--- | :---: | :---: | :--- | :--- |
| **`C8`** | $100\text{nF}$ | **`GND`** | Directly touching ATtiny Pin 8 (`VCC`) & Pin 4 (`GND`) | Decouples high-speed 16 MHz clock & internal 64 MHz PLL. |
| **`C9`** | $100\text{nF}$ | **`GNDA`** | Directly bridging PAM8002 Pin 6 (`VCC`) & Pin 7 (`GNDA`) | Kills local high-frequency switching noise at the audio amp. |
| **`C7`** | $10\text{–}22\,\mu\text{F}$ *(was 220µF)* | **`GND`** | Near PAM8002 ($X=134.50, Y=44.78$) | Buffers heavy speaker bass transients locally without dumping ripple into `GNDA`. |

### The C7 Size & Value Rationalization:
* Old schematics listed $220\,\mu\text{F}$ (an artifact from single-ended LM386 designs).
* The modern PAM8002 is a BTL (Bridge-Tied Load) Class-AB amplifier driving an 8Ω speaker between `OUT+` and `OUT-` (current does not flow into ground).
* The PAM8002 datasheet specifies **$10\,\mu\text{F}$ to $22\,\mu\text{F}$**.
* A standard **$10\,\mu\text{F}$ or $22\,\mu\text{F}$ 1206/1210 MLCC ceramic capacitor** is flat, reliable, and provides superior low-ESR performance compared to bulky electrolytic cans.

---

## 4. Audio Amplifier Comparison: PAM8002 vs. PAM8302

| Feature | **PAM8002** (Selected for ABK-20) | **PAM8302** |
| :--- | :--- | :--- |
| **Class** | **Class-AB** (Linear Analog) | **Class-D** (Switching / Filterless PWM) |
| **RF / EMI** | **Zero switching noise**; silent on DIY boards | Radiates $250\text{ kHz}$ switching harmonics into ADC wipers & audio lines |
| **Shutdown** | Pin 1 = High $\to$ **Shutdown** (Low = ON) | Pin 1 = Low $\to$ **Shutdown** (Active Low — Inverted) |
| **Quiescent** | $\approx 4\text{ mA}$ | $\approx 4\text{ mA}$ |
| **Conclusion** | Ideal for lo-fi 8-bit synths; clean, simple, robust. | High EMI risk on 2-layer DIY-etched boards without solid inner planes. |

---

## 5. Highly KS01 Bi-Directional LED Circuit (`SW2`)

### The Hardware Reality
* `SW2` is an illuminated push button with two isolated systems:
  1. **Tactile Switch (`SW2A`)**: Pins 1 & 2 (Pulls `PB3` resistor ladder down to $\approx 1.0\text{V}$ on press).
  2. **Bi-directional LED (`SW2B`)**: Pins A & K (Two anti-parallel LEDs inside one package).

### Why Pure Discrete Hardware Press + Microcontroller Control Don't Mix Directly
* Tying the LED directly to switch Pin 1 to turn on in hardware would bleed $+5\text{V}$ through the LED into `R16` ($6.8\text{k}\Omega$) when released.
* This would corrupt the analog voltage divider on `PB3`, causing the microcontroller to misread the SPDT toggle switch and navigation states.
* Avoiding this in hardware would require adding extra isolation transistors or diodes to the PCB.

### The Selected Solution: Driven Between PB1 and PB0
The LED is wired in series with current-limiting resistor **`R19` ($1\text{k}\Omega$)** directly across two ATtiny pins:
```
  ATtiny PB1 (Audio PWM) ────[ R19 1kΩ ]──── (Pin A)
                                                │
                                             [ SW2B ]  (Bi-directional LED)
                                                │
  ATtiny PB0 (NeoPixel)  ──────────────────── (Pin K)
```

### Full 3-Color State Truth Table:
| Desired Color | `PB1` (Pin 6) | `PB0` (Pin 5) | Physical Current Flow | Application Meaning |
| :---: | :---: | :---: | :---: | :--- |
| **GREEN** | **HIGH** ($5\text{V}$) | **LOW** ($0\text{V}$) | `PB1` $\to$ `PB0` | Normal Mode, Low Octave, or **Instant Green on Button Press** |
| **RED** | **LOW** ($0\text{V}$) | **HIGH** ($5\text{V}$) | `PB0` $\to$ `PB1` | Accent Mode, High Octave, or Tempo Pulse |
| **AMBER** (Yellow) | **Toggle 50/50** | **Toggle 50/50** | Alternates at $>100\text{ Hz}$ | AudioBoot Sketch Loading / Menu Selection Mode |
| **OFF** | **LOW** ($0\text{V}$) | **LOW** ($0\text{V}$) | No current | Dark / Standby |

> [!TIP]
> **"Firmware-Instant" Tactile Feedback**: At $16\text{ MHz}$, the ATtiny85 reads `PB3` and sets `PB1=HIGH, PB0=LOW` in **under $10\,\mu\text{s}$**. Human touch cannot perceive delays below $\approx 10\text{ ms}$, so the button flash feels 100% mechanical and instantaneous without adding extra discrete components!

---

## 6. Solder Paste Stencil (`ABK-20_stenchill.kicad_pcb`) & Board Outline Grouping

1. **Stencil Board Created**:
   - Dedicated PCB file for solder paste stencil fabrication: [`hardware/ABK-20_stenchill.kicad_pcb`](file:///home/dusjagr/Documents/8bit_Mixtape/ABK-20/hardware/ABK-20_stenchill.kicad_pcb).
   - Contains all surface-mount component paste openings.
2. **Edge.Cuts Boundary Transfer**:
   - Transferred the exact $75 \times 80\text{ mm}$ rounded-corner board outline (4 lines + 4 corner arcs) from the main PCB into `ABK-20_stenchill.kicad_pcb`.
3. **One-Click Outline Grouping**:
   - Grouped the 8 separate boundary drawings into a single KiCad named group: **`"Edge.Cuts"`** in both boards.
   - Clicking any edge or corner now selects the entire perimeter at once for moving, alignment, or locking.

---

## 7. DIY Etching & DFM Verification Checklist

* [x] **Annular Rings**: All 55 through-hole pads verified with $\ge 0.45\text{–}0.50\text{ mm}$ copper rim around drill holes for easy hand-drilling without pad tear-out.
* [x] **Zone Fill Clearances**: Minimum clearance of $\ge 0.40\text{ mm}$ maintained between `GNDA` traces and surrounding digital `GND` copper flood to prevent bridging during home chemical etching.
* [x] **No Closed Ground Loops**: Single-branch tree topology prevents high-frequency inductive hum.
* [x] **Trace Widths**: Unified $0.40\text{ mm}$ minimum baseline across all routed copper.

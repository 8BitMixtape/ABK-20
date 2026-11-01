---
name: PCB DIY Etch & Photolithography Mask Pipeline
description: Automated workflow for generating 1:1 scale double-sided DIY photolithography and chemical etching masks (A4 envelope pouch) directly from KiCad PCB layouts using kicad-cli, vector SVG templating, and Inkscape CLI.
---

# PCB DIY Etch & Photolithography Mask Pipeline

This skill provides an automated, mathematically registered pipeline for creating production-ready, double-sided DIY PCB etching and photolithography masks directly from any KiCad PCB layout (`.kicad_pcb`).

---

## 🎯 The Core Problem & The Envelope Solution

When making double-sided PCBs at home using UV dry-film / negative resist or positive photoresist (Positiv 20):

1. **Direct Emulsion Contact (Zero Undercut)**:
   The printed ink side of the transparency film must physically contact the photoresist on the copper clad. If the light has to pass through the thickness of the transparency film carrier ($\sim 100\ \mu\text{m}$), UV light diffracts laterally, causing track thinning, blurred edges, and bridged fine pads.
2. **Symmetrical Envelope Folding**:
   By printing both the **Top Layer** (`F.Cu`) and **Bottom Layer** (`B.Cu`) on a single A4 landscape transparency sheet positioned symmetrically around the center fold line ($X = 148.5\text{ mm}$):
   * **Left Board (`F.Cu`)**: Placed **mirrored**. When folded over like a greeting card onto the top of the double-sided copper board, the horizontal flip restores `F.Cu` to its **correct normal orientation**, and the ink faces **directly down** onto the top photoresist.
   * **Right Board (`B.Cu`)**: Placed **direct / unmirrored**. The copper clad board sits directly on top of it, with the bottom photoresist directly touching the ink facing **up**.
   * **Perfect Registration**: Folding the sheet along the dashed crease aligns every pad, via, and mounting hole between top and bottom within $\pm 0.05\text{ mm}$.

```
  A4 Landscape Sheet (297 x 210 mm)
  ┌─────────────────────────┬─────────────────────────┐
  │                         │                         │
  │     TOP LAYER (F.Cu)    │   BOTTOM LAYER (B.Cu)   │
  │        [MIRRORED]       │        [DIRECT]         │
  │     Center: X = 75.0    │    Center: X = 222.0    │
  │                         │                         │
  │         ┌─────┐         │         ┌─────┐         │
  │      ╂──│ PCB │──╂      │      ╂──│ PCB │──╂      │
  │         └─────┘         │         └─────┘         │
  │                         │                         │
  │                         │                         │
  │                         ┆ Center Fold Line        │
  │                     <--- 50mm Scale Bar --->      │
  └─────────────────────────┴─────────────────────────┘
                            X = 148.5 mm
```

---

## 🚀 Quick Execution

Run the automated script from the repository root:

```bash
# Standard run for ABK-20 PCB:
python3 .agents/skills/pcb-diy-mask/scripts/generate_mask.py \
  --pcb hardware/ABK-20.kicad_pcb \
  --out-dir production/MASK \
  --board-name "ABK-20 SYNTHESIZER" \
  --rev "REV 0.3" \
  --name "ABK-20-DIY-etch"
```

> [!NOTE]
> To prevent overwriting manually illustrated Inkscape masks (such as `MASK_rev03_ABK-20-DIY-etch.svg` or `MASK_rev02_ABK-20-DIY-etch.svg` which contain custom 8-bit logos and typography), pass a distinct name using `--name` (e.g. `--name MASK_rev03_auto_envelope`).

### Generated Output Files
All files are saved to `production/MASK/`:
* **`<name>.pdf`** (e.g. `ABK-20-DIY-etch.pdf`): Complete 1-page A4 landscape vector PDF generated via Inkscape Cairo backend.
* **`<name>.svg`** (e.g. `ABK-20-DIY-etch.svg`): Standalone SVG containing both mirrored top and direct bottom layers with vector text.

> [!TIP]
> Individual raw layer exports (`F.Cu`, `B.Cu`, `Edge.Cuts`) are automatically processed in a temporary directory and deleted after assembly to keep the mask folder clean. If you need to keep them, pass `--keep-layers`.

---

## 🔧 Key Engineering Features

### 1. Vector Font Outlining (Zero Glitches)
Raw SVG `<text>` elements often glitch, bunch up, or suffer font substitution when parsed by headless CLI tools (e.g. MuPDF, Ghostscript).
* The pipeline converts all labels, titles, scale markings, and notes into **100% pure vector bezier paths (`<path d="...">`)** using `matplotlib.textpath`.
* The text is rendered as geometric shapes—identical across all viewers, printers, and RIP software.

### 2. Drill Hole Options (`--drill-shape-opt`)
* **`2` (Actual Drill Hole - Default)**: Cuts out the exact 1:1 physical drill hole diameter of each footprint pad and via (e.g. $0.8\text{ mm}$, $1.0\text{ mm}$, $1.2\text{ mm}$). This matches traditional photographic PCB masks.
* **`1` (Pilot Drill Centers)**: Forces all holes to tiny pilot center marks ($\approx 0.35\text{ mm}$ diameter) to assist hand-drilling while maximizing pad copper area.
* **`0` (Solid Copper)**: No holes printed in pads.

### 3. Exact 50.0 mm Calibration Scale Bar
* Always print at **100% Scale / Actual Size** (never "Fit to Page").
* A precision $50.0\text{ mm}$ scale bar with $10\text{ mm}$ ticks is printed at the bottom of the sheet, allowing the maker to verify printer dimensional accuracy with a caliper before exposure.

### 4. Inkscape CLI Auto-Detection
The script automatically finds the active Inkscape binary or AppImage:
* Searches system `PATH`.
* Searches `~/Software/Inkscape*.AppImage` (e.g. `/home/dusjagr/Software/Inkscape-ebf0e94-x86_64.AppImage`).
* Uses `--export-filename=<output.pdf>` for pure vector Cairo output.

---

## 📋 Step-by-Step Maker Guide: Double-Sided Pouch UV Etching

1. **Print**:
   * Print `ABK-20-DIY-etch.pdf` on laser or inkjet transparency film at **100% (No Scaling)**.
2. **Verify Scale**:
   * Measure the 50 mm calibration bar with a ruler or caliper. It must measure exactly $50.0\text{ mm}$.
3. **Cut & Crease**:
   * Trim excess margins along the outer edge.
   * Score or crease lightly along the dashed center fold line ($X = 148.5\text{ mm}$) and fold in half.
4. **Inspect Alignment**:
   * Hold the folded envelope up to a lamp or light-box.
   * Confirm that the 4 corner crosshairs and pad drill centers overlap. Tape 2 of the open edges with Kapton tape to create a pouch.
5. **Insert & Expose**:
   * Slide the pre-sensitized double-sided FR4 board into the pouch.
   * Expose Side A (UV, e.g. 90-120s), flip the pouch, and expose Side B.
6. **Develop & Etch**:
   * Develop in 1% sodium hydroxide (NaOH) or sodium carbonate.
   * Etch in Ferric Chloride ($FeCl_3$) or Sodium Persulfate at $45-50^\circ\text{C}$ with aeration.

---

## 🔌 Non-Plated Assembly Guide: The 5 Dedicated Wire Bridges

Because DIY etched PCBs do not have chemical through-hole copper plating (PTH), holes are bare fiberglass.

![ABK-20 DIY Ground and Vias Guide](../../docs/img/ABK-20_diy_ground_and_vias_guide.png)

### 1. Dedicated Vias (Must Solder Wire Pins on BOTH Sides)
Drill these 5 holes with an Ø 0.8–0.9 mm bit, push a snipped resistor lead through, and solder on **both top and bottom**:
* **Via 1 at `(86.82, 44.45) mm`** (`GND`): Master ground link connecting bottom power GND (`J4`/`J5`) to the top NeoPixel ground plane.
* **Via 2 at `(91.88, 44.50) mm`** (`VCC`): Master +5V power link to the ATtiny85 and NeoPixels.
* **Via 3 at `(89.31, 44.42) mm`** (`NEO1-DIN`): ATtiny85 PB0 data signal to the first NeoPixel.
* **Via 4 at `(134.75, 39.07) mm`** (`GNDA`): Analog audio ground bridge for the PAM8002 power amp.
* **Via 5 at `(143.29, 63.08) mm`** (`GNDA`): Analog audio ground bridge for the thumbwheel volume pot.

### 2. THT Component Solder-Side Mapping
* **Front Components (`U1`, `RV1`, `SW2`, `SW3`, `POT2-CV1`, `J1`, `J2`)**: Solder pins on **Bottom (`B.Cu`) only**. Zero tracks are trapped beneath component bodies.
* **Back Components (`Jack1`, `Jack2`, `POT3-Vol1`, `J5` tabs)**: Solder pins on **Top (`F.Cu`) only**. Solder the 4 through-hole tabs of `J5` (USB-C) on the top side to create extra heavy-duty ground ties.


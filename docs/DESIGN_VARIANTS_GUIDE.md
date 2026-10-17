# ABK-20 Hardware Design Variants & Customization Guide

This guide explains the architecture of the **ABK-20** project, how KiCad connects schematics to physical PCB layouts, and how you or external contributors can build custom hardware variants, swap components/footprints, or create new form factors without breaking the base design.

---

## 1. The Core Mental Model: How KiCad Connects Everything

Understanding how KiCad separates electrical intent from physical layout is key to creating clean hardware variants:

```
┌─────────────────────────────────┐      (F8)       ┌─────────────────────────────────┐
│     SCHEMATIC (.kicad_sch)      │  ────────────►  │       PCB (.kicad_pcb)          │
│  "What connects to what" (Nets) │  Update PCB     │  "Where parts sit and how       │
│  + Assigned Footprint name      │                 │   copper traces are routed"     │
└─────────────────────────────────┘                 └─────────────────────────────────┘
                 │                                                   │
                 ▼                                                   ▼
┌─────────────────────────────────┐                 ┌─────────────────────────────────┐
│   SYMBOL LIBRARY (.kicad_sym)   │                 │   FOOTPRINT LIBRARY (.pretty)   │
│  Pin numbers & electrical types │                 │  Pads, solder mask & 3D models  │
└─────────────────────────────────┘                 └─────────────────────────────────┘
```

* **Schematic (`.kicad_sch`)**: Defines the electrical circuit (logical pin numbers and net names) and stores the name of the assigned footprint.
* **PCB (`.kicad_pcb`)**: Defines physical component coordinates $(X, Y, \text{rot})$ and copper traces.
* **The Bridge (`F8` / Update PCB from Schematic)**: Whenever a part, net, or footprint assignment changes in the schematic, pressing **`F8`** pushes those updates into the PCB without disturbing your existing traces.

---

## 2. How to Swap Footprints & Components

Different builders have different needs: some want **through-hole (THT) parts for beginner soldering workshops**, others want a **30 mm slide fader** instead of 20 mm, or standard rotary pots instead of thumbwheels.

### Case A: Swapping Footprint Packages (Same Electrical Circuit)
*Example: Replacing SMD 1206 resistors with through-hole axial resistors for a DIY workshop.*

1. In the **PCB Editor**, right-click the footprint $\rightarrow$ **Change Footprint...**
2. In the browser dialog, select the new footprint (e.g., `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal`).
3. Under **Change Options**, choose:
   * *Change selected footprint only*, or
   * *Change all footprints matching 'R_1206_HandSoldering'* to batch-update the entire board.
4. Click **Apply**.
5. **Result**: As long as the pin numbers match (e.g., Pin 1 and Pin 2), all net connections and ratsnest lines remain completely intact.

### Case B: Changing Component Types in the Schematic
*Example: Upgrading the Bourns `PTL20` (20 mm fader) to `PTL30` (30 mm fader).*

1. Open the schematic in the Schematic Editor.
2. Double-click the slider component (`RV1`).
3. Click the **Footprint** field library icon.
4. Select `8Bitmixtape_reworked:Potentiometer_Bourns_PTL30_Single_Slide_LED`.
5. Save the schematic and switch to the PCB Editor.
6. Press **`F8`** (**Update PCB from Schematic**), make sure *"Re-link footprints to schematic symbols based on their Reference"* is selected, and click **Update PCB**.
7. **Result**: KiCad replaces the 20 mm footprint with the 30 mm footprint (including its 3D model) directly on the board.

---

## 3. The Three Architecture Approaches for Project Variants

Depending on how different your hardware version is, choose one of these three workflows:

### Strategy 1: Git Branch-per-Design (Recommended for Official Variants)

This keeps the repository lightweight while giving each hardware design its own clean workspace.

* **`main`**: The pristine, unrouted baseline (tagged `base-template`). Contains the verified schematic, staged components, and pre-routed 5×4 matrix.
* **`design/75x80`**: Compact 75×80 mm desktop version.
* **`design/eurorack-10hp`**: Dedicated branch for a 3U Eurorack modular synth panel.
* **`design/pocket-operator`**: Handheld battery-powered slim edition.

#### How to manage updates across branches:
If a bug is fixed or an improvement is made to the core audio circuit on `main`:
```bash
# Switch to your design branch
git checkout design/75x80

# Pull in the electrical improvements from main
git merge main
```
KiCad merges the schematic changes cleanly. In the PCB editor, press **`F8`** to apply the schematic update—**your routed tracks and layout on `design/75x80` remain safe and untouched.**

---

### Strategy 2: Multi-Board Layouts in One Repo (Side-by-Side Designs)

If you want users who download a single ZIP file from GitHub to open and compare multiple official layouts side-by-side:

```
ABK-20/
├── hardware/
│   ├── common/                    <-- Shared schematic & sub-sheets
│   │   ├── ABK-20.kicad_sch       <-- Main circuit logic
│   │   └── LED_Matrix.kicad_sch   <-- Reused 5x4 matrix sub-sheet!
│   │
│   ├── desktop-75x80/             <-- Variant 1: Compact desktop console
│   │   ├── ABK-20.kicad_pro
│   │   └── ABK-20.kicad_pcb
│   │
│   └── eurorack-10hp/             <-- Variant 2: Modular synth module
│       ├── ABK-20.kicad_pro
│       └── ABK-20.kicad_pcb
```

#### The Power of Hierarchical Sheets:
Notice that the 5×4 NeoPixel matrix lives in its own hierarchical sheet:
[`hardware/LED_Matrix.kicad_sch`](file:///home/dusjagr/Documents/8bit_Mixtape/ABK-20/hardware/LED_Matrix.kicad_sch)

Any variant project can simply import this sheet as a hierarchical block. You never have to redraw or re-wire the 20 NeoPixels!

---

### Strategy 3: KiCad Project Template (For Independent Spin-Offs)

When someone wants to create an entirely independent derivative or community instrument:

1. In KiCad, select **File $\rightarrow$ New Project from Template...**
2. Browse to the ABK-20 project folder.
3. KiCad copies all schematics, local symbols, footprints, and 3D models into a brand-new standalone project directory.
4. The user can rename, add MIDI jacks, modify the outline, or replace parts without having any connection to the original Git repository.

---

## 4. Self-Contained Project Assets (Zero-Dependency Portability)

The ABK-20 repository is structured to be **100% self-contained**. Any user cloning the project has all symbols, footprints, and 3D shapes ready without needing external library installs:

| Asset | Location | Purpose |
| :--- | :--- | :--- |
| **Symbols** | `hardware/mixtape_schematics.kicad_sym` | Bourns PTL20/30 fader, Highly KS01 switch, PAM8002 amp. |
| **Footprints** | `hardware/8Bitmixtape_reworked.pretty/` | Custom slider footprints, SMD battery clips, AAA holders. |
| **3D Models** | `hardware/3d-models/` | Accurate STEP/WRL models (PTL20/30 with travel slit, illuminated switches). |
| **LED Sub-Sheet** | `hardware/LED_Matrix.kicad_sch` | Modular 20-LED matrix circuit. |

---

## 5. Quick-Start: How to Start a New Variant in 3 Steps

If you want to start another form factor (e.g., Eurorack or Cassette):

```bash
# 1. Start from the clean base template
git checkout base-template

# 2. Create a new branch for the variant
git checkout -b design/my-new-formfactor

# 3. Open KiCad, resize Edge.Cuts, place components, and route!
```

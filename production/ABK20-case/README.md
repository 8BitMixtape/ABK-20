# ABK-20 Enclosure Suite: 3D-Printed Snap-Fit & Laser-Cut Console

This directory contains the complete physical enclosure designs for the **ABK-20 Synthesizer** ($75.0 \times 80.0\text{ mm}$ PCB), modeled parametrically in [OpenSCAD](https://openscad.org/).

---

## 1. The Two Enclosure Architectures

| System | Manufacturing Method | Key Files | Ideal Use Case |
| :--- | :--- | :--- | :--- |
| **Snap-Fit Two-Part Enclosure** | **FDM 3D Printing** (Supportless) | [`ABK-20_case_3dprint.scad`](ABK-20_case_3dprint.scad)<br>[`ABK-20_case_3dprint.json`](ABK-20_case_3dprint.json) | Handheld / Desktop direct-fit shell; requires no screws or Eurorack rails. |
| **Tilted Desktop Console ("Chistli")** | **Laser Cutting** (3mm Acrylic / Wood) | [`ABK-20_case.scad`](ABK-20_case.scad)<br>[`ABK-20_case.json`](ABK-20_case.json) | Ergonomic $12^\circ$ angled desk console with extended cheek feet. |
| **Eurorack Frontplate** | **3D Printing** (16 HP / $81\times 92.3\text{ mm}$) | [`ABK-20_frontplate_3dprint.scad`](ABK-20_frontplate_3dprint.scad) | Front panel for Eurorack rails or standard 16 HP desktop racks. |

---

## 2. 3D-Printed Enclosure: Standard vs. Prototype Editions

Because earlier hardware revisions and prototype builds vary in component orientation, `ABK-20_case_3dprint.scad` supports two distinct hardware configurations via OpenSCAD presets:

### A. The Prototype Hardware Edition (Preset: `"perfect Proto"`)
On the early hand-assembled prototype consoles (such as the Randen prototype shown in the main project README), the two **PJ-317 3.5mm audio jacks are soldered on the TOP side of the PCB**, protruding upward through the faceplate.

* **OpenSCAD Preset**: **`"perfect Proto"`** (saved in `ABK-20_case_3dprint.json`)
* **Key Features**:
  * **Top Audio Jack Window Cutouts**: Enclosed rectangular apertures ($14.5\text{ mm} \times 15.5\text{ mm}$, $R=1.4\text{ mm}$) centered over `Jack1` ($X = -30.14\text{ mm}$) and `Jack2` ($X = +30.60\text{ mm}$) with smooth beveled top edges.
  * **Optimized Insertion Tolerance (`pcb_xy_clearance = 1.50 mm`)**: Gives extra lateral play so the PCB drops straight into the shell without binding on the side thumbwheel volume pot (`POT3-Vol1`).
  * **Drop-In Rear Clearance**: Allows the rear USB-C port to slide in cleanly.
* **Preview Image**: [`docs/img/ABK-20_case_3dprint_proto_assembly.png`](../../docs/img/ABK-20_case_3dprint_proto_assembly.png)

```bash
# Render prototype assembly screenshot using OpenSCAD CLI:
openscad -p ABK-20_case_3dprint.json -P "perfect Proto" \
  -o docs/img/ABK-20_case_3dprint_proto_assembly.png \
  --colorscheme=Sunset ABK-20_case_3dprint.scad
```

### B. Standard Production Edition (Preset: `"ABK-20_diffuser_grid"`)
Intended for standard production boards where audio jacks are bottom-mounted and exit horizontally through the rear enclosure wall.
* **Top Face**: Completely solid and continuous across the top-back, featuring only the 5×4 NeoPixel matrix diffuser grid, slide fader slot, rotary pot, toggle switch, and button openings.
* **Rear Wall**: Precision circular cutouts for both 3.5mm jacks and the USB-C power receptacle.
* **Preview Image**: [`docs/img/ABK-20_case_3dprint_assembly.png`](../../docs/img/ABK-20_case_3dprint_assembly.png)

---

## 3. Optical Baffle Grid & The M600 Diffuser Printing Trick

The top shell is printed **face down** directly on the build bed (`Z = 0`), requiring zero support material:

1. **Integrated 5×4 Baffle Grid**:
   Internal dividing walls ($0.60\text{ mm}$ thick) extend downward from the ceiling to within $0.10\text{ mm}$ of the PCB. This optically isolates every single NeoPixel, completely eliminating light bleed into adjacent cells.
2. **Multi-Color Single-Extruder Filament Swap (`M600`)**:
   * The top diffuser skin is exactly **$0.20\text{ mm}$ thick** (Layer 1).
   * **Layer 1 ($0.00\text{--}0.20\text{ mm}$)**: Print in **White or Translucent PLA**.
   * **Pause / Filament Swap (`M600` at Layer 2)**: Switch to **Black, Pink, or Opaque PLA** for the rest of the print.
   * **Result**: You get a silky-smooth translucent white front diffuser on the outside, while the inner baffle walls are solid dark plastic for razor-sharp pixel contrast!

---

## 4. How to Use the Customizer in OpenSCAD

1. Open `ABK-20_case_3dprint.scad` in OpenSCAD.
2. Open the **Customizer** pane on the right (**Window $\to$ Customizer**).
3. At the top of the Customizer, open the **Preset** dropdown:
   * Select **`perfect Proto`** if building for prototype boards with top-mounted jacks.
   * Select **`ABK-20_diffuser_grid`** if building for standard production boards.
4. Set **Display Mode (`part_to_show`)**:
   * `assembly`: Full 3D inspection with PCB model, jacks, and transparent bottom cover.
   * `top_shell`: Top housing oriented upside-down on the print bed.
   * `bottom_cover`: Bottom lid oriented flat on the bed.
   * `print_plate`: Top shell and bottom cover arranged side by side for a single print run.
5. Press **F6** (Render), then **F7** (Export STL).

---

## 5. Laser-Cut Tilted Console ("Chistli")

[`ABK-20_case.scad`](ABK-20_case.scad) generates a finger-jointed desktop chassis designed for 3.0mm laser-cut acrylic or plywood:
* **$12^\circ$ Ergonomic Playing Tilt**: Angles the controls and 5×4 screen toward the performer.
* **Extended Cheeks**: Side panels feature rounded top corners ($R=8\text{ mm}$) and integrated bottom feet ($R=1.5\text{ mm}$).
* **Eurorack Top Strip**: Support rims with Eurorack mounting holes for easy panel fastening.
* **Exporting for Laser Cutting**: Set `part_to_show = "layout"`, press **F6**, and export as SVG/DXF (**File $\to$ Export as SVG**).

---

## 6. Engineering Notes & Kinematics

For in-depth analysis of PCB insertion kinematics, thumbwheel clearances, button reach, and tolerance stacking, read [**`CASE_DESIGN_NOTES.md`**](CASE_DESIGN_NOTES.md).

---

## 7. Acoustic Optimization & Speaker Back-Chamber Design

For maximum audio fidelity, punch, and low-end bass reproduction from the rear-mounted micro-speaker ($20 \times 8.5\text{ mm}$ driven by the onboard PAM8002 BTL amplifier), refer to [**`ACOUSTIC_OPTIMIZATION_PLAN.md`**](ACOUSTIC_OPTIMIZATION_PLAN.md).

It covers:
* **Dipole Cancellation Prevention**: Perimeter gasket sealing against the PCB.
* **Acoustic Pod / Back-Chamber ($V_b \approx 2.0\text{ cm}^3$)**: Integrating an acoustic cup and tuned bass-reflex port ($f_b \approx 420\text{ Hz}$) into the 3D-printed bottom shell.
* **PCB Soundboard Modes**: Utilizing the $75 \times 80\text{ mm}$ FR4 natural bending resonance ($280 - 380\text{ Hz}$) and silicone O-ring decoupling.
* **Acoustic Polyfill**: Internal chamber stuffing to increase apparent compliance by $15-20\%$.


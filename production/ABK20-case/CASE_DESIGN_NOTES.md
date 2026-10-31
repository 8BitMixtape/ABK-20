# ABK-20 Enclosure Project: Summary & Engineering Review

## 1. Project Summary

We developed two complementary, fully parametric OpenSCAD enclosure systems for the **8Bit Mixtape ABK-20** (`75.0 × 80.0 mm` PCB), backed by a full 3D component mesh exported from KiCad 9:

| File | Manufacturing Target | Architecture |
| :--- | :--- | :--- |
| `ABK-20_pcb.stl` | 3D Reference Mesh | Full PCB + 20 VRML/STEP 3D component models exported via `kicad-cli pcb export vrml` + Blender, centered at `(0, 0, 0)`. |
| `ABK-20_case.scad` | **Laser Cutter** (`3 mm` Acrylic / Wood) | Tilted (`12°`) finger-jointed desktop console with extended side cheeks, Eurorack mounting strips, SVG frontplate (`svgs/ABK_frontplate_02_holes.svg`), and tilted side/back cutouts. |
| `ABK-20_case_3dprint.scad` | **FDM 3D Printer** (Supportless) | Direct-fit two-part enclosure (`top_shell` + `bottom_cover`) with integrated top faceplate, 5×4 NeoPixel baffle grid, `0.20 mm` printed diffuser skin, and 4 corner PCB clamps. |

### Exporting the 3D PCB + Components from KiCad 9 to OpenSCAD
Because the 3D models in `hardware/3d_models/` are VRML (`.wrl`) meshes, KiCad's STEP and direct STL exporters skip the components. Exporting to VRML first and converting via Blender preserves every component:

```bash
kicad-cli pcb export vrml --units mm -o /tmp/ABK-20.wrl ../../hardware/ABK-20.kicad_pcb
blender -b --python-expr "
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.x3d(filepath='/tmp/ABK-20.wrl', axis_forward='Y', axis_up='Z')
bpy.ops.export_mesh.stl(filepath='ABK-20_pcb.stl')
"
```

---

## 2. Deep Dive: What Could Be Improved or Done Differently

After analyzing the exact 3D component coordinates and physical constraints of the `ABK-20` PCB inside `ABK-20_case_3dprint.scad`, here are the most impactful mechanical and usability improvements to consider after the first test print:

### A. PCB Insertion Kinematics (The "Thumbwheel vs. Top Shafts" Geometry Problem)

Look closely at what sticks out past the `75.0 × 80.0 mm` PCB outline AND what sticks up through the top ceiling at the same time:
- **Right Edge (`X = +37.5 mm`)**: The thumbwheel (`POT3-Vol1`) sticks out **`3.72 mm`** past the PCB edge (to `X = +41.22 mm`) at `Z = -2.4 .. -4.6 mm`.
- **Back Edge (`Y = +40.0 mm`)**: The two PJ-317 audio jack barrels (`Jack1`, `Jack2`) stick out **`2.67 mm`** past the PCB edge (to `Y = +42.67 mm`) at `Z = -3.85 .. -10.75 mm`.
- **Top Surface (`Z > 0.8 mm`)**: The rotary pot shaft (`POT2-CV1`, `Z = +24.6 mm`), slide pot lever (`RV1`, `Z = +17.8 mm`), toggle switch (`SW3`, `Z = +18 mm`), and vertical pin headers (`J1`/`J2`, `Z = +9.3 mm`) all protrude through the top ceiling (`Z = +8.1 .. +10.1 mm`).

Because the thumbwheel sticks out `+3.72 mm` to the right while the audio jacks stick out `+2.67 mm` to the back:
1. For the **audio jacks**, we added `jack_drop_in_slot = true` (which opens the jack holes down to the bottom split line `z_split = -12.5 mm`), so the back barrels slide in vertically.
2. However, for the **thumbwheel (`POT3-Vol1`)**, the slot is a closed window at `Z = -3.5 mm`, while the right wall continues solidly down to `z_split = -12.5 mm`. To insert the PCB from the bottom, you have to **angle the right side of the PCB in first** so the thumbwheel enters its slot, and then swing the left side of the PCB up. Because the tall top shafts (`POT2-CV1`, `SW3`, `RV1`, `J1`, `J2`) are entering the top ceiling holes at the same time, tilting the PCB can cause the shafts to bind against the ceiling holes.

**Two ways we can make PCB insertion effortless in v2:**
1. **Split the Shell at the Thumbwheel/USB-C Plane (`z_split ≈ -3.5 mm`)**:
   Instead of the Top Shell going all the way down to `-12.5 mm`, split the case higher up (`Z = -3.5 mm`) or use a stepped parting line. That way the thumbwheel slot and USB-C slot sit right on the seam between the Top Shell and Bottom Tub—allowing the PCB to drop straight in vertically with zero tilting.
2. **Add an Internal Vertical Relief Channel on the Right Wall**:
   Keep the full-height Top Shell, but carve a `2.0 mm` deep vertical slide groove on the *inside* of the right wall from `z_split` (`-12.5 mm`) up to the thumbwheel slot (`-3.5 mm`) so the thumbwheel only needs ~`1.5 mm` of lateral play to snap in.

---

### B. Recessed Tactile Buttons (`SW4` Reset & `SW1` Master Power / AudioBoot)

Look at the Z heights of the two small switches relative to the top outer face of the 3D-printed shell (`z_top_outer = +10.1 mm`):
- **`SW4` (Reset Button at `(-30.47, 21.68)`)**: SMD switch (`SW_SPST_FSMSM`) whose button top sits at **`Z = +2.2 mm`**—meaning it is recessed **`7.9 mm` deep** inside a `3.8 mm` hole. It can only be pressed with a pen tip or paperclip.
- **`SW1` (Master Power / AudioBoot Switch at `(-14.72, 34.27)`)**: Latching switch whose button top sits at **`Z = +4.3 mm`** (`5.8 mm` below the outer top surface). Since cycling `SW1` is how you enter the **AudioBoot** bootloader, you'll want easy finger access to `SW1`.

**How to improve this:**
- **Integrated 3D-Printed Flex Buttons (Print-in-Place Cantilevers)**: We can cut a U-shaped slot in the top shell ceiling directly over `SW4` and/or `SW1` with a built-in downward nub on the underside that reaches down to `Z = +4.5 mm` (for `SW1`) and `Z = +2.4 mm` (for `SW4`). That turns the top shell plastic itself into a clickable tactile button with zero loose parts!
- Alternatively, for `SW1`, we can add a countersunk finger scoop around its hole so a fingertip can reach the button directly.

---

### C. Securing the PCB & Bottom Cover Under Button/Cable Forces

When holding the case in your hand and pressing the main button (`SW2`) or plugging in a 3.5mm audio cable from the back, the PCB is pushed downward against the 4 corner pillars of `bottom_cover()`. Currently, `bottom_cover` is held by friction along its `3.0 mm` inner lip.

**Three upgrades to make the closure rock-solid:**
1. **Use the Existing Panel Nuts on `SW3` and `POT2-CV1`**:
   Both the toggle switch (`SW3`) and rotary potentiometer (`POT2-CV1`) have threaded bushings. If we add a recessed counterbore around the `SW3` hole on the top face (or add an internal spacer ring that rests on the `SW3` and `POT2-CV1` shoulders), threading the nut onto `SW3` and/or `POT2-CV1` locks the PCB directly to the Top Shell!
2. **Snap-Fit Detent Ridges + Fingernail Pry Slots**:
   Borrowing the `45°` snap-notch concept from `case3000.scad`, we can add `0.35 mm` snap bumps on the front/left/right inner walls of `top_shell` with matching grooves on `bottom_cover`'s lip, plus two small `6 × 1.2 mm` fingernail slots at the bottom seam so you can pop the lid open easily.
3. **Slide Pot (`RV1`) Support**:
   `RV1` (`Bourns PTL20`) has two M2 mounting holes (`29.08, 24.27` and `29.08, -6.71`), and its top body sits at `Z = +3.55 mm` while the ceiling is at `Z = +8.1 mm`. Adding two small internal standoffs extending down from the ceiling to `Z = +3.6 mm` around those two screw holes will keep the slide pot rock-solid when moving the fader.

---

### D. Multi-Color / High-Contrast LED Diffuser Printing Trick

Because `top_shell()` prints upside-down on the build plate (`Z = 0`), the `0.20 mm` diffuser skin (`diffuser_cover_thickness = 0.20`) is the **very first layer** printed on the bed:
- **Single-Extruder Filament Swap (`M600` at Layer 2)**: Print Layer 1 (`0.00–0.20 mm`) in **White or Natural/Translucent PLA**, then swap to **Pink or Black PLA** at `Z = 0.20 mm` for the rest of the print.
- **Result**: You get a crystal-bright white diffuser face on top, while the internal `0.60 mm` baffle grid walls (`LedGridCells2D`) are printed in dark/colored filament—completely eliminating pixel-to-pixel light bleed!

---

### E. Laser-Cut Case (`ABK-20_case.scad`) Refinements

For the laser-cut tilted console version:
1. **Tilted Back-Wall Entry Clearance**: Because the PCB is tilted at `12°` while the laser-cut back wall is vertical (`90°`), a 3.5mm audio plug or USB-C plug enters at a `12°` downward angle through a `3.0 mm` vertical wall. The enlarged `9.0 mm` jack holes and `14 × 7 mm` USB-C slot in the `ABK-20_tilted` preset handle this well, and if needed we can add a `usb_z_fine_offset` / `jack_z_fine_offset` slider (`±2 mm`) to center the hole around the angled plug shaft rather than the jack face.
2. **Cleanup of Unused SVGs**: `ABK20-case/svgs/` still contains the inherited `blinkeshit-*`, `dummy-*`, and `hex-top-*` SVGs from `eurorack2chistli`, which can be removed to keep the `ABK-20` repository clean.


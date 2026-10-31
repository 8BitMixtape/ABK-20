# HiFi Audio & Acoustic Optimization Plan for ABK-20 Enclosures

This document serves as the master engineering reference for optimizing acoustic output, frequency response, and bass reproduction from the rear-mounted micro-speaker on the ABK-20 synthesizer in 3D-printed and laser-cut enclosures.

---

## 1. Physical Architecture & The Dipole Problem

```
               Front Wave (Treble & Attack)
                      ▲ ▲ ▲
  ┌───────────────────│─│─│───────────────────────────┐  <-- ABK-20 FR4 PCB (Soundboard)
  │                   ▼ ▼ ▼                           │
  │             [ Acoustic Loch ]                     │
  │          (Options A, B, or C)                     │
  │       ╔═════════════════════════════════╗         │
  └───────╫  Micro-Speaker (Adhesive Seal)  ╫─────────┘
          ║  diaphragm [===] voice coil     ║
          ╚═════════════════════════════════╝
                      │ │ │
                      ▼ ▼ ▼
           [ Sealed Back Chamber / Port ]              <-- 3D Printed / Laser-cut Enclosure
              (Vb ≈ 1.5 - 3.0 cm³)
```

### The Acoustic Short-Circuit
The speaker is an electrodynamic transducer ($\approx 20 \times 8.5\text{ mm}$, $S_d \approx 80\text{ mm}^2$, $F_0 \approx 700 - 1000\text{ Hz}$).
When the diaphragm moves, it generates two opposing waves:
* **Front Wave**: Radiates through the "loch" acoustic holes in the PCB.
* **Back Wave**: Radiates $180^\circ$ out-of-phase from the rear of the speaker.

Without an airtight barrier separating the two waves, destructive acoustic cancellation completely eliminates sound below $\approx 1\text{ kHz}$.

### Rule #1: The Perimeter Gasket Seal
* The speaker's white double-sided adhesive ring must form an **unbroken, airtight seal against the bottom copper/FR4 plane** around the "loch".
* Any air leak around the perimeter of the speaker frame will cause immediate loss of low-frequency response.

---

## 2. Front Acoustic Impedance: The "Loch" Design

The PCB is 1.6 mm thick FR4. Each hole acts as an acoustic pipe of length $L = 1.6\text{ mm} + \text{end corrections} \approx 2.3\text{ mm}$.
If the open hole area is too small, air velocity in the holes causes viscous boundary-layer friction, choking high frequencies and generating port turbulence/chuffing noise.

### Footprint Options in `hardware/8Bitmixtape_reworked.pretty/`:
* **Option A (`Speaker_Micro_Loch_4x3`)**: 12 round holes ($\varnothing 0.8\text{ mm}$), $A \approx 6.0\text{ mm}^2$.
* **Option B (`Speaker_Micro_Loch_4Slots`)**: 4 milled slots ($0.8 \times 2.8\text{ mm}$), $A \approx 9.0\text{ mm}^2$. Directly aligns with the 4 physical speaker sound vents.
* **Option C (`Speaker_Micro_Loch_Honeycomb`)**: 19 round holes ($\varnothing 0.8\text{ mm}$), $A \approx 9.55\text{ mm}^2$. Classic synthesizer acoustic grill.

> **Recommendation**: **Option B** or **Option C** provides the lowest acoustic inertance and lowest viscous losses ($\ge 35\%$ aperture ratio).

---

## 3. Back Cavity Engineering: The Enclosure Cabinet

The bottom enclosure shell should be designed as a miniature loudspeaker cabinet rather than an open tub.

### Approach 1: Integrated 3D-Printed Acoustic Cup / Pod
In `production/ABK20-case/ABK-20_case_3dprint.scad`:
1. **Cup Geometry**:
   * Add a rectangular or stadium-shaped wall rising from the bottom case floor that mates against the back of the PCB surrounding the speaker footprint.
   * Coordinate center: `X = 105.33 mm`, `Y = 81.50 mm` (matching footprint placement).
   * Wall thickness: $1.2 - 1.6\text{ mm}$ (3-4 perimeters for zero air leakage).
   * Top rim: Optional $0.5\text{ mm}$ groove for a soft silicone bead or compressed closed-cell EVA foam gasket.
2. **Back Volume ($V_b$) Target**:
   * Target volume: $V_b \approx 1.5 - 3.0\text{ cm}^3$ ($1500 - 3000\text{ mm}^3$).
   * Maintaining $V_b \ge 2.0\text{ cm}^3$ keeps air spring stiffness low, allowing the driver to reach its maximum low-frequency excursion.
3. **Optional Tuned Bass-Reflex Port (Helmholtz Resonator)**:
   * A small duct integrated into the case bottom ($D = 2.5\text{ mm}$, Length $L = 20\text{ mm}$).
   * Helmholtz resonance formula:
     $$f_b = \frac{c}{2\pi} \sqrt{\frac{S}{V_b (L + 0.85 d)}}$$
   * With $c = 343\text{ m/s}$, $S = \pi \times 1.25^2 \approx 4.9\text{ mm}^2$, $V_b = 2.2\text{ cm}^3$, $L = 20\text{ mm}$:
     $$f_b \approx 420\text{ Hz}$$
   * This provides a $+5\text{ dB}$ acoustic reinforcement bump right at the fundamental punch frequency of 8-bit chip kicks, snares, and basslines!

### Approach 2: Sealed Lower Case (Infinite Baffle Mode)
For laser-cut stacked acrylic/wood cases:
* Place an unbroken EVA foam or silicone gasket along the perimeter shoulder where the PCB rests.
* Seal the USB-C and audio jack cutouts with snug silicone bezels.
* The entire lower cavity ($V_b \approx 30 - 45\text{ cm}^3$) acts as an acoustic suspension chamber.

---

## 4. PCB Soundboard Principle (Distributed Mode Loudspeaker)

The $75 \times 80\text{ mm}$ 1.6mm FR4 PCB acts as a sounding board:
* **Natural Plate Mode**:
  Clamped at the 4 standoff corners, the fundamental flexural bending mode $(1,1)$ of the board occurs at $\approx 280 - 380\text{ Hz}$, aligning with the middle octave of bass synths.
* **Off-Center Driver Placement**:
  The speaker at `(105.33, 81.50)` is slightly off-center. Symmetrical center placement produces harsh cancellation notches; off-center excitation distributes modal energy across multiple plate resonances smoothly.
* **Mechanical Decoupling**:
  To prevent plastic/metal rattles against the enclosure, mount the PCB using **M3 silicone / rubber O-rings** above and below the board at the 4 corner standoffs.

---

## 5. Acoustic Polyfill (Chamber Stuffing)

Inside the rear chamber:
* Insert a light pinch of polyester fiberfill or open-cell reticulated acoustic foam.
* **Acoustic Function**:
  1. Absorbs internal standing waves and prevents "boxy" mid-range coloration.
  2. Slows air velocity, converting adiabatic compression into isothermal compression.
  3. **Apparent Volume Increase**: Increases acoustic compliance by $15 - 20\%$, making a $2.0\text{ cm}^3$ pod behave acoustically like a $2.4\text{ cm}^3$ pod.

---

## 6. Electrical Power & DSP / Software Bass Tuning

* **Amplifier**: The onboard **PAM8002** Class-AB/D mono amplifier provides a **differential Bridge-Tied Load (BTL)** output capable of delivering $2.0 - 2.5\text{ W}$ into $4 - 8\ \Omega$ at $5\text{ V}$.
* **No Coupling Capacitors**: BTL drive eliminates DC-blocking output capacitors, preserving full low-frequency extension down to DC.
* **Psychoacoustic Bass (Virtual Pitch / Missing Fundamental)**:
  Micro-speakers physically cannot move enough air below $120\text{ Hz}$. In software bytebeat/synth routines, generating rich harmonic overtones (2nd harmonic at $160-240\text{ Hz}$, 3rd at $240-360\text{ Hz}$) causes the human brain to reconstruct the deep sub-bass pitch with high clarity and zero distortion.


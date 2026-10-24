#!/usr/bin/env python3
"""
ABK-20 Frontplate Generator
Generates mechanically accurate vector SVG frontplates for the ABK-20 desktop synthesizer.
Derives 1:1 component placements directly from hardware/ABK-20.kicad_pcb.

Overhangs:
  - Left & Right sides: +1.0 mm overhang (Total width: 75.0 + 2*1.0 = 77.0 mm)
  - Top & Bottom:       +6.0 mm overhang (Total height: 80.0 + 2*6.0 = 92.0 mm)

Outputs in hardware/:
  - ABK-20_frontplate.svg                (Primary frontplate with 5x4 matrix display window)
  - ABK-20_frontplate_discrete_leds.svg  (Variant with 20 individual circular LED holes)
"""

import math
import re
from pathlib import Path

# PCB Dimensions
PCB_W = 75.0
PCB_H = 80.0

# Requested Overhangs
OVERHANG_X = 1.0       # 1 mm on left and right
OVERHANG_Y = 6.0       # 6 mm on top and bottom

# Total Frontplate Dimensions
WIDTH = PCB_W + 2 * OVERHANG_X   # 77.0 mm
HEIGHT = PCB_H + 2 * OVERHANG_Y  # 92.0 mm
CORNER_RADIUS = 3.0              # Outer plate rounded corner radius

# Helper to offset PCB coordinates to Frontplate coordinates
def to_plate(x_pcb, y_pcb):
    return x_pcb + OVERHANG_X, y_pcb + OVERHANG_Y

# Component Coordinates on PCB:
# 1. Top Controls
SW1_X_PCB, SW1_Y_PCB = 22.782, 5.728          # Power Switch
SW1_DIAMETER = 6.5

SW4_X_PCB, SW4_Y_PCB = 7.033, 18.326          # Hardware Reset tactile switch pinhole
SW4_DIAMETER = 3.2

# 2. 5x4 NeoPixel Display Matrix
MATRIX_COLS_PCB = [19.880, 28.801, 37.723, 46.645, 55.567]
MATRIX_ROWS_PCB = [18.199, 26.158, 34.116, 42.075]
MATRIX_CENTER_X_PCB = 37.724
MATRIX_CENTER_Y_PCB = 30.137
MATRIX_WINDOW_W = 42.0
MATRIX_WINDOW_H = 30.0
MATRIX_WINDOW_R = 2.0
LED_HOLE_DIAMETER = 4.5

# 3. Bourns PTL20 Slide Fader
RV1_X_PCB, RV1_Y_PCB = 66.561, 31.218          # Fader Center
RV1_SLOT_W = 2.6
RV1_SLOT_H = 22.0                              # 20mm active travel + 2mm margin
RV1_SCREW_TOP_Y_PCB = 15.718                   # Top M2 mounting screw
RV1_SCREW_BOT_Y_PCB = 46.718                   # Bottom M2 mounting screw
RV1_SCREW_DIAMETER = 2.2                       # M2 clearance drill

# 4. Bottom Performance Controls
SW3_X_PCB, SW3_Y_PCB = 14.203, 65.165          # MTS-102 SPDT Toggle Switch
SW3_DIAMETER = 6.2                             # M6 threaded bushing clearance

POT2_X_PCB, POT2_Y_PCB = 37.473, 64.804        # RV09 Rotary Potentiometer (Clear Shaft)
POT2_DIAMETER = 7.5                            # RV09 collar / shaft clearance

SW2_X_PCB, SW2_Y_PCB = 59.669, 65.087          # Highly KS01-BL-13 Illuminated Push Button
SW2_DIAMETER = 9.5                             # Upper part plunger clearance (D=9.0mm upper cap + 0.5mm clearance; base collar is D=12.0mm)

# 5. Case Mounting Holes (placed in the 6mm top & bottom overhang flanges)
FLANGE_MOUNTING_HOLES = [
    (6.0, 3.0),
    (WIDTH - 6.0, 3.0),
    (6.0, HEIGHT - 3.0),
    (WIDTH - 6.0, HEIGHT - 3.0)
]
FLANGE_HOLE_DIAMETER = 3.0                     # M2.5 / M3 screw clearance


def polar_pt(cx, cy, r, angle_deg):
    rad = math.radians(angle_deg)
    return cx + r * math.cos(rad), cy + r * math.sin(rad)


def create_pot_dial_svg(cx, cy, r_inner=5.5, r_outer=7.0, r_text=8.8):
    """Generate dial ticks from -135 to +135 deg around POT2."""
    ticks_svg = []
    for i in range(11):
        angle = -135.0 + i * (270.0 / 10.0)
        x1, y1 = polar_pt(cx, cy, r_inner, angle)
        is_major = (i in [0, 5, 10])
        r_out = r_outer + (0.8 if is_major else 0.0)
        x2, y2 = polar_pt(cx, cy, r_out, angle)
        stroke_w = "0.3" if is_major else "0.2"
        ticks_svg.append(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="#ffffff" stroke-width="{stroke_w}"/>')
        
        if is_major:
            lbl = "0" if i == 0 else ("5" if i == 5 else "10")
            tx, ty = polar_pt(cx, cy, r_text, angle)
            ticks_svg.append(f'<text x="{tx:.3f}" y="{ty+0.7:.3f}" font-family="monospace, sans-serif" font-size="2.0" font-weight="bold" fill="#ffffff" text-anchor="middle">{lbl}</text>')

    start_x, start_y = polar_pt(cx, cy, r_inner - 0.3, -135.0)
    end_x, end_y = polar_pt(cx, cy, r_inner - 0.3, 135.0)
    arc_path = f'<path d="M {start_x:.3f} {start_y:.3f} A {r_inner-0.3:.3f} {r_inner-0.3:.3f} 0 1 1 {end_x:.3f} {end_y:.3f}" fill="none" stroke="#ffffff" stroke-width="0.2" stroke-dasharray="0.8, 0.6"/>'
    ticks_svg.insert(0, arc_path)
    return "\n    ".join(ticks_svg)


def create_fader_scale_svg(x_slot, y_center):
    """Generate scale marks next to the slide fader matching Patterns 0 to 3."""
    scale_svg = []
    y_top = y_center - 10.0
    y_bot = y_center + 10.0
    
    patterns = [
        (3, y_top),
        (2, y_top + 20.0 / 3.0),
        (1, y_top + 40.0 / 3.0),
        (0, y_bot)
    ]
    
    for pat_num, y_pos in patterns:
        x_tick_start = x_slot - 2.2
        x_tick_end = x_slot - 4.5
        scale_svg.append(f'<line x1="{x_tick_start:.3f}" y1="{y_pos:.3f}" x2="{x_tick_end:.3f}" y2="{y_pos:.3f}" stroke="#ffffff" stroke-width="0.3"/>')
        scale_svg.append(f'<text x="{x_tick_end - 1.2:.3f}" y="{y_pos + 0.7:.3f}" font-family="monospace, sans-serif" font-size="2.0" font-weight="bold" fill="#ffffff" text-anchor="end">{pat_num}</text>')
    
    for i in range(3):
        y_mid = y_top + (i + 0.5) * (20.0 / 3.0)
        scale_svg.append(f'<line x1="{x_slot - 2.2:.3f}" y1="{y_mid:.3f}" x2="{x_slot - 3.5:.3f}" y2="{y_mid:.3f}" stroke="#ffffff" stroke-width="0.18"/>')

    return "\n    ".join(scale_svg)


def get_coconut_logo_svg(cx=68.5, cy=81.5, scale=0.65, color="#8899aa"):
    """Extract authentic 8Bit Mixtape Coconut Logo (007_dusjagr:Coconut_logo_sm) from KiCad PCB."""
    pcb_path = Path(__file__).resolve().parents[1] / "ABK-20.kicad_pcb"
    if not pcb_path.exists():
        return ""
    text = pcb_path.read_text(encoding="utf-8")
    parts = text.split("(footprint ")
    paths = []
    for p in parts[1:]:
        if "Coconut_logo" in p:
            blocks = p.split("(fp_poly")
            for b in blocks[1:21]: # First 20 are the F.Cu copper polygons
                pts = re.findall(r"\(xy\s+([-0-9.]+)\s+([-0-9.]+)\)", b)
                if pts:
                    d = "M " + " L ".join([f"{float(x):.3f} {float(y):.3f}" for x, y in pts]) + " Z"
                    paths.append(d)
            break
    if not paths:
        return ""
    paths_str = "\n      ".join([f'<path d="{d}" />' for d in paths])
    return f"""    <!-- Authentic 8Bit Mixtape Coconut Logo (007_dusjagr:Coconut_logo_sm) -->
    <g transform="translate({cx:.3f}, {cy:.3f}) scale({scale:.3f})" fill="{color}" fill-rule="evenodd" opacity="0.9">
      {paths_str}
    </g>"""


def build_svg(matrix_mode="window"):
    # Calculate translated component positions on frontplate:
    sw1_x, sw1_y = to_plate(SW1_X_PCB, SW1_Y_PCB)
    sw4_x, sw4_y = to_plate(SW4_X_PCB, SW4_Y_PCB)
    rv1_x, rv1_y = to_plate(RV1_X_PCB, RV1_Y_PCB)
    rv1_screw_top_y = RV1_SCREW_TOP_Y_PCB + OVERHANG_Y
    rv1_screw_bot_y = RV1_SCREW_BOT_Y_PCB + OVERHANG_Y
    sw3_x, sw3_y = to_plate(SW3_X_PCB, SW3_Y_PCB)
    pot2_x, pot2_y = to_plate(POT2_X_PCB, POT2_Y_PCB)
    sw2_x, sw2_y = to_plate(SW2_X_PCB, SW2_Y_PCB)
    matrix_cx, matrix_cy = to_plate(MATRIX_CENTER_X_PCB, MATRIX_CENTER_Y_PCB)

    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
               f'width="{WIDTH}mm" height="{HEIGHT}mm" viewBox="0 0 {WIDTH} {HEIGHT}" version="1.1">')
    
    svg.append("""  <defs>
    <style>
      .cut-line { stroke: #ff0000; stroke-width: 0.1; fill: none; }
      .hole-line { stroke: #0066ff; stroke-width: 0.1; fill: none; }
      .engrave-text { font-family: 'Helvetica Neue', Arial, sans-serif; fill: #ffffff; }
      .panel-bg { fill: #11141a; }
      .pcb-ref { stroke: #2a3444; stroke-width: 0.2; stroke-dasharray: 1.0, 1.0; fill: none; }
    </style>
  </defs>""")

    # 1. Background Panel
    svg.append('  <!-- LAYER 1: PANEL BACKGROUND -->')
    svg.append('  <g id="layer-panel-base" inkscape:label="Panel Base" inkscape:groupmode="layer">')
    svg.append(f'    <rect class="panel-bg" x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="{CORNER_RADIUS}" ry="{CORNER_RADIUS}"/>')
    # Subtle dashed outline showing PCB footprint underneath
    svg.append(f'    <!-- Underlying PCB reference boundary (75x80mm) -->')
    svg.append(f'    <rect class="pcb-ref" x="{OVERHANG_X}" y="{OVERHANG_Y}" width="{PCB_W}" height="{PCB_H}" rx="2.0" ry="2.0"/>')
    svg.append('  </g>')

    # 2. Silkscreen Artwork & Typography
    svg.append('\n  <!-- LAYER 2: SILKSCREEN & ENGRAVING -->')
    svg.append('  <g id="layer-silkscreen" inkscape:label="Silkscreen &amp; Engraving" inkscape:groupmode="layer">')
    
    # Outer decorative framing border
    svg.append('    <!-- Decorative Framing Lines -->')
    svg.append(f'    <rect x="2.0" y="2.0" width="{WIDTH - 4.0:.1f}" height="{HEIGHT - 4.0:.1f}" rx="2.0" ry="2.0" fill="none" stroke="#252d3a" stroke-width="0.35"/>')
    svg.append(f'    <line x1="2.0" y1="{OVERHANG_Y + 12.0:.1f}" x2="{WIDTH - 2.0:.1f}" y2="{OVERHANG_Y + 12.0:.1f}" stroke="#252d3a" stroke-width="0.3"/>')
    svg.append(f'    <line x1="2.0" y1="{OVERHANG_Y + 54.0:.1f}" x2="{WIDTH - 2.0:.1f}" y2="{OVERHANG_Y + 54.0:.1f}" stroke="#252d3a" stroke-width="0.3"/>')

    # Brand Title Header (centered in top section)
    svg.append('    <!-- Header Title -->')
    svg.append(f'    <text x="{WIDTH / 2.0:.1f}" y="{OVERHANG_Y + 6.2:.1f}" class="engrave-text" font-size="3.4" font-weight="900" letter-spacing="1.2" text-anchor="middle">ABK-20</text>')
    svg.append(f'    <text x="{WIDTH / 2.0:.1f}" y="{OVERHANG_Y + 10.0:.1f}" class="engrave-text" font-size="1.4" font-weight="600" fill="#8899aa" letter-spacing="0.5" text-anchor="middle">8-BIT SYNTHESIZER CONSOLE</text>')

    # Top Controls Labels
    svg.append('    <!-- Power & Reset Labels -->')
    svg.append(f'    <text x="{sw1_x:.3f}" y="{sw1_y + 5.2:.3f}" class="engrave-text" font-size="1.5" font-weight="bold" fill="#ffffff" text-anchor="middle">PWR</text>')
    svg.append(f'    <text x="{sw4_x:.3f}" y="{sw4_y + 3.4:.3f}" class="engrave-text" font-size="1.3" font-weight="bold" fill="#8899aa" text-anchor="middle">RST</text>')

    # Matrix Display Header
    svg.append('    <!-- Matrix Title -->')
    svg.append(f'    <text x="{matrix_cx:.3f}" y="{OVERHANG_Y + 14.5:.1f}" class="engrave-text" font-size="1.5" font-weight="bold" fill="#66bbff" letter-spacing="0.5" text-anchor="middle">5 × 4 NEOPIXEL MATRIX</text>')

    # Fader Scale & Labels
    svg.append('    <!-- Slide Fader Scale & Pattern Labels -->')
    svg.append(f'    {create_fader_scale_svg(rv1_x, rv1_y)}')
    svg.append(f'    <text x="{rv1_x:.3f}" y="{rv1_screw_top_y - 2.2:.3f}" class="engrave-text" font-size="1.6" font-weight="bold" fill="#ff7733" text-anchor="middle">PATTERN</text>')
    svg.append(f'    <text x="{rv1_x:.3f}" y="{rv1_screw_bot_y + 3.6:.3f}" class="engrave-text" font-size="1.3" font-weight="600" fill="#8899aa" text-anchor="middle">FADER</text>')

    # Bottom Controls: Toggle SW3
    svg.append('    <!-- Bottom Controls: Toggle SW3 -->')
    svg.append(f'    <text x="{sw3_x:.3f}" y="{sw3_y - 5.5:.3f}" class="engrave-text" font-size="1.4" font-weight="bold" fill="#ffcc00" text-anchor="middle">▲ 130 BPM</text>')
    svg.append(f'    <text x="{sw3_x:.3f}" y="{sw3_y + 6.8:.3f}" class="engrave-text" font-size="1.4" font-weight="bold" fill="#ffcc00" text-anchor="middle">▼ 166 BPM</text>')
    svg.append(f'    <text x="{sw3_x:.3f}" y="{sw3_y + 10.2:.3f}" class="engrave-text" font-size="1.6" font-weight="bold" fill="#ffffff" text-anchor="middle">TEMPO</text>')

    # Bottom Controls: Potentiometer POT2 Dial & Label
    svg.append('    <!-- Bottom Controls: Potentiometer POT2 -->')
    svg.append(f'    {create_pot_dial_svg(pot2_x, pot2_y)}')
    svg.append(f'    <text x="{pot2_x:.3f}" y="{pot2_y + 9.5:.3f}" class="engrave-text" font-size="1.8" font-weight="bold" fill="#ffffff" text-anchor="middle">FILTER</text>')
    svg.append(f'    <text x="{pot2_x:.3f}" y="{pot2_y + 11.8:.3f}" class="engrave-text" font-size="1.3" font-weight="600" fill="#8899aa" text-anchor="middle">CUTOFF</text>')

    # Bottom Controls: Button SW2
    svg.append('    <!-- Bottom Controls: Button SW2 -->')
    svg.append(f'    <circle cx="{sw2_x:.3f}" cy="{sw2_y:.3f}" r="6.1" fill="none" stroke="#252d3a" stroke-width="0.3" stroke-dasharray="1.0, 0.8"/>')
    svg.append(f'    <text x="{sw2_x:.3f}" y="{sw2_y + 9.5:.3f}" class="engrave-text" font-size="1.8" font-weight="bold" fill="#ffffff" text-anchor="middle">ACCENT</text>')
    svg.append(f'    <text x="{sw2_x:.3f}" y="{sw2_y + 11.8:.3f}" class="engrave-text" font-size="1.3" font-weight="600" fill="#33dd66" text-anchor="middle">+1 OCTAVE</text>')

    # Authentic Coconut Logo in bottom corner
    coconut_svg = get_coconut_logo_svg(cx=68.0, cy=82.0, scale=0.55, color="#8899aa")
    if coconut_svg:
        svg.append(coconut_svg)

    svg.append('  </g>')

    # 3. Outer Cut Line
    svg.append('\n  <!-- LAYER 3: PANEL OUTLINE CUT -->')
    svg.append('  <g id="layer-outline-cut" inkscape:label="Panel Cut Outline" inkscape:groupmode="layer">')
    svg.append(f'    <rect class="cut-line" x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="{CORNER_RADIUS}" ry="{CORNER_RADIUS}"/>')
    svg.append('  </g>')

    # 4. Hardware Cutouts & Slots
    svg.append('\n  <!-- LAYER 4: HARDWARE CUTOUTS & SLOTS -->')
    svg.append('  <g id="layer-hardware-cutouts" inkscape:label="Hardware Cutouts" inkscape:groupmode="layer">')
    
    # Power Switch
    svg.append(f'    <!-- SW1 Power Switch (D={SW1_DIAMETER}mm) -->')
    svg.append(f'    <circle class="hole-line" cx="{sw1_x:.3f}" cy="{sw1_y:.3f}" r="{SW1_DIAMETER / 2.0:.3f}"/>')

    # Reset Button
    svg.append(f'    <!-- SW4 Reset Switch (D={SW4_DIAMETER}mm) -->')
    svg.append(f'    <circle class="hole-line" cx="{sw4_x:.3f}" cy="{sw4_y:.3f}" r="{SW4_DIAMETER / 2.0:.3f}"/>')

    # Slide Fader RV1 Slot & M2 Screws
    slot_x = rv1_x - (RV1_SLOT_W / 2.0)
    slot_y = rv1_y - (RV1_SLOT_H / 2.0)
    slot_r = RV1_SLOT_W / 2.0
    svg.append(f'    <!-- RV1 Slide Fader Slot ({RV1_SLOT_W}x{RV1_SLOT_H}mm pill slot) -->')
    svg.append(f'    <rect class="cut-line" x="{slot_x:.3f}" y="{slot_y:.3f}" width="{RV1_SLOT_W:.3f}" height="{RV1_SLOT_H:.3f}" rx="{slot_r:.3f}" ry="{slot_r:.3f}"/>')
    svg.append(f'    <!-- RV1 Top M2 Screw Hole (D={RV1_SCREW_DIAMETER}mm) -->')
    svg.append(f'    <circle class="hole-line" cx="{rv1_x:.3f}" cy="{rv1_screw_top_y:.3f}" r="{RV1_SCREW_DIAMETER / 2.0:.3f}"/>')
    svg.append(f'    <!-- RV1 Bottom M2 Screw Hole (D={RV1_SCREW_DIAMETER}mm) -->')
    svg.append(f'    <circle class="hole-line" cx="{rv1_x:.3f}" cy="{rv1_screw_bot_y:.3f}" r="{RV1_SCREW_DIAMETER / 2.0:.3f}"/>')

    # Toggle Switch SW3
    svg.append(f'    <!-- SW3 MTS-102 Toggle Switch (D={SW3_DIAMETER}mm) -->')
    svg.append(f'    <circle class="hole-line" cx="{sw3_x:.3f}" cy="{sw3_y:.3f}" r="{SW3_DIAMETER / 2.0:.3f}"/>')

    # Rotary Potentiometer POT2
    svg.append(f'    <!-- POT2-CV1 RV09 Potentiometer (D={POT2_DIAMETER}mm) -->')
    svg.append(f'    <circle class="hole-line" cx="{pot2_x:.3f}" cy="{pot2_y:.3f}" r="{POT2_DIAMETER / 2.0:.3f}"/>')

    # Push Button SW2
    svg.append(f'    <!-- SW2 Highly KS01-BL-13 Button (D={SW2_DIAMETER}mm) -->')
    svg.append(f'    <circle class="hole-line" cx="{sw2_x:.3f}" cy="{sw2_y:.3f}" r="{SW2_DIAMETER / 2.0:.3f}"/>')

    # Case Flange Mounting Holes (in top and bottom 6mm overhangs)
    svg.append('    <!-- 4x Chassis Mounting Holes in Flanges (D=3.0mm for M2.5/M3) -->')
    for fx, fy in FLANGE_MOUNTING_HOLES:
        svg.append(f'    <circle class="hole-line" cx="{fx:.3f}" cy="{fy:.3f}" r="{FLANGE_HOLE_DIAMETER / 2.0:.3f}"/>')

    svg.append('  </g>')

    # 5. Matrix Display Cutout
    win_x = matrix_cx - (MATRIX_WINDOW_W / 2.0)
    win_y = matrix_cy - (MATRIX_WINDOW_H / 2.0)

    if matrix_mode == "window":
        svg.append('\n  <!-- LAYER 5: MATRIX DISPLAY WINDOW CUTOUT -->')
        svg.append('  <g id="layer-matrix-window" inkscape:label="Matrix Window Cutout" inkscape:groupmode="layer">')
        svg.append(f'    <!-- 5x4 Matrix Bezel Window ({MATRIX_WINDOW_W}x{MATRIX_WINDOW_H}mm, R={MATRIX_WINDOW_R}mm) -->')
        svg.append(f'    <rect class="cut-line" x="{win_x:.3f}" y="{win_y:.3f}" width="{MATRIX_WINDOW_W:.3f}" height="{MATRIX_WINDOW_H:.3f}" rx="{MATRIX_WINDOW_R:.3f}" ry="{MATRIX_WINDOW_R:.3f}"/>')
        svg.append('  </g>')
    else:
        svg.append('\n  <!-- LAYER 5: MATRIX DISCRETE LED CUTOUTS (20 Holes) -->')
        svg.append('  <g id="layer-matrix-discrete-leds" inkscape:label="Matrix Discrete LED Holes" inkscape:groupmode="layer">')
        for r_idx, y_val_pcb in enumerate(MATRIX_ROWS_PCB):
            y_val = y_val_pcb + OVERHANG_Y
            for c_idx, x_val_pcb in enumerate(MATRIX_COLS_PCB):
                x_val = x_val_pcb + OVERHANG_X
                svg.append(f'    <circle class="hole-line" cx="{x_val:.3f}" cy="{y_val:.3f}" r="{LED_HOLE_DIAMETER / 2.0:.3f}"/>')
        svg.append('  </g>')

    svg.append('</svg>\n')
    return "\n".join(svg)


def main():
    hw_dir = Path(__file__).resolve().parents[1]
    out_dir = hw_dir / "frontplate"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Primary SVG with Window Cutout
    window_svg = build_svg(matrix_mode="window")
    primary_path = out_dir / "ABK-20_frontplate.svg"
    primary_path.write_text(window_svg, encoding="utf-8")
    print(f"Wrote {primary_path.name} in {out_dir.name}/ ({WIDTH}x{HEIGHT}mm, Window style)")

    # 2. Variant SVG with Discrete LED Holes
    discrete_svg = build_svg(matrix_mode="discrete")
    discrete_path = out_dir / "ABK-20_frontplate_discrete_leds.svg"
    discrete_path.write_text(discrete_svg, encoding="utf-8")
    print(f"Wrote {discrete_path.name} in {out_dir.name}/ ({WIDTH}x{HEIGHT}mm, 20 Discrete holes)")


if __name__ == "__main__":
    main()

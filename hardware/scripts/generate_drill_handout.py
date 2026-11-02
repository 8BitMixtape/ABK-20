#!/usr/bin/env python3
"""
generate_drill_handout.py
=========================
Generates a printable, authoritative DIY PCB Drilling Map and Handout
for the ABK-20 Rev 0.3 synthesizer, calibrated specifically for standard A4 landscape.

Hole positions are extracted directly from KiCad's official Excellon DRL engine
to ensure 100% geometric accuracy with zero flipped footprints or distorted pin axes.
"""

import os
import subprocess
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

def get_kicad_drl_holes(pcb_path):
    tmp_dir = '/tmp/kicad_drill_handout_export'
    os.makedirs(tmp_dir, exist_ok=True)
    subprocess.run([
        'kicad-cli', 'pcb', 'export', 'drill',
        '-u', 'mm',
        '-o', tmp_dir,
        pcb_path
    ], check=True, stdout=subprocess.DEVNULL)

    drl_path = os.path.join(tmp_dir, 'ABK-20.drl')
    with open(drl_path) as f:
        lines = f.readlines()

    tool_map = {}
    current_tool = None
    holes = []

    for line in lines:
        line = line.strip()
        if line.startswith('T') and 'C' in line:
            parts = line.split('C')
            tool_map[parts[0]] = float(parts[1])
        elif line.startswith('T') and line in tool_map:
            current_tool = line
        elif line.startswith('X') and 'Y' in line:
            m = re.match(r'X([-+]?\d*\.?\d+)Y([-+]?\d*\.?\d+)', line)
            if m and current_tool:
                x = float(m.group(1))
                y = -float(m.group(2))
                holes.append({'x': x, 'y': y, 'drill': tool_map[current_tool]})

    return holes

def generate_handout(pcb_path, output_png, output_pdf):
    holes = get_kicad_drl_holes(pcb_path)
    
    # Board dimensions from KiCad PCB Edge.Cuts
    min_x, max_x = 77.21, 152.21
    min_y, max_y = 28.66, 108.66
    bw = max_x - min_x  # 75.0 mm
    bh = max_y - min_y  # 80.0 mm

    # Standard A4 Landscape: 297 mm x 210 mm = 11.69291 x 8.26772 inches
    fig = plt.figure(figsize=(11.69291, 8.26772), facecolor='#ffffff')

    # Top Header Banner - with generous safe margins (0.05 left/right, 0.90 to 0.97 top)
    ax_hdr = fig.add_axes([0.05, 0.90, 0.90, 0.08])
    ax_hdr.axis('off')
    ax_hdr.text(0.0, 0.70, "ABK-20 DIY PCB DRILLING HANDOUT & PIN HOLE MAP",
                color='#1f2328', fontsize=14.0, weight='bold', fontfamily='sans-serif')
    ax_hdr.text(0.0, 0.22, "Hardware Rev 0.3 • Authoritative KiCad DRL Engine • 86 Holes Total • 4 Carbide Bit Sizes • A4 Landscape",
                color='#57606a', fontsize=8.0, fontfamily='sans-serif')
    ax_hdr.plot([0.0, 1.0], [0.0, 0.0], color='#d0d7de', lw=1.0)

    # Left: Main PCB Drilling Map
    # Placed with safe margin: left=0.05 (15 mm from paper edge), width=0.58, height=0.82
    ax_map = fig.add_axes([0.05, 0.05, 0.58, 0.82])
    ax_map.set_facecolor('#ffffff')
    ax_map.set_aspect('equal')
    ax_map.invert_yaxis()
    ax_map.axis('off')

    # Right: Checklist & Instructions Table
    # Placed at left=0.65, width=0.30 (stops at 0.95 = 15 mm from right paper edge)
    ax_side = fig.add_axes([0.65, 0.05, 0.30, 0.82])
    ax_side.set_facecolor('#ffffff')
    ax_side.axis('off')

    # Color palette by bit size
    color_08 = '#1a7f37'  # Green: Ø 0.8 mm
    color_10 = '#b45309'  # Amber / Warm Gold: Ø 1.0 mm
    color_12 = '#0969da'  # Blue: Ø 1.2–1.3 mm
    color_76 = '#8250df'  # Purple: Ø 1.5–8.0 mm (Large switch holes)

    def get_color(d):
        if d <= 0.9: return color_08
        elif d <= 1.05: return color_10
        elif d <= 2.2: return color_12
        else: return color_76

    # Coordinate extents: exactly spans callouts with breathing room
    ax_map.set_xlim(40.0, 186.0)
    ax_map.set_ylim(128.0, 10.0)

    # Board background
    board_rect = FancyBboxPatch((min_x, min_y), bw, bh,
                                boxstyle="round,pad=0,rounding_size=2",
                                facecolor='#f6f8fa', edgecolor='#1f2328', linewidth=1.8)
    ax_map.add_patch(board_rect)
    
    # Scale markers
    ax_map.text(min_x + bw/2, min_y - 3.5, "<--- 75.0 mm --->", color='#656d76', fontsize=7.5, ha='center', va='bottom', weight='bold')
    ax_map.text(min_x - 3.0, min_y + bh/2, "^ 80.0 mm v", color='#656d76', fontsize=7.5, ha='right', va='center', rotation=90, weight='bold')
    ax_map.text(min_x + bw/2, max_y + 4.0, "[ FRONT VIEW / TOP COMPONENT SIDE ]", color='#1f2328', fontsize=8.0, ha='center', va='top', weight='bold')

    # Draw all 86 holes directly from KiCad DRL coordinates
    for h in holes:
        d = h['drill']
        c = get_color(d)
        r = max(d / 2.0, 0.70)
        ax_map.add_patch(Circle((h['x'], h['y']), r, facecolor=c, edgecolor='#1f2328', linewidth=0.6, alpha=0.9))
        ax_map.add_patch(Circle((h['x'], h['y']), 0.22, facecolor='#ffffff', edgecolor='none'))

    # Helper for clear callout arrows with tight bounding boxes
    def add_callout(text, target_xy, text_xy, color, align='left', rad=-0.08):
        ax_map.annotate(
            text,
            xy=target_xy,
            xytext=text_xy,
            arrowprops=dict(
                arrowstyle="->,head_width=0.22,head_length=0.35",
                color=color,
                lw=1.1,
                shrinkA=2,
                shrinkB=2,
                connectionstyle=f"arc3,rad={rad}"
            ),
            fontsize=6.5,
            weight='bold',
            fontfamily='sans-serif',
            color='#1f2328',
            ha=align,
            va='center',
            bbox=dict(boxstyle="round,pad=0.22", facecolor='#ffffff', edgecolor=color, lw=1.1, alpha=0.96)
        )

    # -------------------------------------------------------------
    # Left Callouts: X=46.0 (align='left', spans X=46 to ~72)
    # -------------------------------------------------------------
    # 1. Jack1 (Audio In) - Top Left
    add_callout("Jack1 (Audio In)\n5x Ø 1.2 mm (Pins)\n2x Ø 1.3 mm (Pegs)",
                (84.61, 31.90), (46.0, 24.0), color_12, 'left')

    # 2. Vias 1, 2, 3 (GND, VCC, DIN) - Above U1
    add_callout("VIAS 1, 2, 3 (GND/VCC/DIN)\n3x Ø 0.8 mm Holes\n[Solder wire both sides!]",
                (89.31, 44.42), (46.0, 43.0), color_08, 'left')

    # 3. U1 (ATtiny85 Socket) - Left Middle
    add_callout("U1 (ATtiny85 DIP-8)\n8x Ø 0.8 mm Holes\n[Pins 1–4 left, 5–8 right]",
                (80.90, 58.30), (46.0, 60.0), color_08, 'left')

    # 4. J1 Header (1x04) - Bottom Left
    add_callout("J1 Header\n4x Ø 1.0 mm Holes\n[P0 to P3]",
                (82.02, 101.3), (46.0, 99.0), color_10, 'left')

    # -------------------------------------------------------------
    # Top & Center Callouts
    # -------------------------------------------------------------
    # 5. SW1 (Power Switch) - Top Center
    add_callout("SW1 Power Switch\n1x Ø 7.6 mm (Center)\n2x Ø 1.5–2.0 mm (Legs)",
                (99.99, 34.39), (99.99, 16.0), color_76, 'center')

    # 6. J5 (USB-C Shield Tabs) - Top Center
    add_callout("J5 USB-C Tabs\n4x Ø 1.0 mm Tabs",
                (114.37, 32.51), (114.37, 45.0), color_10, 'center')

    # 7. Speaker Acoustic Sound Grill - Center
    add_callout("Speaker Sound Grill\n19x Ø 0.8 mm Holes\n[Under chimney]",
                (114.81, 81.51), (114.81, 68.0), color_08, 'center')

    # -------------------------------------------------------------
    # Bottom Callouts
    # -------------------------------------------------------------
    # 8. SW3 (SPDT Toggle Switch) - Bottom Left Center
    add_callout("SW3 Toggle Switch\n3x Ø 1.1 mm (Vertical)",
                (91.77, 93.83), (87.0, 118.0), color_12, 'center')

    # 9. POT2-CV1 (Rotary Pot) - Bottom Center
    add_callout("POT2-CV1 Rotary Pot\n3x Ø 1.0 mm (Signal)\n2x Ø 1.2 mm (Tabs)",
                (114.69, 100.97), (114.69, 118.0), color_10, 'center')

    # 10. SW2 (Pushbutton KS01) - Bottom Right
    add_callout("SW2 Pushbutton\n4x Ø 1.1 mm (Switch)\n2x Ø 1.1 mm (LED)",
                (136.88, 93.75), (142.0, 118.0), color_12, 'center')

    # -------------------------------------------------------------
    # Right Callouts: X=158.0 (align='left', spans X=158 to ~183)
    # -------------------------------------------------------------
    # 11. Jack2 (Audio Out) - Top Right
    add_callout("Jack2 (Audio Out)\n5x Ø 1.2 mm (Pins)\n2x Ø 1.3 mm (Pegs)",
                (144.73, 31.88), (158.0, 24.0), color_12, 'left')

    # 12. Vias 4 & 5 (GNDA Analog Audio Ground) - Right Top
    add_callout("VIA 4 & 5 (GNDA)\n2x Ø 0.8–0.9 mm\n[Audio ground ties]",
                (134.75, 39.07), (158.0, 40.0), color_08, 'left')

    # 13. POT3-Vol1 (Thumbwheel Pot) - Right Middle
    add_callout("POT3 Thumbwheel\n3x Ø 1.0 mm (Pins)\n2x Ø 1.4 mm (Tabs)",
                (147.93, 59.77), (158.0, 56.0), color_10, 'left')

    # 14. RV1 (Bourns Slide Pot PTL20) - Right Edge
    add_callout("RV1 Slide Pot (PTL20)\n5x Ø 1.2 mm (Pins)\n1x Ø 1.2 mm (Peg)",
                (143.77, 59.88), (158.0, 75.0), color_12, 'left')

    # 15. J2 Header (1x04) - Bottom Right
    add_callout("J2 Header\n4x Ø 1.0 mm Holes\n[P4 to P7]",
                (148.11, 101.4), (158.0, 99.0), color_10, 'left')

    # -------------------------------------------------------------
    # Right Side: Workshop Table & Drilling Checklist
    # -------------------------------------------------------------
    card = FancyBboxPatch((0.01, 0.01), 0.98, 0.98, boxstyle="round,pad=0,rounding_size=0.02",
                          facecolor='#f6f8fa', edgecolor='#d0d7de', linewidth=1.2)
    ax_side.add_patch(card)

    ty = 0.95
    ax_side.text(0.06, ty, "DRILL BIT SELECTION & CHECKLIST", color='#1f2328', fontsize=10.0, weight='bold')
    ty -= 0.032
    ax_side.text(0.06, ty, "Work from smallest to largest • 86 Holes Total", color='#57606a', fontsize=7.2)

    ty -= 0.045
    # Step 1: 0.8 mm
    box1 = FancyBboxPatch((0.05, ty - 0.145), 0.90, 0.155, boxstyle="round,pad=0,rounding_size=0.015",
                          facecolor='#ffffff', edgecolor=color_08, linewidth=1.3)
    ax_side.add_patch(box1)
    ax_side.text(0.08, ty - 0.025, "[ ] STEP 1: Ø 0.8 mm BIT (32 Holes)", color=color_08, fontsize=8.0, weight='bold')
    ax_side.text(0.08, ty - 0.060, "• 19x Speaker Sound Grill (Acoustic center)\n"
                                  "•  8x U1 ATtiny85 IC Socket (Pins 1–8)\n"
                                  "•  5x Dedicated Vias (VIA 1, 2, 3, 4, 5)",
                 color='#24292f', fontsize=6.8, va='top')

    ty -= 0.175
    # Step 2: 1.0 mm
    box2 = FancyBboxPatch((0.05, ty - 0.155), 0.90, 0.165, boxstyle="round,pad=0,rounding_size=0.015",
                          facecolor='#ffffff', edgecolor=color_10, linewidth=1.3)
    ax_side.add_patch(box2)
    ax_side.text(0.08, ty - 0.025, "[ ] STEP 2: Ø 1.0 mm BIT (18 Holes)", color=color_10, fontsize=8.0, weight='bold')
    ax_side.text(0.08, ty - 0.060, "•  4x J1 Pin Socket Header (1x04)\n"
                                  "•  4x J2 Pin Socket Header (1x04)\n"
                                  "•  3x POT2-CV1 Rotary Pot (Signal pins)\n"
                                  "•  3x POT3-Vol1 Thumbwheel (Signal pins)\n"
                                  "•  4x J5 USB-C Mechanical Shield Tabs",
                 color='#24292f', fontsize=6.8, va='top')

    ty -= 0.185
    # Step 3: 1.2 - 1.3 mm
    box3 = FancyBboxPatch((0.05, ty - 0.170), 0.90, 0.180, boxstyle="round,pad=0,rounding_size=0.015",
                          facecolor='#ffffff', edgecolor=color_12, linewidth=1.3)
    ax_side.add_patch(box3)
    ax_side.text(0.08, ty - 0.025, "[ ] STEP 3: Ø 1.2–1.3 mm BIT (33 Holes)", color=color_12, fontsize=8.0, weight='bold')
    ax_side.text(0.08, ty - 0.060, "•  7x Jack1 (5 pins + 2 plastic pegs)\n"
                                  "•  7x Jack2 (5 pins + 2 plastic pegs)\n"
                                  "•  6x RV1 Slide Pot (5 pins + 1 peg)\n"
                                  "•  6x SW2 Pushbutton KS01 (4 sw + 2 LED)\n"
                                  "•  3x SW3 SPDT Sub-mini Toggle\n"
                                  "•  4x Pot Side Bracket Tabs (POT2/POT3)",
                 color='#24292f', fontsize=6.8, va='top')

    ty -= 0.200
    # Step 4: Large Switch Holes
    box4 = FancyBboxPatch((0.05, ty - 0.115), 0.90, 0.125, boxstyle="round,pad=0,rounding_size=0.015",
                          facecolor='#ffffff', edgecolor=color_76, linewidth=1.3)
    ax_side.add_patch(box4)
    ax_side.text(0.08, ty - 0.025, "[ ] STEP 4: LARGE HOLES (SW1 Switch)", color=color_76, fontsize=8.0, weight='bold')
    ax_side.text(0.08, ty - 0.055, "•  2x Ø 1.5–2.0 mm: SW1 power switch legs\n"
                                  "•  1x Ø 7.5–8.0 mm: SW1 center button hole\n"
                                  "   (Use step drill bit or round needle file)",
                 color='#24292f', fontsize=6.8, va='top')

    ty -= 0.145
    # Practical Tips Box
    box_tips = FancyBboxPatch((0.05, 0.03), 0.90, ty - 0.02, boxstyle="round,pad=0,rounding_size=0.015",
                              facecolor='#ddf4ff', edgecolor='#54aeff', linewidth=1.0)
    ax_side.add_patch(box_tips)
    ax_side.text(0.08, ty - 0.022, "DIY DRILLING SAFETY & WORKSHOP TIPS", color='#0969da', fontsize=7.5, weight='bold')
    ax_side.text(0.08, ty - 0.050, "1. Backing Board: Clamp flat scrap wood underneath\n"
                                   "   to prevent copper delamination on exit.\n"
                                   "2. High RPM / Low Pressure: Carbide micro-bits are brittle!\n"
                                   "   Drill at 10,000+ RPM straight down with zero lateral tilt.\n"
                                   "3. Pilot Centers: Your mask etched copper pilot marks,\n"
                                   "   so 0.8 mm self-centers without bit wandering.\n"
                                   "4. Bottom Side Drilling: If drilling from copper back,\n"
                                   "   flip left-to-right (Jack1 is right, Jack2 is left).",
                 color='#1f2328', fontsize=6.5, va='top')

    # Save PNG at 300 DPI
    plt.savefig(output_png, dpi=300, facecolor='#ffffff')
    
    # Save PDF directly formatted to true A4 page dimensions (841.89 x 595.28 pt)
    plt.savefig(output_pdf, facecolor='#ffffff', format='pdf')
    plt.close()
    print(f"[+] Successfully generated drill handout image: {output_png}")
    print(f"[+] Successfully generated drill handout PDF:   {output_pdf}")

if __name__ == '__main__':
    pcb = 'hardware/ABK-20.kicad_pcb'
    out_png = 'docs/img/ABK-20_diy_drill_handout.png'
    out_pdf = 'docs/fabrication/ABK-20_DIY_DRILL_HANDOUT.pdf'
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    os.makedirs(os.path.dirname(out_pdf), exist_ok=True)
    generate_handout(pcb, out_png, out_pdf)

#!/usr/bin/env python3
"""
generate_diy_wiring_guide.py
============================
Generates a visual diagram for DIY etching of the ABK-20 PCB without plated through-holes.
Highlights:
- 5 dedicated via wire bridges with color-coded targets and coordinates
- Component solder-side guide (F.Cu vs B.Cu)
- Multimeter continuity check probe points
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle

def create_guide_graphic(output_path):
    min_x, max_x = 77.21, 152.21
    min_y, max_y = 28.66, 108.66
    bw = max_x - min_x  # 75 mm
    bh = max_y - min_y  # 80 mm

    fig = plt.figure(figsize=(20, 11.5), facecolor='#0d1117')
    
    ax_title = fig.add_axes([0.05, 0.91, 0.90, 0.08])
    ax_title.axis('off')
    ax_title.text(0.5, 0.65, "ABK-20 DIY ETCHING: GND & VIA WIRE BRIDGE GUIDE",
                  color='#58a6ff', fontsize=20, weight='bold', ha='center', va='center', fontfamily='monospace')
    ax_title.text(0.5, 0.15, "Non-Plated Through-Hole (PTH) Assembly - 5 Dedicated Wire Bridges - Solder-Side Mapping",
                  color='#8b949e', fontsize=12, ha='center', va='center', fontfamily='monospace')

    ax_left = fig.add_axes([0.04, 0.28, 0.44, 0.61])
    ax_right = fig.add_axes([0.52, 0.28, 0.44, 0.61])
    ax_info = fig.add_axes([0.04, 0.03, 0.92, 0.22])

    for ax in [ax_left, ax_right]:
        ax.set_facecolor('#0d1117')
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.axis('off')

    via_colors = {
        1: '#00f0ff',  # Cyan: Master GND
        2: '#ff3366',  # Red/Pink: Master VCC
        3: '#ffaa00',  # Amber: NEO1-DIN
        4: '#bc8cff',  # Purple: GNDA Audio Amp
        5: '#bc8cff',  # Purple: GNDA Vol Pot
    }

    vias = [
        {'id': 1, 'x': 86.82, 'y': 44.45, 'name': 'GND Bridge', 'net': 'GND (Digital)', 'desc': 'Master top-to-bottom ground plane tie'},
        {'id': 2, 'x': 91.88, 'y': 44.50, 'name': 'VCC Bridge', 'net': 'VCC (+5V)', 'desc': 'Master +5V power to ATtiny & NeoPixels'},
        {'id': 3, 'x': 89.31, 'y': 44.42, 'name': 'DIN Bridge', 'net': 'NEO1-DIN', 'desc': 'PB0 data line to 1st NeoPixel'},
        {'id': 4, 'x': 134.75, 'y': 39.07, 'name': 'GNDA Bridge', 'net': 'GNDA (Audio)', 'desc': 'Analog ground return for PAM8002 amp'},
        {'id': 5, 'x': 143.29, 'y': 63.08, 'name': 'GNDA Vol', 'net': 'GNDA (Audio)', 'desc': 'Ground tie for thumbwheel volume pot'},
    ]

    # Draw Left: FRONT SIDE
    ax_left.set_xlim(min_x - 14, max_x + 14)
    ax_left.set_ylim(max_y + 8, min_y - 12)
    
    rect_f = FancyBboxPatch((min_x, min_y), bw, bh,
                            boxstyle="round,pad=0,rounding_size=2",
                            facecolor='#16201b', edgecolor='#3fb950', linewidth=2.0)
    ax_left.add_patch(rect_f)
    ax_left.text(min_x + bw/2, min_y - 6, "FRONT SIDE (F.Cu) — Top View",
                 color='#3fb950', fontsize=14, weight='bold', ha='center', va='center', fontfamily='monospace')

    # Draw 5x4 NeoPixel Matrix on Front
    neo_xs = [97.09, 106.01, 114.94, 123.86, 132.78]
    neo_ys = [46.86, 54.82, 62.78, 70.74]
    for xi, x in enumerate(neo_xs):
        for yi, y in enumerate(neo_ys):
            neo_rect = FancyBboxPatch((x - 2.4, y - 2.4), 4.8, 4.8,
                                      boxstyle="round,pad=0,rounding_size=0.6",
                                      facecolor='#26382c', edgecolor='#56d364', linewidth=1.0)
            ax_left.add_patch(neo_rect)
            circ = Circle((x, y), 1.3, facecolor='#2ea043', edgecolor='#7ee787', linewidth=0.8)
            ax_left.add_patch(circ)
    ax_left.text(114.94, 76.5, "5x4 NeoPixel Matrix (20 LEDs)\n[SMD on F.Cu: All return via Via 1!]",
                 color='#7ee787', fontsize=8, ha='center', va='top', fontfamily='monospace')

    # ATtiny85 Socket (U1)
    u1_rect = FancyBboxPatch((80.90 - 4.5, 54.51 - 2.0), 9.0, 11.5,
                             boxstyle="round,pad=0,rounding_size=1.0",
                             facecolor='#21262d', edgecolor='#8b949e', linewidth=1.2)
    ax_left.add_patch(u1_rect)
    ax_left.text(80.90, 54.51 + 3.75, "U1\nATtiny85\n(DIP-8)", color='#f0f6fc', fontsize=8, weight='bold', ha='center', va='center', fontfamily='monospace')
    ax_left.text(80.90, 67.5, "[Solder on Bottom!]", color='#f85149', fontsize=7.5, ha='center', va='top', fontfamily='monospace')

    # Bourns Slide Pot (RV1)
    rv1_rect = FancyBboxPatch((143.77 - 4.0, 44.88 - 3.0), 8.0, 33.0,
                              boxstyle="round,pad=0,rounding_size=1.2",
                              facecolor='#21262d', edgecolor='#8b949e', linewidth=1.2)
    ax_left.add_patch(rv1_rect)
    ax_left.text(143.77, 60.0, "RV1\nSlide\nPot\nPTL20", color='#f0f6fc', fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace')
    ax_left.text(143.77, 78.5, "[Solder\non Bottom!]", color='#f85149', fontsize=7, ha='center', va='top', fontfamily='monospace')

    # Rotary Pot (POT2-CV1)
    pot2_circ = Circle((114.68, 93.47), 5.5, facecolor='#21262d', edgecolor='#8b949e', linewidth=1.2)
    ax_left.add_patch(pot2_circ)
    ax_left.text(114.68, 93.47, "POT2\nCV1", color='#f0f6fc', fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace')

    # Pushbutton SW2 & Toggle SW3
    sw2_rect = FancyBboxPatch((136.88 - 3.5, 93.75 - 3.5), 7.0, 7.0, boxstyle="round,pad=0,rounding_size=1.0", facecolor='#21262d', edgecolor='#8b949e', linewidth=1.0)
    ax_left.add_patch(sw2_rect)
    ax_left.text(136.88, 93.75, "SW2", color='#f0f6fc', fontsize=8, weight='bold', ha='center', va='center', fontfamily='monospace')
    
    sw3_rect = FancyBboxPatch((91.41 - 3.0, 93.83 - 4.0), 6.0, 8.0, boxstyle="round,pad=0,rounding_size=1.0", facecolor='#21262d', edgecolor='#8b949e', linewidth=1.0)
    ax_left.add_patch(sw3_rect)
    ax_left.text(91.41, 93.83, "SW3", color='#f0f6fc', fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace')

    # Pin headers J1 & J2
    j1_rect = FancyBboxPatch((82.02 - 1.5, 97.51 - 5.0), 3.0, 10.0, facecolor='#21262d', edgecolor='#8b949e', linewidth=1.0)
    ax_left.add_patch(j1_rect)
    ax_left.text(82.02 - 4.0, 97.51, "J1", color='#8b949e', fontsize=8, ha='right', va='center', fontfamily='monospace')
    
    j2_rect = FancyBboxPatch((148.11 - 1.5, 100.21 - 5.0), 3.0, 10.0, facecolor='#21262d', edgecolor='#8b949e', linewidth=1.0)
    ax_left.add_patch(j2_rect)
    ax_left.text(148.11 + 4.0, 100.21, "J2", color='#8b949e', fontsize=8, ha='left', va='center', fontfamily='monospace')

    # Jacks and USB-C poking through to Front!
    j1_pin = Circle((84.61, 31.90), 2.2, facecolor='#1f6feb', edgecolor='#58a6ff', linewidth=1.5)
    ax_left.add_patch(j1_pin)
    ax_left.text(84.61, 26.0, "Jack1 (Audio In)\n* Solder Pin on Front!", color='#58a6ff', fontsize=7.5, weight='bold', ha='center', va='bottom', fontfamily='monospace')

    j2_pin = Circle((144.73, 31.88), 2.2, facecolor='#bc8cff', edgecolor='#d2a8ff', linewidth=1.5)
    ax_left.add_patch(j2_pin)
    ax_left.text(144.73, 26.0, "Jack2 (Audio Out)\n* Solder Pin on Front!", color='#d2a8ff', fontsize=7.5, weight='bold', ha='center', va='bottom', fontfamily='monospace')

    # USB-C Shield Tabs
    for sx, sy in [(110.05, 30.61), (110.05, 34.41), (118.69, 30.61), (118.69, 34.41)]:
        tab = Circle((sx, sy), 1.0, facecolor='#00f0ff', edgecolor='#ffffff', linewidth=1.0)
        ax_left.add_patch(tab)
    ax_left.text(114.37, 26.0, "J5 USB-C 4x Tabs\n* Solder on Front!", color='#00f0ff', fontsize=7.5, weight='bold', ha='center', va='bottom', fontfamily='monospace')

    # Draw the 5 Vias on Front
    for v in vias:
        col = via_colors[v['id']]
        ax_left.add_patch(Circle((v['x'], v['y']), 2.0, facecolor='#0d1117', edgecolor=col, linewidth=2.0))
        ax_left.add_patch(Circle((v['x'], v['y']), 0.9, facecolor=col, edgecolor='#ffffff', linewidth=0.5))
        offset_x = 0
        offset_y = -4.5 if v['id'] in [1, 2, 3] else (4.5 if v['id'] == 4 else -4.5)
        if v['id'] == 1: offset_x = -5.0
        elif v['id'] == 2: offset_x = 5.0
        elif v['id'] == 3: offset_x = 0.0
        ax_left.text(v['x'] + offset_x, v['y'] + offset_y, f"VIA {v['id']}\n{v['name']}",
                     color=col, fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace',
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='#0d1117', edgecolor=col, alpha=0.9))

    # -------------------------------------------------------------
    # Draw Right: BACK SIDE (B.Cu) — Physically Mirrored (X' = 229.42 - X)
    # -------------------------------------------------------------
    def mir(x): return 229.42 - x

    ax_right.set_xlim(mir(max_x) - 14, mir(min_x) + 14)
    ax_right.set_ylim(max_y + 8, min_y - 12)

    rect_b = FancyBboxPatch((mir(max_x), min_y), bw, bh,
                            boxstyle="round,pad=0,rounding_size=2",
                            facecolor='#131d2a', edgecolor='#1f6feb', linewidth=2.0)
    ax_right.add_patch(rect_b)
    ax_right.text(mir(min_x + bw/2), min_y - 6, "BACK SIDE (B.Cu) — Physical View Looking at Bottom",
                 color='#58a6ff', fontsize=14, weight='bold', ha='center', va='center', fontfamily='monospace')

    # Battery Connector (J4)
    j4_rect = FancyBboxPatch((mir(96.24) - 4.0, 51.13 - 3.5), 8.0, 7.0, boxstyle="round,pad=0,rounding_size=1.0", facecolor='#21262d', edgecolor='#f0883e', linewidth=1.5)
    ax_right.add_patch(j4_rect)
    ax_right.text(mir(96.24), 51.13, "J4\nBATTERY\n[SMD B.Cu]", color='#f0883e', fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace')

    # USB-C (J5)
    j5_rect = FancyBboxPatch((mir(114.37) - 5.5, 31.41 - 4.5), 11.0, 9.0, boxstyle="round,pad=0,rounding_size=1.2", facecolor='#21262d', edgecolor='#58a6ff', linewidth=1.5)
    ax_right.add_patch(j5_rect)
    ax_right.text(mir(114.37), 31.41, "J5\nUSB-C\n[B.Cu]", color='#58a6ff', fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace')

    # Regulator (U3 - TO-252)
    u3_rect = FancyBboxPatch((mir(116.31) - 4.0, 44.16 - 4.0), 8.0, 8.0, boxstyle="round,pad=0,rounding_size=1.0", facecolor='#21262d', edgecolor='#d29922', linewidth=1.2)
    ax_right.add_patch(u3_rect)
    ax_right.text(mir(116.31), 44.16, "U3\nLM1117\n[B.Cu]", color='#d29922', fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace')

    # Audio Amp (U2 - PAM8002)
    u2_rect = FancyBboxPatch((mir(128.40) - 3.5, 47.19 - 3.0), 7.0, 6.0, boxstyle="round,pad=0,rounding_size=0.8", facecolor='#21262d', edgecolor='#bc8cff', linewidth=1.2)
    ax_right.add_patch(u2_rect)
    ax_right.text(mir(128.40), 47.19, "U2\nPAM8002\n[B.Cu]", color='#bc8cff', fontsize=7, weight='bold', ha='center', va='center', fontfamily='monospace')

    # Star Ground Tie (NT1)
    nt1_rect = FancyBboxPatch((mir(122.10) - 2.5, 32.84 - 1.5), 5.0, 3.0, boxstyle="round,pad=0,rounding_size=0.5", facecolor='#1f6feb', edgecolor='#bc8cff', linewidth=1.5)
    ax_right.add_patch(nt1_rect)
    ax_right.text(mir(122.10), 38.0, "NT1\nStar Ground", color='#bc8cff', fontsize=7.5, weight='bold', ha='center', va='top', fontfamily='monospace')

    # Volume Thumbwheel Pot (POT3-Vol1)
    pot3_rect = FancyBboxPatch((mir(147.93) - 3.0, 59.77 - 8.0), 6.0, 16.0, boxstyle="round,pad=0,rounding_size=1.5", facecolor='#21262d', edgecolor='#bc8cff', linewidth=1.2)
    ax_right.add_patch(pot3_rect)
    ax_right.text(mir(147.93), 59.77, "POT3\nVol\nWheel", color='#bc8cff', fontsize=7, weight='bold', ha='center', va='center', fontfamily='monospace')

    # Jack Bodies on Back (Jack1, Jack2)
    j1_back = FancyBboxPatch((mir(84.61) - 6.0, 31.90 - 6.0), 12.0, 12.0, facecolor='#21262d', edgecolor='#30363d', linewidth=1.2)
    ax_right.add_patch(j1_back)
    ax_right.text(mir(84.61), 31.90, "Jack1 Body\n[B.Cu]", color='#8b949e', fontsize=7.5, ha='center', va='center', fontfamily='monospace')
    
    j2_back = FancyBboxPatch((mir(144.73) - 6.0, 31.88 - 6.0), 12.0, 12.0, facecolor='#21262d', edgecolor='#30363d', linewidth=1.2)
    ax_right.add_patch(j2_back)
    ax_right.text(mir(144.73), 31.88, "Jack2 Body\n[B.Cu]", color='#8b949e', fontsize=7.5, ha='center', va='center', fontfamily='monospace')

    # THT Component pins sticking out on Back (Solder here!)
    for py in [50.7, 53.24, 55.78, 58.32]:
        p_left = Circle((mir(80.90 - 3.81), py), 0.8, facecolor='#f85149', edgecolor='#ffffff', linewidth=0.5)
        p_right = Circle((mir(80.90 + 3.81), py), 0.8, facecolor='#f85149', edgecolor='#ffffff', linewidth=0.5)
        ax_right.add_patch(p_left)
        ax_right.add_patch(p_right)
    ax_right.text(mir(80.90), 54.51, "U1 DIP-8 Pins\n* Solder on Bottom!", color='#f85149', fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace')

    for rvy in [44.88, 74.88]:
        rp = Circle((mir(143.77), rvy), 1.0, facecolor='#f85149', edgecolor='#ffffff', linewidth=0.5)
        ax_right.add_patch(rp)
    ax_right.text(mir(143.77), 60.0, "RV1 Pins\n* Solder Bottom!", color='#f85149', fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace')

    # Draw the 5 Vias on Back (Mirrored X)
    for v in vias:
        mx = mir(v['x'])
        col = via_colors[v['id']]
        ax_right.add_patch(Circle((mx, v['y']), 2.0, facecolor='#0d1117', edgecolor=col, linewidth=2.0))
        ax_right.add_patch(Circle((mx, v['y']), 0.9, facecolor=col, edgecolor='#ffffff', linewidth=0.5))
        offset_x = 0
        offset_y = -4.5 if v['id'] in [1, 2, 3] else (4.5 if v['id'] == 4 else -4.5)
        if v['id'] == 1: offset_x = 5.0
        elif v['id'] == 2: offset_x = -5.0
        elif v['id'] == 3: offset_x = 0.0
        ax_right.text(mx + offset_x, v['y'] + offset_y, f"VIA {v['id']}\n{v['name']}",
                      color=col, fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace',
                      bbox=dict(boxstyle='round,pad=0.2', facecolor='#0d1117', edgecolor=col, alpha=0.9))

    # -------------------------------------------------------------
    # Bottom Panel: Solder Instructions & Multimeter Continuity Table
    # -------------------------------------------------------------
    ax_info.set_facecolor('#161b22')
    ax_info.axis('off')
    border = FancyBboxPatch((0.005, 0.02), 0.99, 0.96, boxstyle="round,pad=0,rounding_size=0.02",
                            facecolor='#161b22', edgecolor='#30363d', linewidth=1.5)
    ax_info.add_patch(border)

    col1_x = 0.03
    col2_x = 0.36
    col3_x = 0.69

    ax_info.text(col1_x, 0.85, "[1] HOW TO SOLDER THE 5 VIAS", color='#58a6ff', fontsize=11, weight='bold', fontfamily='monospace')
    ax_info.text(col1_x, 0.66, "1. Drill the 5 via holes with DIA 0.8 - 0.9 mm bit.\n"
                               "2. Snip a discarded resistor/diode copper lead.\n"
                               "3. Push wire through hole -> solder on TOP.\n"
                               "4. Flip board -> solder on BOTTOM -> snip flush.\n"
                               "* This creates the permanent top-to-bottom bridge!",
                 color='#c9d1d9', fontsize=8.5, va='top', fontfamily='monospace')

    ax_info.text(col2_x, 0.85, "[2] COMPONENT SOLDER SIDES", color='#3fb950', fontsize=11, weight='bold', fontfamily='monospace')
    ax_info.text(col2_x, 0.66, "- Front Parts (U1, RV1, SW2, SW3, POT2, J1, J2):\n"
                               "  -> Body sits on Front. Solder pins on BOTTOM ONLY.\n"
                               "  -> Zero tracks are trapped under component bodies!\n"
                               "- Back Parts (Jack1, Jack2, POT3, J5 shield tabs):\n"
                               "  -> Body sits on Back. Solder pins on TOP ONLY.\n"
                               "  -> Soldering J5 4x tabs on top adds heavy GND ties!",
                 color='#c9d1d9', fontsize=8.5, va='top', fontfamily='monospace')

    ax_info.text(col3_x, 0.85, "[3] MULTIMETER CONTINUITY BEEP TEST", color='#e3b341', fontsize=11, weight='bold', fontfamily='monospace')
    ax_info.text(col3_x, 0.66, "Before powering on or inserting ATtiny85:\n"
                               "[✔] TEST 1 (GND): J4 Battery (-) <---> NEO20 Pin 1 (BEEP)\n"
                               "    Verifies Via 1 links bottom power GND to top matrix.\n"
                               "[✔] TEST 2 (VCC): J4 Battery (+) <---> U1 Pin 8 (BEEP with SW1 on)\n"
                               "    Verifies Via 2 links power to MCU & NeoPixels.\n"
                               "[✔] TEST 3 (Star GND): NT1 Pin 1 <---> Jack2 GNDA (BEEP)\n"
                               "    Verifies star ground tie between digital & audio.",
                 color='#c9d1d9', fontsize=8.5, va='top', fontfamily='monospace')

    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='#0d1117')
    plt.close()
    print(f"[+] Successfully generated guide graphic: {output_path}")

if __name__ == '__main__':
    out_dir = 'docs/img'
    os.makedirs(out_dir, exist_ok=True)
    out_png = os.path.join(out_dir, 'ABK-20_diy_ground_and_vias_guide.png')
    create_guide_graphic(out_png)

#!/usr/bin/env python3
"""
generate_diy_wiring_guide.py
============================
Generates a visual diagram for DIY etching of the ABK-20 PCB without plated through-holes.
Highlights:
- Dedicated via wire bridges with color-coded targets and coordinates (dynamically read from PCB)
- Special callout for RV1 Slide Potentiometer Pin 3 GND bridge
- Component solder-side guide (F.Cu vs B.Cu)
- Multimeter continuity check probe points
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle

def load_vias_from_pcb(pcb_path):
    vias = []
    has_pcbnew = False
    try:
        import pcbnew
        board = pcbnew.LoadBoard(pcb_path)
        has_pcbnew = True
        for t in board.GetTracks():
            if t.GetClass() == 'PCB_VIA':
                pos = t.GetPosition()
                vias.append({
                    'x': round(pos.x / 1e6, 2),
                    'y': round(pos.y / 1e6, 2),
                    'net': t.GetNetname(),
                    'drill': round(t.GetDrill() / 1e6, 2)
                })
    except Exception as e:
        print(f"Warning: could not read pcbnew: {e}")

    if not vias:
        # Fallback to current 7 known vias
        vias = [
            {'x': 86.82, 'y': 44.45, 'net': 'GND', 'drill': 0.8},
            {'x': 91.88, 'y': 44.50, 'net': 'VCC', 'drill': 0.8},
            {'x': 89.31, 'y': 44.42, 'net': 'Net-(NEO1-DIN)', 'drill': 0.8},
            {'x': 134.62, 'y': 39.01, 'net': 'GNDA', 'drill': 0.9},
            {'x': 139.09, 'y': 63.88, 'net': 'GNDA', 'drill': 0.9},
            {'x': 124.66, 'y': 96.77, 'net': 'GND', 'drill': 0.9},
            {'x': 143.69, 'y': 96.95, 'net': 'GND', 'drill': 0.9},
        ]
    return vias

def create_guide_graphic(output_path, pcb_path='hardware/ABK-20.kicad_pcb'):
    min_x, max_x = 77.21, 152.21
    min_y, max_y = 28.66, 108.66
    bw = max_x - min_x  # 75 mm
    bh = max_y - min_y  # 80 mm

    fig = plt.figure(figsize=(22, 12.5), facecolor='#0d1117')
    
    raw_vias = load_vias_from_pcb(pcb_path)
    
    # Sort vias in logical reading order (top to bottom)
    raw_vias.sort(key=lambda v: (v['y'], v['x']))
    
    # Check if a via exists near RV1.3 (x in [143..147], y in [73..81])
    rv1_via_present = any(abs(v['x'] - 145.0) < 2.0 and 73.0 <= v['y'] <= 81.0 and 'GND' in v['net'] for v in raw_vias)
    
    total_via_count = len(raw_vias)
    
    ax_title = fig.add_axes([0.04, 0.92, 0.92, 0.07])
    ax_title.axis('off')
    ax_title.text(0.5, 0.65, "ABK-20 DIY ETCHING: GND & VIA WIRE BRIDGE GUIDE",
                  color='#58a6ff', fontsize=20, weight='bold', ha='center', va='center', fontfamily='monospace')
    sub_title = f"Non-Plated Through-Hole (PTH) Assembly — {total_via_count} Active Wire Bridges"
    if not rv1_via_present:
        sub_title += " + 1 RECOMMENDED VIA FOR RV1 PIN 3 (SLIDER GND)"
    sub_title += " — Solder-Side Mapping"
    ax_title.text(0.5, 0.15, sub_title,
                  color='#8b949e' if rv1_via_present else '#f0883e', fontsize=11, ha='center', va='center', fontfamily='monospace')

    ax_left = fig.add_axes([0.03, 0.26, 0.45, 0.64])
    ax_right = fig.add_axes([0.52, 0.26, 0.45, 0.64])
    ax_info = fig.add_axes([0.03, 0.02, 0.94, 0.22])

    for ax in [ax_left, ax_right]:
        ax.set_facecolor('#0d1117')
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.axis('off')

    # Color coding helper
    def get_color(net):
        if 'GNDA' in net: return '#bc8cff'   # Purple
        if 'VCC' in net: return '#ff3366'    # Red
        if 'DIN' in net: return '#ffaa00'    # Amber
        return '#00f0ff'                     # Cyan for Digital GND

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
    ax_left.text(114.94, 76.5, "5x4 NeoPixel Matrix (20 LEDs)\n[SMD on F.Cu: All return to GND via Matrix Via!]",
                 color='#7ee787', fontsize=8, ha='center', va='top', fontfamily='monospace')

    # ATtiny85 Socket (U1)
    u1_rect = FancyBboxPatch((80.90 - 4.5, 54.51 - 2.0), 9.0, 11.5,
                             boxstyle="round,pad=0,rounding_size=1.0",
                             facecolor='#21262d', edgecolor='#8b949e', linewidth=1.2)
    ax_left.add_patch(u1_rect)
    ax_left.text(80.90, 54.51 + 3.75, "U1\nATtiny85\n(DIP-8)", color='#f0f6fc', fontsize=8, weight='bold', ha='center', va='center', fontfamily='monospace')
    # Callout for U1 Pin 1 (Top Solder for Reset)
    ax_left.add_patch(Circle((80.90, 54.51), 1.2, facecolor='#f85149', edgecolor='#ffffff', linewidth=1.0))
    ax_left.text(80.90, 67.5, "[Pin 1: Solder on TOP\nfor SW4 Reset Button!]", color='#f85149', fontsize=7.2, weight='bold', ha='center', va='top', fontfamily='monospace')

    # Bourns Slide Pot (RV1)
    rv1_rect = FancyBboxPatch((143.77 - 4.6, 42.26), 9.2, 35.2,
                              boxstyle="round,pad=0,rounding_size=1.2",
                              facecolor='#21262d', edgecolor='#8b949e', linewidth=1.2)
    ax_left.add_patch(rv1_rect)
    ax_left.text(143.77, 58.0, "RV1\nSlide Pot\n(PTL20)\nFlush Body", color='#f0f6fc', fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace')
    
    # Highlight RV1 Pin 3 (GND) on Front
    p3_x, p3_y = 145.02, 74.88
    ax_left.add_patch(Circle((p3_x, p3_y), 1.3, facecolor='#f85149', edgecolor='#ffffff', linewidth=1.2))
    ax_left.text(p3_x - 1.5, p3_y, "Pin 3\n(GND)", color='#ff7b72', fontsize=7, weight='bold', ha='right', va='center', fontfamily='monospace')

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
    ax_left.text(91.41, 93.83, "SW3\nUP/DN", color='#f0f6fc', fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace')

    # Pin headers J1 & J2
    j1_rect = FancyBboxPatch((82.02 - 1.5, 97.51 - 5.0), 3.0, 10.0, facecolor='#21262d', edgecolor='#8b949e', linewidth=1.0)
    ax_left.add_patch(j1_rect)
    ax_left.text(82.02 - 4.0, 97.51, "J1", color='#8b949e', fontsize=8, ha='right', va='center', fontfamily='monospace')
    
    j2_rect = FancyBboxPatch((148.11 - 1.5, 100.21 - 5.0), 3.0, 10.0, facecolor='#21262d', edgecolor='#8b949e', linewidth=1.0)
    ax_left.add_patch(j2_rect)
    ax_left.text(148.11 + 4.0, 100.21, "J2", color='#8b949e', fontsize=8, ha='left', va='center', fontfamily='monospace')

    # Jacks and USB-C poking through to Front
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

    # Plot Active Vias on Front
    for idx, v in enumerate(raw_vias, 1):
        col = get_color(v['net'])
        ax_left.add_patch(Circle((v['x'], v['y']), 1.8, facecolor='#0d1117', edgecolor=col, linewidth=2.0))
        ax_left.add_patch(Circle((v['x'], v['y']), 0.8, facecolor=col, edgecolor='#ffffff', linewidth=0.5))
        
        # smart offset
        off_x = 0
        off_y = -4.5
        if v['x'] < 90 and v['y'] < 50: off_x = -5.0
        elif v['x'] > 90 and v['y'] < 50: off_x = 5.0
        elif v['y'] > 90: off_y = 4.5
        
        ax_left.text(v['x'] + off_x, v['y'] + off_y, f"VIA {idx}\n({v['net']})",
                     color=col, fontsize=7.0, weight='bold', ha='center', va='center', fontfamily='monospace',
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='#0d1117', edgecolor=col, alpha=0.9))

    # If RV1.3 via is not yet present, plot PROPOSED VIA marker in dashed gold
    if not rv1_via_present:
        prop_x, prop_y = 145.0, 78.5
        ax_left.add_patch(Circle((prop_x, prop_y), 2.2, facecolor='none', edgecolor='#e3b341', linewidth=2.0, linestyle='--'))
        ax_left.add_patch(Circle((prop_x, prop_y), 0.9, facecolor='#e3b341', edgecolor='#ffffff', linewidth=0.5))
        ax_left.text(prop_x + 5.5, prop_y + 2.0, "PROPOSED VIA:\nRV1 Pin 3 (GND)\n(145.0, 78.5)",
                     color='#e3b341', fontsize=7.5, weight='bold', ha='left', va='center', fontfamily='monospace',
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='#0d1117', edgecolor='#e3b341', alpha=0.9))

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
    ax_right.text(mir(84.61), 31.90, "Jack1 Body\n* Solder Pins\non B.Cu!", color='#58a6ff', fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace')
    
    j2_back = FancyBboxPatch((mir(144.73) - 6.0, 31.88 - 6.0), 12.0, 12.0, facecolor='#21262d', edgecolor='#30363d', linewidth=1.2)
    ax_right.add_patch(j2_back)
    ax_right.text(mir(144.73), 31.88, "Jack2 Body\n* Solder Pins\non B.Cu!", color='#d2a8ff', fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace')

    # THT Component pins sticking out on Back (Solder here!)
    for py in [50.7, 53.24, 55.78, 58.32]:
        p_left = Circle((mir(80.90 - 3.81), py), 0.8, facecolor='#f85149', edgecolor='#ffffff', linewidth=0.5)
        p_right = Circle((mir(80.90 + 3.81), py), 0.8, facecolor='#f85149', edgecolor='#ffffff', linewidth=0.5)
        ax_right.add_patch(p_left)
        ax_right.add_patch(p_right)
    ax_right.text(mir(80.90), 54.51, "U1 DIP-8 Pins\n* Solder on Bottom!", color='#f85149', fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace')

    # RV1 Pins on Bottom
    for rvy in [44.88, 74.88]:
        rp = Circle((mir(145.02), rvy), 1.1, facecolor='#f85149', edgecolor='#ffffff', linewidth=0.5)
        ax_right.add_patch(rp)
    ax_right.text(mir(145.02), 60.0, "RV1 Pins\n* Solder Bottom!", color='#f85149', fontsize=7.5, weight='bold', ha='center', va='center', fontfamily='monospace')
    
    # Highlight RV1 Pin 3 (GND) on Back
    ax_right.add_patch(Circle((mir(p3_x), p3_y), 1.5, facecolor='#f85149', edgecolor='#ffffff', linewidth=1.5))
    ax_right.text(mir(p3_x) + 2.0, p3_y, "RV1 Pin 3\n(GND Pin)", color='#ff7b72', fontsize=7, weight='bold', ha='left', va='center', fontfamily='monospace')

    # Draw Active Vias on Back (Mirrored X)
    for idx, v in enumerate(raw_vias, 1):
        mx = mir(v['x'])
        col = get_color(v['net'])
        ax_right.add_patch(Circle((mx, v['y']), 1.8, facecolor='#0d1117', edgecolor=col, linewidth=2.0))
        ax_right.add_patch(Circle((mx, v['y']), 0.8, facecolor=col, edgecolor='#ffffff', linewidth=0.5))
        
        off_x = 0
        off_y = -4.5
        if v['x'] < 90 and v['y'] < 50: off_x = 5.0
        elif v['x'] > 90 and v['y'] < 50: off_x = -5.0
        elif v['y'] > 90: off_y = 4.5
        
        ax_right.text(mx + off_x, v['y'] + off_y, f"VIA {idx}\n({v['net']})",
                      color=col, fontsize=7.0, weight='bold', ha='center', va='center', fontfamily='monospace',
                      bbox=dict(boxstyle='round,pad=0.2', facecolor='#0d1117', edgecolor=col, alpha=0.9))

    # Proposed RV1.3 via on Back
    if not rv1_via_present:
        prop_mx = mir(prop_x)
        ax_right.add_patch(Circle((prop_mx, prop_y), 2.2, facecolor='none', edgecolor='#e3b341', linewidth=2.0, linestyle='--'))
        ax_right.add_patch(Circle((prop_mx, prop_y), 0.9, facecolor='#e3b341', edgecolor='#ffffff', linewidth=0.5))
        ax_right.text(prop_mx - 5.5, prop_y + 2.0, "PROPOSED VIA:\nRV1 Pin 3 (GND)\n(145.0, 78.5)",
                      color='#e3b341', fontsize=7.5, weight='bold', ha='right', va='center', fontfamily='monospace',
                      bbox=dict(boxstyle='round,pad=0.2', facecolor='#0d1117', edgecolor='#e3b341', alpha=0.9))

    # -------------------------------------------------------------
    # Bottom Panel: Solder Instructions & Multimeter Continuity Table
    # -------------------------------------------------------------
    ax_info.set_facecolor('#161b22')
    ax_info.axis('off')
    border = FancyBboxPatch((0.005, 0.02), 0.99, 0.96, boxstyle="round,pad=0,rounding_size=0.02",
                            facecolor='#161b22', edgecolor='#30363d', linewidth=1.5)
    ax_info.add_patch(border)

    col1_x = 0.025
    col2_x = 0.35
    col3_x = 0.68

    ax_info.text(col1_x, 0.86, f"[1] HOW TO SOLDER THE {total_via_count} VIA BRIDGES", color='#58a6ff', fontsize=11, weight='bold', fontfamily='monospace')
    ax_info.text(col1_x, 0.68, "1. Drill the via holes with DIA 0.8 - 0.9 mm bit.\n"
                               "2. Snip a discarded resistor/diode copper lead.\n"
                               "3. Push wire through hole -> solder on TOP.\n"
                               "4. Flip board -> solder on BOTTOM -> snip flush.\n"
                               "* This creates the permanent top-to-bottom bridge!\n"
                               f"⚠️ Note: RV1 Pin 3 (GND) needs a via at (145.0, 78.5) mm!",
                 color='#c9d1d9', fontsize=8.2, va='top', fontfamily='monospace')

    ax_info.text(col2_x, 0.86, "[2] COMPONENT SOLDER SIDES & DUAL-SIDE TIPS", color='#3fb950', fontsize=11, weight='bold', fontfamily='monospace')
    ax_info.text(col2_x, 0.68, "• Front Parts: Solder on BOTTOM (B.Cu).\n"
                               "  -> EXCEPTION: Solder U1 Pin 1 on TOP (F.Cu) for SW4 Reset!\n"
                               "  -> RV1 sits flush: Pin 3 ties to GND via Via 8 bridge!\n"
                               "• Back Parts (Jack1, Jack2, POT3, J5):\n"
                               "  -> Solder Jack pins on BOTTOM (B.Cu) to catch audio tracks!\n"
                               "  -> Solder J5 4x tabs on TOP for heavy mechanical ground.",
                 color='#c9d1d9', fontsize=8.0, va='top', fontfamily='monospace')

    ax_info.text(col3_x, 0.86, "[3] MULTIMETER CONTINUITY BEEP TEST", color='#e3b341', fontsize=11, weight='bold', fontfamily='monospace')
    ax_info.text(col3_x, 0.68, "Before powering on or inserting ATtiny85:\n"
                               "[✔] TEST 1 (Digital GND): J4 Bat (-) <---> NEO20 Pin 1 (BEEP)\n"
                               "[✔] TEST 2 (Master VCC): J4 Bat (+) <---> U1 Pin 8 (BEEP with SW1 on)\n"
                               "[✔] TEST 3 (Star Audio GND): NT1 Pin 1 <---> Jack2 GNDA (BEEP)\n"
                               "[✔] TEST 4 (Fader GND): RV1 Pin 3 (Bottom) <---> J5 USB GND (BEEP!)\n"
                               "[✔] TEST 5 (Buttons GND): SW2.2 / SW3.2 <---> J5 USB GND (BEEP!)",
                 color='#c9d1d9', fontsize=8.2, va='top', fontfamily='monospace')

    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='#0d1117')
    plt.close()
    print(f"[+] Successfully generated guide graphic: {output_path}")

if __name__ == '__main__':
    out_dir = 'docs/img'
    os.makedirs(out_dir, exist_ok=True)
    out_png = os.path.join(out_dir, 'ABK-20_diy_ground_and_vias_guide.png')
    create_guide_graphic(out_png)

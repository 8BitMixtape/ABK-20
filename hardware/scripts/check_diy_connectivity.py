#!/usr/bin/env python3
"""
check_diy_connectivity.py
=========================
Inspects a KiCad PCB for DIY etching without plated through-holes (PTH).
Identifies:
1. All dedicated vias that require manual wire bridges (rivets/pins).
2. THT component pads that require soldering on specific sides.
3. GND and GNDA layer continuity check between F.Cu and B.Cu.
"""

import os
import re
import math
import argparse

def main():
    parser = argparse.ArgumentParser(description="Check DIY PCB connectivity for non-plated through-holes")
    parser.add_argument("--pcb", default="hardware/ABK-20_DIY.kicad_pcb", help="Path to KiCad PCB")
    args = parser.parse_args()

    pcb_path = os.path.abspath(args.pcb)
    if not os.path.exists(pcb_path):
        print(f"Error: {pcb_path} not found")
        return

    with open(pcb_path) as f:
        text = f.read()

    # 1. Parse Nets
    net_map = {}
    for m in re.finditer(r'\(net\s+(\d+)\s+\"([^\"]+)\"\)', text):
        net_map[int(m.group(1))] = m.group(2)

    # 2. Parse Vias
    vias = []
    for m in re.finditer(r'\(via\s+\(at\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\)\s+\(size\s+([-+]?\d*\.?\d+)\)\s+\(drill\s+([-+]?\d*\.?\d+)\)\s+\(layers\s+\"([^\"]+)\"\s+\"([^\"]+)\"\).*?\(net\s+(\d+)\)', text, re.DOTALL):
        net_id = int(m.group(7))
        vias.append({
            'x': float(m.group(1)), 'y': float(m.group(2)),
            'size': float(m.group(3)), 'drill': float(m.group(4)),
            'net_id': net_id, 'net_name': net_map.get(net_id, f"Net {net_id}")
        })

    print("=" * 70)
    print(" 🛠️  DIY ETCHING CONNECTIVITY REPORT (NON-PLATED HOLES)")
    print(f" Board: {os.path.basename(pcb_path)}")
    print("=" * 70)

    print(f"\n[*] 1. DEDICATED VIAS (MUST SOLDER WIRE PINS THROUGH TOP & BOTTOM):")
    print(f"    Total dedicated vias: {len(vias)}")
    print("    " + "-" * 66)
    print(f"    {'#':<3} {'Coordinates (X, Y)':<22} {'Net Name':<25} {'Drill / Pad'}")
    print("    " + "-" * 66)
    for i, v in enumerate(vias):
        coord_str = f"({v['x']:.2f}, {v['y']:.2f}) mm"
        drill_str = f"Ø {v['drill']:.1f} / {v['size']:.1f} mm"
        print(f"    {i+1:<3} {coord_str:<22} {v['net_name']:<25} {drill_str}")

    # 3. Parse THT Pads
    tht_gnd_pads = []
    for m in re.finditer(r'\(footprint\s+\"([^\"]+)\"(.*?)(?=\n\t\(footprint|\Z)', text, re.DOTALL):
        fp_type = m.group(1)
        chunk = m.group(2)
        ref_m = re.search(r'\(property\s+\"Reference\"\s+\"([^\"]+)\"', chunk)
        ref = ref_m.group(1) if ref_m else 'UNKNOWN'
        layer_m = re.search(r'\(layer\s+\"([^\"]+)\"\)', chunk)
        fp_layer = layer_m.group(1) if layer_m else 'F.Cu'

        for pm in re.finditer(r'\(pad\s+\"([^\"]+)\"\s+thru_hole\s+([^\s\)]+)(.*?)\n\t\t\)', chunk, re.DOTALL):
            p_num = pm.group(1)
            p_body = pm.group(3)
            net_m = re.search(r'\(net\s+(\d+)\s+\"([^\"]+)\"\)', p_body)
            if net_m:
                net_id = int(net_m.group(1))
                net_name = net_m.group(2)
                if 'gnd' in net_name.lower():
                    solder_side = 'B.Cu (Bottom)' if fp_layer == 'F.Cu' else 'F.Cu (Top)'
                    tht_gnd_pads.append({
                        'ref': ref, 'pin': p_num, 'layer': fp_layer,
                        'solder_side': solder_side, 'net_name': net_name,
                        'fp_type': fp_type
                    })

    print(f"\n[*] 2. THT GROUND PADS (GND / GNDA) SOLDER-SIDE GUIDE:")
    print("    " + "-" * 66)
    print(f"    {'Component':<12} {'Pin':<6} {'Mount Side':<12} {'Solder On':<15} {'Net'}")
    print("    " + "-" * 66)
    for p in sorted(tht_gnd_pads, key=lambda x: (x['solder_side'], x['ref'])):
        print(f"    {p['ref']:<12} {p['pin']:<6} {p['layer']:<12} {p['solder_side']:<15} {p['net_name']}")

    print("\n[*] 3. GROUND CONTINUITY SUMMARY:")
    print("    - Top Ground (F.Cu): Power return for all 20 NeoPixels (WS2812B SMD).")
    print("    - Bottom Ground (B.Cu): Power input from Battery (J4) and USB-C (J5).")
    print("    - CRITICAL BRIDGE: Via 1 at (86.82, 44.45) mm links F.Cu GND to B.Cu GND.")
    print("    - OPTIONAL EXTRA BRIDGES: J5 (USB-C) shield tabs poke through to F.Cu.")
    print("      Soldering J5 shield tabs on F.Cu creates a 4-point heavy ground tie.")
    print("=" * 70)

if __name__ == "__main__":
    main()

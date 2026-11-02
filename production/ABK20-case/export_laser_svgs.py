#!/usr/bin/env python3
"""
Parametric Laser Cut SVG Exporter for ABK-20 Enclosure
======================================================
Generates ready-to-burn, multi-layered SVG files for LightBurn:
- Layer C00 (Black / Line): Through-cuts (100% laser power)
- Layer C01 (Blue / Fill): Blind notch mortises & underside component pockets

Usage:
  python3 export_laser_svgs.py                 # Interactive or defaults to SuperVintage
  python3 export_laser_svgs.py SuperVintage    # Export specific preset
  python3 export_laser_svgs.py --list          # List available presets
"""

import sys
import os
import json
import shutil
import subprocess
import re
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCAD_FILE = os.path.join(SCRIPT_DIR, "ABK-20_case.scad")
JSON_FILE = os.path.join(SCRIPT_DIR, "ABK-20_case.json")
OUTPUT_BASE = os.path.join(SCRIPT_DIR, "laser_export")

def find_openscad():
    candidates = [
        "/snap/bin/openscad",
        "/usr/local/bin/openscad",
        shutil.which("openscad"),
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    raise FileNotFoundError("OpenSCAD binary not found on system!")

def load_presets():
    with open(JSON_FILE, "r") as f:
        data = json.load(f)
    return data.get("parameterSets", {})

def build_scad_args(preset_params, part_to_show):
    args = []
    # Copy parameters
    params = dict(preset_params)
    params["part_to_show"] = f'"{part_to_show}"'
    
    for k, v in params.items():
        v_str = str(v)
        # Check if bool
        if v_str.lower() in ["true", "false"]:
            args.extend(["-D", f"{k}={v_str.lower()}"])
        # Check if number
        elif re.match(r"^-?\d+(\.\d+)?$", v_str):
            args.extend(["-D", f"{k}={v_str}"])
        else:
            # String value: ensure quoted
            if not (v_str.startswith('"') and v_str.endswith('"')):
                v_str = f'"{v_str}"'
            args.extend(["-D", f"{k}={v_str}"])
    return args

def export_raw_svg(openscad_bin, preset_params, part_to_show, output_path):
    cmd = [openscad_bin]
    cmd.extend(build_scad_args(preset_params, part_to_show))
    cmd.extend(["-o", output_path, SCAD_FILE])
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"[-] Error exporting {part_to_show}:")
        print(res.stderr)
        return False
    return True

def extract_paths_from_svg(svg_path):
    """Extract path elements and viewBox from an OpenSCAD-generated SVG."""
    if not os.path.exists(svg_path):
        return [], None, None, None
    tree = ET.parse(svg_path)
    root = tree.getroot()
    # Strip namespace if any
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"
    
    view_box = root.attrib.get("viewBox")
    width = root.attrib.get("width")
    height = root.attrib.get("height")
    
    paths = []
    for elem in root.iter(f"{ns}path"):
        d = elem.attrib.get("d")
        if d:
            paths.append(d)
    return paths, view_box, width, height

def create_combined_svg(output_path, base_svg_path, pocket_svg_path=None, cut_label="CUTS", pocket_label="POCKETS"):
    """Combines cut paths (Black) and optional pocket paths (Blue) with matching viewBox."""
    cut_paths, view_box, width, height = extract_paths_from_svg(base_svg_path)
    pocket_paths = []
    if pocket_svg_path and os.path.exists(pocket_svg_path):
        pocket_paths, _, _, _ = extract_paths_from_svg(pocket_svg_path)
    
    if not cut_paths:
        print(f"[-] No cut paths found in {base_svg_path}")
        return False
        
    svg_header = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="{width}" height="{height}" viewBox="{view_box}" xmlns="http://www.w3.org/2000/svg" version="1.1">
  <title>{cut_label}</title>
  
  <!-- LightBurn Layer C00: Through-Cut Paths (Black / Line Mode) -->
  <g id="Layer_C00_CUTS_{cut_label}" stroke="#000000" fill="none" stroke-width="0.1mm">
"""
    body_cuts = "".join(f'    <path d="{d}" />\n' for d in cut_paths)
    
    if pocket_paths:
        svg_middle = f"""  </g>

  <!-- LightBurn Layer C01: Underside Clearance / Blind Mortise Pockets (Blue / Fill Mode) -->
  <g id="Layer_C01_ENGRAVE_{pocket_label}" stroke="#0000ff" fill="none" stroke-width="0.1mm">
"""
        body_pockets = "".join(f'    <path d="{d}" />\n' for d in pocket_paths)
        svg_footer = """  </g>
</svg>
"""
        content = svg_header + body_cuts + svg_middle + body_pockets + svg_footer
    else:
        content = svg_header + body_cuts + "  </g>\n</svg>\n"
        
    with open(output_path, "w") as f:
        f.write(content)
        
    return True

def main():
    presets = load_presets()
    if not presets:
        print("[-] No presets found in ABK-20_case.json")
        sys.exit(1)
        
    if len(sys.argv) > 1 and sys.argv[1] in ["--list", "-l", "--help", "-h"]:
        print("Usage: python3 export_laser_svgs.py [preset_name]")
        print("\nAvailable presets in ABK-20_case.json:")
        for name in presets:
            print(f"  - {name}")
        sys.exit(0)
        
    chosen_preset = sys.argv[1] if len(sys.argv) > 1 else "SuperVintage"
    if chosen_preset not in presets:
        print(f"[-] Preset '{chosen_preset}' not found! Choose from: {list(presets.keys())}")
        sys.exit(1)
        
    preset_params = presets[chosen_preset]
    openscad_bin = find_openscad()
    
    preset_out_dir = os.path.join(OUTPUT_BASE, chosen_preset)
    indiv_out_dir = os.path.join(preset_out_dir, "individual")
    os.makedirs(indiv_out_dir, exist_ok=True)
    
    thickness_main = preset_params.get("thickness", "3.0")
    thickness_sides = preset_params.get("thickness_sides", "5.0")
    
    print(f"[+] Exporting LightBurn SVGs for preset: '{chosen_preset}'")
    print(f"    - Main material thickness: {thickness_main} mm")
    print(f"    - Cheeks thickness:        {thickness_sides} mm")
    print(f"    - Using OpenSCAD binary:   {openscad_bin}")
    
    # 1. Export 3mm Main cuts & pockets
    raw_main_cuts = os.path.join(indiv_out_dir, "raw_main_cuts.svg")
    raw_main_pockets = os.path.join(indiv_out_dir, "raw_main_pockets.svg")
    
    print("    [1/5] Rendering main box cuts...")
    export_raw_svg(openscad_bin, preset_params, "layout_main", raw_main_cuts)
    
    print("    [2/5] Rendering top faceplate underside pockets...")
    export_raw_svg(openscad_bin, preset_params, "layout_main_pockets", raw_main_pockets)
    
    # 2. Export Cheeks cuts & pockets
    raw_sides_cuts = os.path.join(indiv_out_dir, "raw_sides_cuts.svg")
    raw_sides_pockets = os.path.join(indiv_out_dir, "raw_sides_pockets.svg")
    
    print("    [3/5] Rendering side cheeks cuts...")
    export_raw_svg(openscad_bin, preset_params, "layout_sides", raw_sides_cuts)
    
    print("    [4/5] Rendering side cheeks blind mortise pockets...")
    export_raw_svg(openscad_bin, preset_params, "layout_sides_pockets", raw_sides_pockets)

    # 3. Export standalone Matrix Baffle Grid
    raw_matrix_grid = os.path.join(indiv_out_dir, "raw_matrix_grid.svg")
    print("    [5/5] Rendering standalone matrix baffle grid...")
    export_raw_svg(openscad_bin, preset_params, "matrix_grid", raw_matrix_grid)
    
    # 4. Combine into LightBurn multi-layer files
    comb_main = os.path.join(preset_out_dir, f"01_ABK-20_{chosen_preset}_{thickness_main}mm_main_sheet.svg")
    comb_sides = os.path.join(preset_out_dir, f"02_ABK-20_{chosen_preset}_cheeks_{thickness_sides}mm.svg")
    comb_grid = os.path.join(preset_out_dir, f"03_ABK-20_{chosen_preset}_matrix_baffle_grid.svg")
    
    create_combined_svg(comb_main, raw_main_cuts, raw_main_pockets, "MAIN_BOX", "TOP_CLEARANCE")
    create_combined_svg(comb_sides, raw_sides_cuts, raw_sides_pockets, "SIDE_CHEEKS", "BLIND_MORTISES")
    create_combined_svg(comb_grid, raw_matrix_grid, None, "MATRIX_BAFFLE_GRID")
    
    print("\n[+] SUCCESS! Exported LightBurn Multi-Layer SVGs:")
    print(f"    👉 Sheet 1 (Main Box {thickness_main}mm):     {comb_main}")
    print(f"    👉 Sheet 2 (Cheeks {thickness_sides}mm):       {comb_sides}")
    print(f"    👉 Sheet 3 (Standalone Grid):          {comb_grid}")
    print("\n[i] LightBurn Layer Mapping:")
    print("    - Black (C00): Line Mode -> Cut through")
    print("    - Blue  (C01): Fill Mode -> Pocket engrave (1.2mm on top plate, 2.0mm on cheeks)")

if __name__ == "__main__":
    main()


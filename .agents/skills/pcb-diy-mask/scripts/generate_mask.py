#!/usr/bin/env python3
"""
generate_mask.py
================
Automated pipeline to generate 1:1 scale double-sided DIY photolithography
and etching masks (A4 envelope pouch) directly from a KiCad PCB layout.

Features:
- Exports vector F.Cu (mirrored) and B.Cu (direct) with pilot drill centers.
- Automatically calculates symmetrical placement around the A4 center fold line.
- Adds 4-corner registration crosshairs, fold guidelines, and 50.0 mm calibration bar.
- Renders all typography as 100% pure vector bezier paths (zero font substitution bugs).
- Automatically converts to production-grade PDF via Inkscape CLI (Cairo backend).
"""

import os
import sys
import shutil
import glob
import subprocess
import argparse
import re
import xml.etree.ElementTree as ET

# Matplotlib for text-to-path conversion
import matplotlib
matplotlib.use('Agg')
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path


def find_inkscape():
    """Locate inkscape binary or AppImage."""
    # Check standard PATH
    path = shutil.which('inkscape')
    if path:
        return path

    # Check common user AppImage locations
    search_paths = [
        os.path.expanduser('~/Software/Inkscape*.AppImage'),
        os.path.expanduser('~/.local/bin/inkscape*'),
        '/opt/inkscape*/inkscape*',
    ]
    for pattern in search_paths:
        matches = sorted(glob.glob(pattern), reverse=True)
        if matches:
            for m in matches:
                if os.access(m, os.X_OK):
                    return m
    return None


def text_to_svg_path(text, x, y, size, align='center', weight='bold'):
    """Convert any text string into pure SVG path d string."""
    prop = FontProperties(family='monospace', weight=weight)
    tp = TextPath((0, 0), text, size=size, prop=prop)
    bbox = tp.get_extents()
    width = bbox.width
    if align == 'center':
        x_offset = x - width / 2 - bbox.xmin
    elif align == 'right':
        x_offset = x - width - bbox.xmin
    else:
        x_offset = x - bbox.xmin
    y_offset = y

    parts = []
    for verts, code in tp.iter_segments():
        if code == Path.MOVETO:
            parts.append(f'M {verts[0]+x_offset:.3f} {-verts[1]+y_offset:.3f}')
        elif code == Path.LINETO:
            parts.append(f'L {verts[0]+x_offset:.3f} {-verts[1]+y_offset:.3f}')
        elif code == Path.CURVE3:
            parts.append(f'Q {verts[0]+x_offset:.3f} {-verts[1]+y_offset:.3f} {verts[2]+x_offset:.3f} {-verts[3]+y_offset:.3f}')
        elif code == Path.CURVE4:
            parts.append(f'C {verts[0]+x_offset:.3f} {-verts[1]+y_offset:.3f} {verts[2]+x_offset:.3f} {-verts[3]+y_offset:.3f} {verts[4]+x_offset:.3f} {-verts[5]+y_offset:.3f}')
        elif code == Path.CLOSEPOLY:
            parts.append('Z')
    return ' '.join(parts)


def get_board_bounds(svg_path):
    """Extract board bounding box and center from an exported KiCad SVG."""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    xs, ys = [], []
    for g in root.iter('{http://www.w3.org/2000/svg}g'):
        for p in g.findall('{http://www.w3.org/2000/svg}path'):
            d = p.get('d', '')
            # Look for Edge.Cuts arcs or coordinates
            nums = [float(x) for x in re.findall(r'[-+]?\d*\.\d+|\d+', d)]
            if len(nums) >= 4:
                for i in range(0, len(nums) - 1, 2):
                    # Filter out zero coordinates that might be arc params
                    if 10.0 <= nums[i] <= 290.0 and 10.0 <= nums[i+1] <= 200.0:
                        xs.append(nums[i])
                        ys.append(nums[i+1])
    if not xs:
        # Fallback to standard 75x80 board defaults if parsing fails
        return (114.71, 68.66, 75.0, 80.0)
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    return ((min_x + max_x) / 2.0, (min_y + max_y) / 2.0, max_x - min_x, max_y - min_y)


def main():
    parser = argparse.ArgumentParser(description='Generate DIY Photolithography & Etching Mask (A4 Pouch)')
    parser.add_argument('--pcb', default='hardware/ABK-20.kicad_pcb', help='Path to KiCad PCB file')
    parser.add_argument('--out-dir', default='production/MASK', help='Output directory')
    parser.add_argument('--board-name', default='ABK-20 SYNTHESIZER', help='Project / Board title')
    parser.add_argument('--rev', default='REV 0.3', help='Hardware revision string')
    parser.add_argument('--name', default='ABK-20-DIY-etch', help='Output base filename (without .svg/.pdf extension)')
    parser.add_argument('--drill-shape-opt', default='2', choices=['0', '1', '2'],
                        help='Pad/via drill shape option: 0=no hole, 1=small pilot hole, 2=actual drill hole (default: 2)')
    parser.add_argument('--keep-layers', action='store_true',
                        help='Keep intermediate individual layer SVG exports in out-dir (default: False)')
    args = parser.parse_args()

    pcb_path = os.path.abspath(args.pcb)
    out_dir = os.path.abspath(args.out_dir)
    os.makedirs(out_dir, exist_ok=True)
    tmp_dir = '/tmp/kicad_mask_gen'
    os.makedirs(tmp_dir, exist_ok=True)

    print(f"[*] Processing KiCad PCB: {pcb_path}")
    print(f"[*] Output directory:     {out_dir}")

    # 1. Export Front Copper (mirrored) and Bottom Copper (direct)
    f_cu_tmp = os.path.join(tmp_dir, 'F_Cu_mirrored.svg')
    b_cu_tmp = os.path.join(tmp_dir, 'B_Cu_unmirrored.svg')
    edge_tmp = os.path.join(tmp_dir, 'Edge_Cuts.svg')

    print("[*] Exporting copper layers via kicad-cli...")
    subprocess.run([
        'kicad-cli', 'pcb', 'export', 'svg',
        '-l', 'F.Cu,Edge.Cuts',
        '--black-and-white', '--drill-shape-opt', args.drill_shape_opt,
        '--mirror', '--exclude-drawing-sheet',
        '-o', f_cu_tmp, pcb_path
    ], check=True, stdout=subprocess.DEVNULL)

    subprocess.run([
        'kicad-cli', 'pcb', 'export', 'svg',
        '-l', 'B.Cu,Edge.Cuts',
        '--black-and-white', '--drill-shape-opt', args.drill_shape_opt,
        '--exclude-drawing-sheet',
        '-o', b_cu_tmp, pcb_path
    ], check=True, stdout=subprocess.DEVNULL)

    subprocess.run([
        'kicad-cli', 'pcb', 'export', 'svg',
        '-l', 'Edge.Cuts',
        '--black-and-white', '--exclude-drawing-sheet',
        '-o', edge_tmp, pcb_path
    ], check=True, stdout=subprocess.DEVNULL)

    # Copy individual standalone layers only if requested
    if args.keep_layers:
        shutil.copy(f_cu_tmp, os.path.join(out_dir, f'{args.name}-F_Cu.svg'))
        shutil.copy(b_cu_tmp, os.path.join(out_dir, f'{args.name}-B_Cu.svg'))
        shutil.copy(edge_tmp, os.path.join(out_dir, f'{args.name}-Edge_Cuts.svg'))
        print(f"[+] Preserved individual layer SVGs in {out_dir}")

    # 2. Parse SVG roots and measure board centers
    tree_f = ET.parse(f_cu_tmp)
    root_f = tree_f.getroot()
    tree_b = ET.parse(b_cu_tmp)
    root_b = tree_b.getroot()

    cx_f, cy_f, bw_f, bh_f = get_board_bounds(f_cu_tmp)
    cx_b, cy_b, bw_b, bh_b = get_board_bounds(b_cu_tmp)

    # 3. Build A4 Landscape Envelope Mask SVG
    a4_w = 297.0
    a4_h = 210.0
    fold_x = a4_w / 2.0  # 148.5 mm
    target_cy = 105.0

    # Symmetric distance from fold line
    dist_from_fold = 73.5
    target_cx_left = fold_x - dist_from_fold   # 75.0 mm
    target_cx_right = fold_x + dist_from_fold  # 222.0 mm

    new_root = ET.Element('svg', {
        'version': '1.1',
        'xmlns': 'http://www.w3.org/2000/svg',
        'xmlns:xlink': 'http://www.w3.org/1999/xlink',
        'width': f'{a4_w:.4f}mm',
        'height': f'{a4_h:.4f}mm',
        'viewBox': f'0.0000 0.0000 {a4_w:.4f} {a4_h:.4f}'
    })

    style = ET.SubElement(new_root, 'style')
    style.text = '''
      .textpath { fill: #000000; stroke: none; fill-rule: nonzero; }
      .textpath_gray { fill: #333333; stroke: none; fill-rule: nonzero; }
      .crosshair { stroke: #000000; stroke-width: 0.25; fill: none; }
      .foldline { stroke: #666666; stroke-width: 0.3; stroke-dasharray: 2.5, 2.5; fill: none; }
      .calib { stroke: #000000; stroke-width: 0.4; fill: none; }
    '''

    def add_text(parent, text, x, y, size, align='center', weight='bold', is_gray=False):
        d = text_to_svg_path(text, x, y, size, align, weight)
        cls = 'textpath_gray' if is_gray else 'textpath'
        ET.SubElement(parent, 'path', {'d': d, 'class': cls})

    # Fold line
    ET.SubElement(new_root, 'path', {'d': f'M {fold_x} 14 L {fold_x} 196', 'class': 'foldline'})
    add_text(new_root, 'FOLD LINE (FOLD IN HALF FOR DOUBLE-SIDED POUCH ENVELOPE)', fold_x, 11.0, 2.0, 'center', 'bold', True)

    # Top Title
    add_text(new_root, f'{args.board_name} -- {args.rev} DIY PHOTOLITHO MASK (1:1 SCALE)', fold_x, 19.0, 3.6, 'center', 'bold')

    # Column Headers
    add_text(new_root, 'TOP LAYER (F.Cu) -- [MIRRORED FOR EMULSION-DOWN UV]', target_cx_left, 57.0, 2.8, 'center', 'bold')
    add_text(new_root, f'{bw_f:.1f} x {bh_f:.1f} mm -- Direct Emulsion Contact on Top Copper', target_cx_left, 61.5, 2.0, 'center', 'normal', True)

    add_text(new_root, 'BOTTOM LAYER (B.Cu) -- [SOLDER SIDE EMULSION-UP]', target_cx_right, 57.0, 2.8, 'center', 'bold')
    add_text(new_root, f'{bw_b:.1f} x {bh_b:.1f} mm -- Direct Emulsion Contact on Bottom Copper', target_cx_right, 61.5, 2.0, 'center', 'normal', True)

    # Calibration Bar (50 mm)
    cal_x = fold_x - 25.0
    cal_g = ET.SubElement(new_root, 'g', {'transform': f'translate({cal_x:.2f}, 185.0)'})
    ET.SubElement(cal_g, 'path', {
        'd': 'M 0 0 L 50 0 M 0 -2.5 L 0 2.5 M 10 -1.5 L 10 1.5 M 20 -1.5 L 20 1.5 M 30 -1.5 L 30 1.5 M 40 -1.5 L 40 1.5 M 50 -2.5 L 50 2.5',
        'class': 'calib'
    })
    add_text(cal_g, '<--- EXACT 50.0 mm CALIBRATION SCALE BAR --->', 25.0, 6.0, 2.2, 'center', 'bold')

    # Alignment Crosshairs
    def add_crosshairs(parent, cx, cy):
        for sx in [-1, 1]:
            for sy in [-1, 1]:
                hx = cx + sx * (bw_f / 2.0 + 4.0)
                hy = cy + sy * (bh_f / 2.0 + 4.0)
                ET.SubElement(parent, 'path', {
                    'd': f'M {hx-3.5:.2f} {hy:.2f} L {hx+3.5:.2f} {hy:.2f} M {hx:.2f} {hy-3.5:.2f} L {hx:.2f} {hy+3.5:.2f}',
                    'class': 'crosshair'
                })
                ET.SubElement(parent, 'circle', {
                    'cx': f'{hx:.2f}', 'cy': f'{hy:.2f}', 'r': '1.5',
                    'class': 'crosshair'
                })

    add_crosshairs(new_root, target_cx_left, target_cy)
    add_crosshairs(new_root, target_cx_right, target_cy)

    # Attach F_Cu (mirrored)
    dx_f = target_cx_left - cx_f
    dy_f = target_cy - cy_f
    gf = ET.SubElement(new_root, 'g', {
        'id': 'layer_F_Cu_mirrored',
        'transform': f'translate({dx_f:.4f}, {dy_f:.4f})'
    })
    for child in root_f:
        if child.tag.endswith('g'):
            gf.append(child)

    # Attach B_Cu (unmirrored)
    dx_b = target_cx_right - cx_b
    dy_b = target_cy - cy_b
    gb = ET.SubElement(new_root, 'g', {
        'id': 'layer_B_Cu_unmirrored',
        'transform': f'translate({dx_b:.4f}, {dy_b:.4f})'
    })
    for child in root_b:
        if child.tag.endswith('g'):
            gb.append(child)

    svg_out = os.path.join(out_dir, f'{args.name}.svg')
    ET.ElementTree(new_root).write(svg_out, encoding='utf-8', xml_declaration=True)
    print(f"[+] Successfully wrote SVG: {svg_out}")

    # 4. Convert SVG to PDF via Inkscape CLI
    pdf_out = os.path.join(out_dir, f'{args.name}.pdf')
    inkscape_bin = find_inkscape()
    if inkscape_bin:
        print(f"[*] Rendering PDF via Inkscape: {inkscape_bin}")
        res = subprocess.run([
            inkscape_bin,
            f'--export-filename={pdf_out}',
            svg_out
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode == 0 and os.path.exists(pdf_out):
            pdf_size = os.path.getsize(pdf_out)
            print(f"[+] Successfully wrote 1:1 Vector PDF: {pdf_out} ({pdf_size} bytes)")
        else:
            print(f"[!] Inkscape conversion warning/error: {res.stderr.decode('utf-8', errors='ignore')}")
    else:
        print("[!] Inkscape not found; please open SVG in Inkscape and save as PDF.")

    # Clean up temporary files
    shutil.rmtree(tmp_dir, ignore_errors=True)

    print("[✔] Done!")


if __name__ == '__main__':
    main()


#!/usr/bin/env python3
"""
Generate Freedesktop standard thumbnails for all WRL and STEP 3D models in hardware/3d_models
into ~/.cache/thumbnails/large/ and ~/.cache/thumbnails/normal/
"""
import os
import hashlib
import struct
import re
import math
import subprocess
from PIL import Image, PngImagePlugin

models_dir = '/home/dusjagr/Documents/8bit_Mixtape/ABK-20/hardware/3d_models'
large_dir = '/home/dusjagr/.cache/thumbnails/large'
normal_dir = '/home/dusjagr/.cache/thumbnails/normal'
fail_dir = '/home/dusjagr/.cache/thumbnails/fail/gnome-thumbnail-factory'

os.makedirs(large_dir, exist_ok=True)
os.makedirs(normal_dir, exist_ok=True)

def calc_normal(p1, p2, p3):
    u = (p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2])
    v = (p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2])
    nx = u[1]*v[2] - u[2]*v[1]
    ny = u[2]*v[0] - u[0]*v[2]
    nz = u[0]*v[1] - u[1]*v[0]
    l = math.sqrt(nx*nx + ny*ny + nz*nz)
    if l < 1e-7:
        return None
    return (nx/l, ny/l, nz/l)

print(f"Scanning {models_dir}...")
count = 0
wrl_images = {} # base_name -> (PIL Image, diff_hex)

# 1. Generate thumbnails for all WRL models
for fname in sorted(os.listdir(models_dir)):
    if not fname.endswith('.wrl'):
        continue
    base_name = os.path.splitext(fname)[0]
    filepath = os.path.join(models_dir, fname)
    uri = f'file://{filepath}'
    mtime = str(int(os.path.getmtime(filepath)))
    md5_hash = hashlib.md5(uri.encode('utf-8')).hexdigest()

    fail_file = os.path.join(fail_dir, f'{md5_hash}.png')
    if os.path.exists(fail_file):
        try: os.remove(fail_file)
        except Exception: pass

    with open(filepath, 'r', errors='ignore') as f:
        text = f.read()

    # Color extraction
    m = re.search(r'diffuseColor\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)', text)
    if m:
        r, g, b = float(m.group(1)), float(m.group(2)), float(m.group(3))
        lum = 0.299*r + 0.587*g + 0.114*b
        if lum < 0.2:
            diff_hex = '333336'
            amb_hex = '111112'
        else:
            diff_hex = f'{min(255, int(r*255)):02x}{min(255, int(g*255)):02x}{min(255, int(b*255)):02x}'
            amb_hex = f'{min(255, int(r*70)):02x}{min(255, int(g*70)):02x}{min(255, int(b*70)):02x}'
        spec_hex = 'eeeeee'
    else:
        amb_hex, diff_hex, spec_hex = '222222', '888888', 'ffffff'

    shapes = text.split('Shape {')
    triangles = []
    for s in shapes[1:]:
        pt_m = re.search(r'point\s*\[(.*?)\]', s, re.DOTALL)
        idx_m = re.search(r'coordIndex\s*\[(.*?)\]', s, re.DOTALL)
        if pt_m and idx_m:
            raw_pts = pt_m.group(1).replace(',', ' ').split()
            pts = [(float(raw_pts[i]), float(raw_pts[i+1]), float(raw_pts[i+2])) for i in range(0, len(raw_pts), 3)]
            raw_idx = idx_m.group(1).replace(',', ' ').split()
            poly = []
            for token in raw_idx:
                v = int(token)
                if v == -1:
                    if len(poly) == 3:
                        n = calc_normal(pts[poly[0]], pts[poly[1]], pts[poly[2]])
                        if n: triangles.append((n, pts[poly[0]], pts[poly[1]], pts[poly[2]]))
                    elif len(poly) == 4:
                        n1 = calc_normal(pts[poly[0]], pts[poly[1]], pts[poly[2]])
                        if n1: triangles.append((n1, pts[poly[0]], pts[poly[1]], pts[poly[2]]))
                        n2 = calc_normal(pts[poly[0]], pts[poly[2]], pts[poly[3]])
                        if n2: triangles.append((n2, pts[poly[0]], pts[poly[2]], pts[poly[3]]))
                    elif len(poly) > 4:
                        for k in range(1, len(poly)-1):
                            n = calc_normal(pts[poly[0]], pts[poly[k]], pts[poly[k+1]])
                            if n: triangles.append((n, pts[poly[0]], pts[poly[k]], pts[poly[k+1]]))
                    poly = []
                else:
                    poly.append(v)

    if not triangles:
        print(f"Skipping {fname}: no valid triangles")
        continue

    header = b'Binary STL' + b' ' * 70
    out = bytearray(header[:80])
    out.extend(struct.pack('<I', len(triangles)))
    for n, p1, p2, p3 in triangles:
        out.extend(struct.pack('<3f', n[0], n[1], n[2]))
        out.extend(struct.pack('<3f', p1[0], p1[1], p1[2]))
        out.extend(struct.pack('<3f', p2[0], p2[1], p2[2]))
        out.extend(struct.pack('<3f', p3[0], p3[1], p3[2]))
        out.extend(struct.pack('<H', 0))

    temp_stl = f'/tmp/thumb_{md5_hash}.stl'
    temp_png = f'/tmp/thumb_{md5_hash}.png'
    with open(temp_stl, 'wb') as f:
        f.write(out)

    env = os.environ.copy()
    env['XDG_RUNTIME_DIR'] = '/run/user/1000'
    env['WAYLAND_DISPLAY'] = 'wayland-0'

    cmd = ['stl-thumb', '-m', amb_hex, diff_hex, spec_hex, '-f', 'png', '-s', '256', temp_stl, temp_png]
    res = subprocess.run(cmd, capture_output=True, env=env)

    if os.path.exists(temp_png):
        img = Image.open(temp_png)
        wrl_images[base_name] = (img.copy(), diff_hex)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text('Thumb::URI', uri)
        pnginfo.add_text('Thumb::MTime', mtime)
        pnginfo.add_text('Software', 'GNOME::ThumbnailFactory')

        large_path = os.path.join(large_dir, f'{md5_hash}.png')
        img.save(large_path, 'PNG', pnginfo=pnginfo)

        normal_path = os.path.join(normal_dir, f'{md5_hash}.png')
        resample_filter = getattr(Image, 'Resampling', Image).LANCZOS
        img_normal = img.resize((128, 128), resample_filter)
        img_normal.save(normal_path, 'PNG', pnginfo=pnginfo)

        os.remove(temp_png)
        count += 1
        print(f"[{count}] WRL thumbnail: {fname} -> {md5_hash}.png (#{diff_hex})")

    if os.path.exists(temp_stl):
        os.remove(temp_stl)

# 2. Generate thumbnails for matching STEP models using the WRL renders
step_count = 0
for fname in sorted(os.listdir(models_dir)):
    if not fname.endswith('.step') and not fname.endswith('.stp'):
        continue
    base_name = os.path.splitext(fname)[0]
    if base_name in wrl_images:
        filepath = os.path.join(models_dir, fname)
        uri = f'file://{filepath}'
        mtime = str(int(os.path.getmtime(filepath)))
        md5_hash = hashlib.md5(uri.encode('utf-8')).hexdigest()

        fail_file = os.path.join(fail_dir, f'{md5_hash}.png')
        if os.path.exists(fail_file):
            try: os.remove(fail_file)
            except Exception: pass

        img, diff_hex = wrl_images[base_name]
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text('Thumb::URI', uri)
        pnginfo.add_text('Thumb::MTime', mtime)
        pnginfo.add_text('Software', 'GNOME::ThumbnailFactory')

        large_path = os.path.join(large_dir, f'{md5_hash}.png')
        img.save(large_path, 'PNG', pnginfo=pnginfo)

        normal_path = os.path.join(normal_dir, f'{md5_hash}.png')
        resample_filter = getattr(Image, 'Resampling', Image).LANCZOS
        img_normal = img.resize((128, 128), resample_filter)
        img_normal.save(normal_path, 'PNG', pnginfo=pnginfo)

        step_count += 1
        print(f"[STEP {step_count}] STEP thumbnail: {fname} -> {md5_hash}.png (#{diff_hex})")

print(f"\nAll done! Generated {count} WRL thumbnails and {step_count} STEP thumbnails.")

#!/usr/bin/env python3
"""
Generate high-fidelity VRML 2.0 (.wrl) 3D model for 16mm Rotary Potentiometer
Matching user-verified size and alignment for Potentiometer_backPads_noHole.
Offset in footprint: (offset (xyz 0 10 -2.5))
All cylindrical shells are double-sided to prevent any backface culling in KiCad.
"""
import math

# Baked-in shift so footprint uses offset (0 0 0)
SHIFT_X = 0.0
SHIFT_Y = 10.0
SHIFT_Z = -2.5

def format_vec(x, y, z):
    # Apply baked-in shift (mm), then convert to VRML units (1 unit = 2.54 mm)
    return f"{(x + SHIFT_X)/2.54:.4f} {(y + SHIFT_Y)/2.54:.4f} {(z + SHIFT_Z)/2.54:.4f}"

def generate_pot_wrl(out_path):
    shapes = []

    # -------------------------------------------------------------
    # 1. Main Can / Housing (Golden / Brass Plated Metal)
    # -------------------------------------------------------------
    cx, cy = 10.0, -5.0
    r_body = 8.0
    z_top = -0.8
    z_bot = -7.8
    n_seg = 32

    body_pts = []
    for i in range(n_seg):
        ang = 2 * math.pi * i / n_seg
        body_pts.append((cx + r_body * math.cos(ang), cy + r_body * math.sin(ang), z_top))
    for i in range(n_seg):
        ang = 2 * math.pi * i / n_seg
        body_pts.append((cx + r_body * math.cos(ang), cy + r_body * math.sin(ang), z_bot))
    body_pts.append((cx, cy, z_bot))
    c_idx = 2 * n_seg

    body_faces = []
    # Side quads - double-sided so both front and back are always visible
    for i in range(n_seg):
        nxt = (i + 1) % n_seg
        # CCW
        body_faces.append([i, nxt, nxt + n_seg, i + n_seg])
        # CW
        body_faces.append([i, i + n_seg, nxt + n_seg, nxt])
    # Bottom fan
    for i in range(n_seg):
        nxt = (i + 1) % n_seg
        body_faces.append([c_idx, i + n_seg, nxt + n_seg])
        body_faces.append([c_idx, nxt + n_seg, i + n_seg])

    # 4 crimp tabs around rim
    for ang_deg in [45, 135, 225, 315]:
        ang_rad = math.radians(ang_deg)
        w = 1.2
        dx = -math.sin(ang_rad) * w
        dy = math.cos(ang_rad) * w
        px = cx + (r_body - 0.2) * math.cos(ang_rad)
        py = cy + (r_body - 0.2) * math.sin(ang_rad)
        base = len(body_pts)
        body_pts.extend([
            (px - dx, py - dy, z_top),
            (px + dx, py + dy, z_top),
            (px + dx * 0.8, py + dy * 0.8, 0.0),
            (px - dx * 0.8, py - dy * 0.8, 0.0),
        ])
        body_faces.append([base, base+1, base+2, base+3])
        body_faces.append([base, base+3, base+2, base+1])

    shapes.append({
        "name": "Can_Golden_Brass",
        "pts": body_pts,
        "faces": body_faces,
        "diffuse": "0.82 0.70 0.28",
        "specular": "0.90 0.82 0.45",
        "shininess": "0.7",
        "transparency": "0.0"
    })

    # -------------------------------------------------------------
    # 2. Phenolic Terminal Board (Bakelite Warm Orange/Brown)
    # -------------------------------------------------------------
    wafer_pts = [
        (4.0, 2.5, -0.8), (4.0, -12.5, -0.8), (-1.5, -12.5, -0.8), (-1.5, 2.5, -0.8),
        (4.0, 2.5, 0.0), (4.0, -12.5, 0.0), (-1.5, -12.5, 0.0), (-1.5, 2.5, 0.0),
    ]
    wafer_faces = [
        [0, 1, 2, 3], [3, 2, 1, 0],
        [7, 6, 5, 4], [4, 5, 6, 7],
        [0, 3, 7, 4], [4, 7, 3, 0],
        [1, 0, 4, 5], [5, 4, 0, 1],
        [2, 1, 5, 6], [6, 5, 1, 2],
        [3, 2, 6, 7], [7, 6, 2, 3],
    ]
    shapes.append({
        "name": "Phenolic_Wafer",
        "pts": wafer_pts,
        "faces": wafer_faces,
        "diffuse": "0.78 0.45 0.18",
        "specular": "0.25 0.20 0.15",
        "shininess": "0.25",
        "transparency": "0.0"
    })

    # -------------------------------------------------------------
    # 3. Terminals / Solder Lugs (Silver / Tin Plated Metal)
    # -------------------------------------------------------------
    term_pts = []
    term_faces = []

    y_lugs = [0.0, -5.08, -10.08]
    for y_c in y_lugs:
        base = len(term_pts)
        hw = 1.1 # half width
        z0, z1 = 0.0, 0.35

        p0 = ( 0.8, y_c - hw, z0); p1 = (-2.0, y_c - hw, z0)
        p2 = (-2.0, y_c + hw, z0); p3 = ( 0.8, y_c + hw, z0)
        p4 = ( 0.8, y_c - hw, z1); p5 = (-2.0, y_c - hw, z1)
        p6 = (-2.0, y_c + hw, z1); p7 = ( 0.8, y_c + hw, z1)

        p8  = (-3.2, y_c - hw, z0); p9  = (-3.2, y_c - 0.5, z0)
        p10 = (-2.0, y_c - 0.5, z0); p11 = (-3.2, y_c - hw, z1)
        p12 = (-3.2, y_c - 0.5, z1); p13 = (-2.0, y_c - 0.5, z1)

        p14 = (-2.0, y_c + 0.5, z0); p15 = (-3.2, y_c + 0.5, z0)
        p16 = (-3.2, y_c + hw, z0); p17 = (-2.0, y_c + 0.5, z1)
        p18 = (-3.2, y_c + 0.5, z1); p19 = (-3.2, y_c + hw, z1)

        p20 = (-4.2, y_c - hw, z0); p21 = (-4.2, y_c + hw, z0)
        p22 = (-4.2, y_c - hw, z1); p23 = (-4.2, y_c + hw, z1)

        term_pts.extend([
            p0, p1, p2, p3, p4, p5, p6, p7,
            p8, p9, p10, p11, p12, p13,
            p14, p15, p16, p17, p18, p19,
            p20, p21, p22, p23
        ])

        # Top surfaces
        term_faces.append([base+7, base+6, base+5, base+4])
        term_faces.append([base+4, base+5, base+6, base+7])
        term_faces.append([base+6, base+13, base+12, base+19])
        term_faces.append([base+19, base+12, base+13, base+6])
        term_faces.append([base+17, base+7, base+4, base+11])
        term_faces.append([base+11, base+4, base+7, base+17])
        term_faces.append([base+23, base+22, base+11, base+19])
        term_faces.append([base+19, base+11, base+22, base+23])
        # Bottom surfaces
        term_faces.append([base+0, base+1, base+2, base+3])
        term_faces.append([base+3, base+2, base+1, base+0])
        term_faces.append([base+1, base+10, base+9, base+8])
        term_faces.append([base+8, base+9, base+10, base+1])
        term_faces.append([base+14, base+2, base+16, base+15])
        term_faces.append([base+15, base+16, base+2, base+14])
        term_faces.append([base+8, base+20, base+21, base+16])
        term_faces.append([base+16, base+21, base+20, base+8])
        # Outer sides
        term_faces.append([base+0, base+4, base+5, base+1])
        term_faces.append([base+1, base+5, base+4, base+0])
        term_faces.append([base+1, base+5, base+11, base+8])
        term_faces.append([base+8, base+11, base+5, base+1])
        term_faces.append([base+8, base+11, base+22, base+20])
        term_faces.append([base+20, base+22, base+11, base+8])
        term_faces.append([base+20, base+22, base+23, base+21])
        term_faces.append([base+21, base+23, base+22, base+20])
        term_faces.append([base+21, base+23, base+19, base+16])
        term_faces.append([base+16, base+19, base+23, base+21])
        term_faces.append([base+16, base+19, base+6, base+2])
        term_faces.append([base+2, base+6, base+19, base+16])
        term_faces.append([base+2, base+6, base+7, base+3])
        term_faces.append([base+3, base+7, base+6, base+2])
        term_faces.append([base+3, base+7, base+4, base+0])
        term_faces.append([base+0, base+4, base+7, base+3])
        # Inner hole sides
        term_faces.append([base+10, base+13, base+12, base+9])
        term_faces.append([base+9, base+12, base+13, base+10])
        term_faces.append([base+14, base+17, base+18, base+15])
        term_faces.append([base+15, base+18, base+17, base+14])
        term_faces.append([base+10, base+14, base+17, base+13])
        term_faces.append([base+13, base+17, base+14, base+10])
        term_faces.append([base+9, base+12, base+18, base+15])
        term_faces.append([base+15, base+18, base+12, base+9])

        # Eyelet Rivet
        r_riv = 0.8
        riv_base = len(term_pts)
        for i in range(12):
            ang = 2 * math.pi * i / 12
            term_pts.append((0.5 + r_riv * math.cos(ang), y_c + r_riv * math.sin(ang), 0.6))
        for i in range(12):
            ang = 2 * math.pi * i / 12
            term_pts.append((0.5 + 0.4 * math.cos(ang), y_c + 0.4 * math.sin(ang), 0.6))
        for i in range(12):
            nxt = (i + 1) % 12
            term_faces.append([riv_base + i, riv_base + nxt, riv_base + 12 + nxt, riv_base + 12 + i])
            term_faces.append([riv_base + i, riv_base + 12 + i, riv_base + 12 + nxt, riv_base + nxt])

    shapes.append({
        "name": "Terminals_Lugs",
        "pts": term_pts,
        "faces": term_faces,
        "diffuse": "0.85 0.85 0.88",
        "specular": "0.92 0.92 0.95",
        "shininess": "0.85",
        "transparency": "0.0"
    })

    # -------------------------------------------------------------
    # 4. Front Plate, Bushing & Anti-Rotation Tab (Zinc Die-Cast)
    # -------------------------------------------------------------
    front_pts = []
    front_faces = []

    # Front collar plate (Z = 0.0 to 0.8)
    r_collar = 7.5
    c_base = len(front_pts)
    for i in range(n_seg):
        ang = 2 * math.pi * i / n_seg
        front_pts.append((cx + r_collar * math.cos(ang), cy + r_collar * math.sin(ang), 0.0))
    for i in range(n_seg):
        ang = 2 * math.pi * i / n_seg
        front_pts.append((cx + r_collar * math.cos(ang), cy + r_collar * math.sin(ang), 0.8))
    for i in range(n_seg):
        nxt = (i + 1) % n_seg
        front_faces.append([c_base + i, c_base + nxt, c_base + n_seg + nxt, c_base + n_seg + i])
        front_faces.append([c_base + i, c_base + n_seg + i, c_base + n_seg + nxt, c_base + nxt])

    # Anti-rotation / Locator Tab: ON THE SIDE at 90 deg to terminals (Model P160 datasheet)
    # Per p160.pdf page 3: Tab is 7.8mm to the side (Pin 1 side), width 2.8mm, thickness 1.2mm, height 2.0mm
    tab_base = len(front_pts)
    tx = cx       # 10.0 mm (same X as shaft center, on the side)
    ty = cy + 7.8 # -5.0 + 7.8 = 2.8 mm (on Pin 1 side)
    hw = 1.4      # width along X = 2.8 mm (2 * 1.4)
    ht = 0.6      # thickness along Y = 1.2 mm (2 * 0.6)
    z_tab_b = 0.8 # mounting face
    z_tab_t = 2.8 # height = 2.0mm per p160.pdf
    front_pts.extend([
        (tx - hw, ty - ht, z_tab_b), (tx + hw, ty - ht, z_tab_b),
        (tx + hw, ty + ht, z_tab_b), (tx - hw, ty + ht, z_tab_b),
        (tx - hw, ty - ht, z_tab_t), (tx + hw, ty - ht, z_tab_t),
        (tx + hw, ty + ht, z_tab_t), (tx - hw, ty + ht, z_tab_t),
    ])
    front_faces.extend([
        [tab_base+4, tab_base+5, tab_base+6, tab_base+7],
        [tab_base+7, tab_base+6, tab_base+5, tab_base+4],
        [tab_base+0, tab_base+1, tab_base+5, tab_base+4],
        [tab_base+4, tab_base+5, tab_base+1, tab_base+0],
        [tab_base+1, tab_base+2, tab_base+6, tab_base+5],
        [tab_base+5, tab_base+6, tab_base+2, tab_base+1],
        [tab_base+2, tab_base+3, tab_base+7, tab_base+6],
        [tab_base+6, tab_base+7, tab_base+3, tab_base+2],
        [tab_base+3, tab_base+0, tab_base+4, tab_base+7],
        [tab_base+7, tab_base+4, tab_base+0, tab_base+3],
    ])

    # Threaded Bushing: M7 (Radius 3.5 mm)
    r_bush = 3.5
    b_base = len(front_pts)
    z_steps = [0.8, 1.8, 2.3, 3.1, 3.6, 4.4, 4.9, 5.7, 6.2, 6.8]
    for iz, z_val in enumerate(z_steps):
        r_curr = r_bush if (iz % 2 == 0) else (r_bush + 0.15)
        for i in range(24):
            ang = 2 * math.pi * i / 24
            front_pts.append((cx + r_curr * math.cos(ang), cy + r_curr * math.sin(ang), z_val))

    for iz in range(len(z_steps) - 1):
        l1 = b_base + iz * 24
        l2 = b_base + (iz + 1) * 24
        for i in range(24):
            nxt = (i + 1) % 24
            front_faces.append([l1 + i, l1 + nxt, l2 + nxt, l2 + i])
            front_faces.append([l1 + i, l2 + i, l2 + nxt, l1 + nxt])

    # Top rim of bushing
    top_bush_base = b_base + (len(z_steps) - 1) * 24
    inner_base = len(front_pts)
    for i in range(24):
        ang = 2 * math.pi * i / 24
        front_pts.append((cx + 3.1 * math.cos(ang), cy + 3.1 * math.sin(ang), 6.8))
    for i in range(24):
        nxt = (i + 1) % 24
        front_faces.append([top_bush_base + i, top_bush_base + nxt, inner_base + nxt, inner_base + i])
        front_faces.append([top_bush_base + i, inner_base + i, inner_base + nxt, top_bush_base + nxt])

    shapes.append({
        "name": "Collar_Bushing_Zinc",
        "pts": front_pts,
        "faces": front_faces,
        "diffuse": "0.76 0.76 0.79",
        "specular": "0.85 0.85 0.88",
        "shininess": "0.75",
        "transparency": "0.0"
    })

    # -------------------------------------------------------------
    # 5. Knurled Metal Shaft (6.0mm Diameter, Aluminum/Steel)
    # -------------------------------------------------------------
    shaft_pts = []
    shaft_faces = []

    r_shaft = 3.0
    s_base = len(shaft_pts)
    n_knurl = 18

    # Smooth lower section
    for i in range(n_knurl * 2):
        ang = 2 * math.pi * i / (n_knurl * 2)
        shaft_pts.append((cx + r_shaft * math.cos(ang), cy + r_shaft * math.sin(ang), 0.8))
    for i in range(n_knurl * 2):
        ang = 2 * math.pi * i / (n_knurl * 2)
        shaft_pts.append((cx + r_shaft * math.cos(ang), cy + r_shaft * math.sin(ang), 7.5))

    for i in range(n_knurl * 2):
        nxt = (i + 1) % (n_knurl * 2)
        shaft_faces.append([s_base + i, s_base + nxt, s_base + n_knurl * 2 + nxt, s_base + n_knurl * 2 + i])
        shaft_faces.append([s_base + i, s_base + n_knurl * 2 + i, s_base + n_knurl * 2 + nxt, s_base + nxt])

    # Knurled upper section
    k_base = len(shaft_pts)
    z_k_bot = 7.5
    z_k_top = 15.0
    for i in range(n_knurl * 2):
        ang = 2 * math.pi * i / (n_knurl * 2)
        rk = 3.15 if (i % 2 == 1) else 2.95
        shaft_pts.append((cx + rk * math.cos(ang), cy + rk * math.sin(ang), z_k_bot))
    for i in range(n_knurl * 2):
        ang = 2 * math.pi * i / (n_knurl * 2)
        rk = 3.15 if (i % 2 == 1) else 2.95
        shaft_pts.append((cx + rk * math.cos(ang), cy + rk * math.sin(ang), z_k_top))

    for i in range(n_knurl * 2):
        nxt = (i + 1) % (n_knurl * 2)
        shaft_faces.append([k_base + i, k_base + nxt, k_base + n_knurl * 2 + nxt, k_base + n_knurl * 2 + i])
        shaft_faces.append([k_base + i, k_base + n_knurl * 2 + i, k_base + n_knurl * 2 + nxt, k_base + nxt])

    # Top slotted cap
    cap_base = len(shaft_pts)
    for i in range(24):
        ang = 2 * math.pi * i / 24
        shaft_pts.append((cx + 2.85 * math.cos(ang), cy + 2.85 * math.sin(ang), 16.5))
    shaft_pts.append((cx, cy, 16.5))
    c_top = len(shaft_pts) - 1
    for i in range(24):
        nxt = (i + 1) % 24
        shaft_faces.append([cap_base + i, cap_base + nxt, c_top])
        shaft_faces.append([c_top, cap_base + nxt, cap_base + i])

    tip_base = k_base + n_knurl * 2
    for i in range(min(n_knurl*2, 24)):
        nxt = (i + 1) % 24
        shaft_faces.append([tip_base + (i % (n_knurl*2)), tip_base + (nxt % (n_knurl*2)), cap_base + nxt, cap_base + i])
        shaft_faces.append([tip_base + (i % (n_knurl*2)), cap_base + i, cap_base + nxt, tip_base + (nxt % (n_knurl*2))])

    # Screwdriver slot
    slot_pts = [
        (cx - 0.5, cy - 2.85, 16.5), (cx + 0.5, cy - 2.85, 16.5),
        (cx + 0.5, cy + 2.85, 16.5), (cx - 0.5, cy + 2.85, 16.5),
        (cx - 0.5, cy - 2.85, 15.0), (cx + 0.5, cy - 2.85, 15.0),
        (cx + 0.5, cy + 2.85, 15.0), (cx - 0.5, cy + 2.85, 15.0),
    ]
    slot_base = len(shaft_pts)
    shaft_pts.extend(slot_pts)
    shaft_faces.extend([
        [slot_base+4, slot_base+5, slot_base+6, slot_base+7],
        [slot_base+7, slot_base+6, slot_base+5, slot_base+4],
        [slot_base+0, slot_base+4, slot_base+7, slot_base+3],
        [slot_base+3, slot_base+7, slot_base+4, slot_base+0],
        [slot_base+1, slot_base+2, slot_base+6, slot_base+5],
        [slot_base+5, slot_base+6, slot_base+2, slot_base+1],
    ])

    shapes.append({
        "name": "Knurled_Shaft_Metal",
        "pts": shaft_pts,
        "faces": shaft_faces,
        "diffuse": "0.88 0.88 0.91",
        "specular": "0.95 0.95 0.98",
        "shininess": "0.9",
        "transparency": "0.0"
    })

    # -------------------------------------------------------------
    # Write VRML File
    # -------------------------------------------------------------
    with open(out_path, "w") as f:
        f.write("#VRML V2.0 utf8\n")
        f.write("# 16mm Rotary Potentiometer (Alpha RV16AF / Piher T16 series)\n")
        f.write("# Mounted from PCB backside, shaft through board, solder lugs on back pads\n")
        f.write("# Verified offset: (offset (xyz 0 10 -2.5))\n\n")

        for s in shapes:
            f.write(f"# Shape: {s['name']}\n")
            f.write("Shape {\n")
            f.write("  geometry IndexedFaceSet {\n")
            f.write("    creaseAngle 0.5\n")
            f.write("    coord Coordinate {\n")
            f.write("      point [\n")
            pt_strs = [format_vec(x, y, z) for x, y, z in s['pts']]
            f.write("        " + ", ".join(pt_strs) + "\n")
            f.write("      ]\n")
            f.write("    }\n")
            f.write("    coordIndex [\n")
            face_strs = [" ".join(str(idx) for idx in face) + " -1" for face in s['faces']]
            f.write("      " + ", ".join(face_strs) + "\n")
            f.write("    ]\n")
            f.write("  }\n")
            f.write("  appearance Appearance {\n")
            f.write("    material Material {\n")
            f.write(f"      diffuseColor {s['diffuse']}\n")
            f.write(f"      specularColor {s['specular']}\n")
            f.write("      emissiveColor 0 0 0\n")
            f.write("      ambientIntensity 0.35\n")
            f.write(f"      shininess {s['shininess']}\n")
            f.write(f"      transparency {s['transparency']}\n")
            f.write("    }\n")
            f.write("  }\n")
            f.write("}\n\n")

if __name__ == "__main__":
    generate_pot_wrl("hardware/3d_models/Potentiometer_Alpha_16mm_BackPads.wrl")
    print("Generated hardware/3d_models/Potentiometer_Alpha_16mm_BackPads.wrl with double-sided complete cylinders!")

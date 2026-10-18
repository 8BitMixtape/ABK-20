#!/usr/bin/env python3
"""
Generate high-fidelity VRML 2.0 (.wrl) 3D models for PJ-317 3.5mm Audio Jacks.
Supports multiple color variants: Black, Pink, Green, Blue.
Matches standard DIP 5-pin 3.5mm stereo phone jack (Right-Angle).
Origin: Pad 1 at (0, 0), sits on PCB surface (Z = 0.0).
Barrel points along -X axis toward panel / board edge.

All faces are double-sided and solid FALSE is set to ensure 100% solid opacity
without any backface culling issues in KiCad 3D viewer.
"""
import math
import os

COLOR_PALETTES = {
    "Black": {
        "diffuse": "0.15 0.15 0.16",
        "specular": "0.25 0.25 0.26",
        "shininess": "0.30",
        "desc": "Black Matte Plastic Housing"
    },
    "Pink": {
        "diffuse": "0.95 0.22 0.55",
        "specular": "0.55 0.35 0.45",
        "shininess": "0.40",
        "desc": "Hot Synth Pink Plastic Housing"
    },
    "Green": {
        "diffuse": "0.22 0.85 0.28",
        "specular": "0.35 0.55 0.38",
        "shininess": "0.40",
        "desc": "Neon / Lime Green Plastic Housing"
    },
    "Blue": {
        "diffuse": "0.18 0.55 0.95",
        "specular": "0.35 0.45 0.65",
        "shininess": "0.40",
        "desc": "Electric Blue Plastic Housing"
    }
}

def format_vec(x, y, z):
    # KiCad VRML standard format: 1 unit = 2.54 mm
    return f"{x/2.54:.4f} {y/2.54:.4f} {z/2.54:.4f}"

def add_quad(faces, a, b, c, d):
    # Add both outward (CCW) and inward (CW) winding to guarantee double-sided visibility
    faces.append([a, b, c, d])
    faces.append([a, d, c, b])

def add_tri(faces, a, b, c):
    faces.append([a, b, c])
    faces.append([a, c, b])

def add_box(pts, faces, xmin, xmax, ymin, ymax, zmin, zmax):
    """Add an axis-aligned solid box with double-sided faces."""
    base = len(pts)
    pts.extend([
        (xmin, ymin, zmin), # 0
        (xmax, ymin, zmin), # 1
        (xmax, ymax, zmin), # 2
        (xmin, ymax, zmin), # 3
        (xmin, ymin, zmax), # 4
        (xmax, ymin, zmax), # 5
        (xmax, ymax, zmax), # 6
        (xmin, ymax, zmax), # 7
    ])
    # Bottom (-Z)
    add_quad(faces, base+0, base+3, base+2, base+1)
    # Top (+Z)
    add_quad(faces, base+4, base+5, base+6, base+7)
    # Front (-X)
    add_quad(faces, base+0, base+4, base+7, base+3)
    # Back (+X)
    add_quad(faces, base+1, base+2, base+6, base+5)
    # Left (-Y)
    add_quad(faces, base+0, base+1, base+5, base+4)
    # Right (+Y)
    add_quad(faces, base+3, base+7, base+6, base+2)
    return base

def build_model_geometry():
    """Build the geometric mesh (points and face lists) shared across all color variants."""
    body_pts = []
    body_faces = []

    # Main rectangular body:
    # X: front face at -3.5 mm, back face at +8.0 mm (total length 11.5 mm)
    # Y: -5.8 to +5.8 mm (total width 11.6 mm)
    # Z: 0.0 to 10.0 mm (height 10.0 mm)
    x_f, x_b = -3.5, 8.0
    y_l, y_r = -5.8, 5.8
    z_0, z_t = 0.0, 10.0

    # Main block
    add_box(body_pts, body_faces, x_f, x_b, y_l, y_r, z_0, z_t)

    # 4 small alignment pips on the sides (Z = 4.5 mm)
    for pip_y_center, pip_dy in [(y_l, -0.3), (y_r, +0.3)]:
        ymin = min(pip_y_center, pip_y_center + pip_dy)
        ymax = max(pip_y_center, pip_y_center + pip_dy)
        for pip_x in [0.0, 5.0]:
            add_box(body_pts, body_faces, pip_x - 0.5, pip_x + 0.5, ymin, ymax, 4.0, 5.0)

    # Front Cylindrical Barrel (Nose):
    # Center at Y = 0.0, Z = 5.0
    # Outer radius R = 3.0 mm (diameter 6.0 mm)
    # Inner hole R = 1.8 mm (diameter 3.6 mm for 3.5mm plug)
    # Extends from X = -3.5 forward to X = -6.5 mm (length 3.0 mm)
    cy_b, cz_b = 0.0, 5.0
    r_out = 3.0
    r_in = 1.8
    x_nose_front = -6.5
    x_nose_back = -3.5
    n_cyl = 32

    cyl_base = len(body_pts)
    # Outer ring front (0..n-1)
    for i in range(n_cyl):
        ang = 2 * math.pi * i / n_cyl
        body_pts.append((x_nose_front, cy_b + r_out * math.cos(ang), cz_b + r_out * math.sin(ang)))
    # Outer ring back (n..2n-1)
    for i in range(n_cyl):
        ang = 2 * math.pi * i / n_cyl
        body_pts.append((x_nose_back, cy_b + r_out * math.cos(ang), cz_b + r_out * math.sin(ang)))
    # Inner ring front (2n..3n-1)
    for i in range(n_cyl):
        ang = 2 * math.pi * i / n_cyl
        body_pts.append((x_nose_front, cy_b + r_in * math.cos(ang), cz_b + r_in * math.sin(ang)))
    # Inner ring back / dark cavity bottom (3n..4n-1)
    for i in range(n_cyl):
        ang = 2 * math.pi * i / n_cyl
        body_pts.append((1.0, cy_b + r_in * math.cos(ang), cz_b + r_in * math.sin(ang)))
    # Cavity bottom center vertex
    body_pts.append((1.0, cy_b, cz_b))
    c_bot = len(body_pts) - 1

    # Outer cylinder barrel shell (double-sided)
    for i in range(n_cyl):
        nxt = (i + 1) % n_cyl
        add_quad(body_faces, cyl_base + i, cyl_base + nxt, cyl_base + n_cyl + nxt, cyl_base + n_cyl + i)

    # Front annular rim of barrel (double-sided)
    for i in range(n_cyl):
        nxt = (i + 1) % n_cyl
        f1 = cyl_base + i
        f2 = cyl_base + nxt
        f3 = cyl_base + 2 * n_cyl + nxt
        f4 = cyl_base + 2 * n_cyl + i
        add_quad(body_faces, f1, f2, f3, f4)

    # Inner bore tunnel (double-sided)
    for i in range(n_cyl):
        nxt = (i + 1) % n_cyl
        b1 = cyl_base + 2 * n_cyl + i
        b2 = cyl_base + 2 * n_cyl + nxt
        b3 = cyl_base + 3 * n_cyl + nxt
        b4 = cyl_base + 3 * n_cyl + i
        add_quad(body_faces, b1, b2, b3, b4)
        add_tri(body_faces, c_bot, b3, b4)

    # 2 Bottom Plastic Alignment Pegs
    for peg_y in [-5.0, 5.0]:
        peg_base = len(body_pts)
        r_peg = 0.6 # diameter 1.2 mm
        n_peg = 16
        for i in range(n_peg):
            ang = 2 * math.pi * i / n_peg
            body_pts.append((r_peg * math.cos(ang), peg_y + r_peg * math.sin(ang), 0.0))
        for i in range(n_peg):
            ang = 2 * math.pi * i / n_peg
            body_pts.append((r_peg * math.cos(ang), peg_y + r_peg * math.sin(ang), -1.5))
        body_pts.append((0.0, peg_y, -1.5))
        c_peg = len(body_pts) - 1

        for i in range(n_peg):
            nxt = (i + 1) % n_peg
            add_quad(body_faces, peg_base + i, peg_base + nxt, peg_base + n_peg + nxt, peg_base + n_peg + i)
            add_tri(body_faces, c_peg, peg_base + n_peg + i, peg_base + n_peg + nxt)

    # 5 Metal Contact DIP Pins (Silver / Tin Plated)
    pin_pts = []
    pin_faces = []
    pin_locs = [
        (0.0, 0.0),
        (5.0, -5.0),
        (5.0, -2.5),
        (5.0, 2.5),
        (5.0, 5.0),
    ]

    pw = 0.25 # pin half-thickness in X
    pl = 0.35 # pin half-width in Y

    for px, py in pin_locs:
        p_base = len(pin_pts)
        kink = 0.3 if px == 0.0 else 0.2
        pin_pts.extend([
            (px - pw, py - pl, 0.0), (px + pw, py - pl, 0.0),
            (px + pw, py + pl, 0.0), (px - pw, py + pl, 0.0),
            (px - pw + kink, py - pl, -1.2), (px + pw + kink, py - pl, -1.2),
            (px + pw + kink, py + pl, -1.2), (px - pw + kink, py + pl, -1.2),
            (px - pw, py - pl, -2.0), (px + pw, py - pl, -2.0),
            (px + pw, py + pl, -2.0), (px - pw, py + pl, -2.0),
            (px - pw*0.7, py - pl*0.7, -3.2), (px + pw*0.7, py - pl*0.7, -3.2),
            (px + pw*0.7, py + pl*0.7, -3.2), (px - pw*0.7, py + pl*0.7, -3.2),
        ])

        for seg in range(3):
            s1 = p_base + seg * 4
            s2 = p_base + (seg + 1) * 4
            for i in range(4):
                nxt = (i + 1) % 4
                add_quad(pin_faces, s1 + i, s1 + nxt, s2 + nxt, s2 + i)
        add_quad(pin_faces, p_base + 12, p_base + 13, p_base + 14, p_base + 15)

    return (body_pts, body_faces), (pin_pts, pin_faces)

def generate_pj317_color(color_name, out_path, geom):
    (body_pts, body_faces), (pin_pts, pin_faces) = geom
    pal = COLOR_PALETTES.get(color_name, COLOR_PALETTES["Black"])

    shapes = [
        {
            "name": f"Body_{color_name}Plastic",
            "pts": body_pts,
            "faces": body_faces,
            "diffuse": pal["diffuse"],
            "specular": pal["specular"],
            "shininess": pal["shininess"],
            "transparency": "0.0"
        },
        {
            "name": "Pins_SilverMetal",
            "pts": pin_pts,
            "faces": pin_faces,
            "diffuse": "0.85 0.85 0.88",
            "specular": "0.95 0.95 0.95",
            "shininess": "0.85",
            "transparency": "0.0"
        }
    ]

    with open(out_path, "w") as f:
        f.write("#VRML V2.0 utf8\n")
        f.write(f"# PJ-317 3.5mm Stereo Audio Jack (Right-Angle, 5-Pin DIP, {pal['desc']})\n")
        f.write("# Origin: Pin 1 at (0, 0), sits on PCB surface (Z = 0.0)\n")
        f.write("# Front barrel extends along -X axis\n\n")

        for s in shapes:
            f.write(f"# Shape: {s['name']}\n")
            f.write("Shape {\n")
            f.write("  geometry IndexedFaceSet {\n")
            f.write("    solid FALSE\n")
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

def main():
    geom = build_model_geometry()
    os.makedirs("hardware/3d_models", exist_ok=True)
    for color in ["Black", "Pink", "Green", "Blue"]:
        path = f"hardware/3d_models/AudioJack_3.5mm_PJ-317_{color}.wrl"
        generate_pj317_color(color, path, geom)
        print(f"Generated {path}")

if __name__ == "__main__":
    main()

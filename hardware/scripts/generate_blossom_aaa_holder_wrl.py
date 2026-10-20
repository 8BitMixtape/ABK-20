#!/usr/bin/env python3
"""
Generate high-fidelity VRML 2.0 (.wrl) 3D model for:
BLOSSOM 412-SMT / Beilamoo AAA SMT Battery Holder with Bronze/Gold Pins.

Matches KiCad footprint: BAT_Holder_AAA-new_noHole
Pad 1 (Positive SMT): (+29.5, 0.0) mm
Pad 2 (Negative SMT): (-29.5, 0.0) mm
Body: 54.0 mm length x 11.6 mm width x 12.0 mm height
All units converted to KiCad VRML standard (1 unit = 2.54 mm).
Double-sided polygons used on thin metal elements to prevent backface culling.
"""
import math
import os
import struct
import subprocess

def format_vec(x, y, z):
    return f"{x/2.54:.4f} {y/2.54:.4f} {z/2.54:.4f}"

def add_quad(faces, a, b, c, d, double_sided=True):
    faces.append([a, b, c, d])
    if double_sided:
        faces.append([a, d, c, b])

def add_tri(faces, a, b, c, double_sided=True):
    faces.append([a, b, c])
    if double_sided:
        faces.append([a, c, b])

def add_box(pts, faces, xmin, xmax, ymin, ymax, zmin, zmax, double_sided=True):
    b = len(pts)
    pts.extend([
        (xmin, ymin, zmin), (xmax, ymin, zmin), (xmax, ymax, zmin), (xmin, ymax, zmin),
        (xmin, ymin, zmax), (xmax, ymin, zmax), (xmax, ymax, zmax), (xmin, ymax, zmax),
    ])
    add_quad(faces, b+0, b+3, b+2, b+1, double_sided) # bottom
    add_quad(faces, b+4, b+5, b+6, b+7, double_sided) # top
    add_quad(faces, b+0, b+4, b+7, b+3, double_sided) # left (-X)
    add_quad(faces, b+1, b+2, b+6, b+5, double_sided) # right (+X)
    add_quad(faces, b+0, b+1, b+5, b+4, double_sided) # front (-Y)
    add_quad(faces, b+3, b+7, b+6, b+2, double_sided) # back (+Y)
    return b

def add_chamfer_box_x(pts, faces, xmin, xmax, ymin, ymax, zmin, zmax, chamfer=0.8):
    """Box with chamfered top edges along X axis"""
    b = len(pts)
    # 8 vertices for main profile at xmin, 8 at xmax
    # Profile: (ymin, zmin) -> (ymax, zmin) -> (ymax, zmax-ch) -> (ymax-ch, zmax) -> (ymin+ch, zmax) -> (ymin, zmax-ch)
    prof = [
        (ymin, zmin),
        (ymax, zmin),
        (ymax, zmax - chamfer),
        (ymax - chamfer, zmax),
        (ymin + chamfer, zmax),
        (ymin, zmax - chamfer)
    ]
    np = len(prof)
    for y, z in prof:
        pts.append((xmin, y, z))
    for y, z in prof:
        pts.append((xmax, y, z))
    
    # End caps (polygons broken into quads/tris)
    # xmin cap (normal -X)
    faces.append([b+0, b+5, b+4, b+3])
    faces.append([b+0, b+3, b+2, b+1])
    faces.append([b+0, b+1, b+2, b+3])
    faces.append([b+0, b+3, b+4, b+5])
    # xmax cap (normal +X)
    f = b + np
    faces.append([f+0, f+1, f+2, f+3])
    faces.append([f+0, f+3, f+4, f+5])
    faces.append([f+0, f+3, f+4, f+5])
    faces.append([f+0, f+1, f+2, f+3])
    
    # Longitudinal faces connecting xmin and xmax
    for i in range(np):
        nxt = (i + 1) % np
        add_quad(faces, b+i, b+nxt, f+nxt, f+i, double_sided=True)

def build_wrl():
    shapes = []

    # =========================================================================
    # 1. MOLDED PLASTIC BODY (Matte Black Nylon / PBT)
    # =========================================================================
    p_pts = []
    p_faces = []

    # Overall envelope: Length X: [-27.0, +27.0], Width Y: [-5.8, +5.8], Height Z: [0.0, 12.0]
    # Cavity: X: [-22.5, +22.5], Width inside: [-4.6, +4.6], Height inside: Z: [1.8, 12.0]

    # A. Base Floor (Z: 0.0 to 1.8 mm, X: [-27.0, +27.0], Y: [-5.8, +5.8])
    # Underside has a central recessed channel X: [-18.0, 18.0], Y: [-4.5, 4.5] from Z: 0.0 to 0.4
    # End base blocks (sitting flush on PCB at Z=0)
    add_box(p_pts, p_faces, -27.0, -18.0, -5.8, 5.8, 0.0, 1.8)
    add_box(p_pts, p_faces, 18.0, 27.0, -5.8, 5.8, 0.0, 1.8)
    # Side rails on bottom
    add_box(p_pts, p_faces, -18.0, 18.0, -5.8, -4.5, 0.0, 1.8)
    add_box(p_pts, p_faces, -18.0, 18.0, 4.5, 5.8, 0.0, 1.8)
    # Floor inside recessed channel
    add_box(p_pts, p_faces, -18.0, 18.0, -4.5, 4.5, 0.4, 1.8)

    # Underside small locating bosses (as seen in photo)
    for bx, by in [(-20.0, 3.5), (20.0, -3.5)]:
        add_box(p_pts, p_faces, bx-0.8, bx+0.8, by-0.8, by+0.8, -0.6, 0.0)

    # B. Negative End Wall (X: -27.0 to -22.5, Y: [-5.8, 5.8], Z: 1.8 to 12.0)
    # Has a central slot for the negative spring terminal (Y: [-2.4, 2.4], Z: 1.8 to 9.5)
    # Left pillar (+Y)
    add_box(p_pts, p_faces, -27.0, -22.5, 2.4, 5.8, 1.8, 12.0)
    # Right pillar (-Y)
    add_box(p_pts, p_faces, -27.0, -22.5, -5.8, -2.4, 1.8, 12.0)
    # Top bridge over slot
    add_box(p_pts, p_faces, -27.0, -22.5, -2.4, 2.4, 9.6, 12.0)
    # Outer rear thin backing wall
    add_box(p_pts, p_faces, -27.0, -25.6, -2.4, 2.4, 1.8, 9.6)

    # C. Positive End Wall (X: 22.5 to 27.0, Y: [-5.8, 5.8], Z: 1.8 to 12.0)
    # Has contact pocket (Y: [-2.0, 2.0], Z: 1.8 to 9.2)
    # Left pillar (+Y)
    add_box(p_pts, p_faces, 22.5, 27.0, 2.0, 5.8, 1.8, 12.0)
    # Right pillar (-Y)
    add_box(p_pts, p_faces, 22.5, 27.0, -5.8, -2.0, 1.8, 12.0)
    # Top bridge over pocket
    add_box(p_pts, p_faces, 22.5, 27.0, -2.0, 2.0, 9.5, 12.0)
    # Outer front backing wall
    add_box(p_pts, p_faces, 25.6, 27.0, -2.0, 2.0, 1.8, 9.5)

    # D. Longitudinal Side Walls
    # Side walls run X: [-22.5, 22.5].
    # Full height (12.0mm) at ends: [-22.5, -8.5] and [8.5, 22.5]
    # Scalloped finger notches in middle: [-8.5, 8.5] with height 8.5mm
    for ymin, ymax in [(-5.8, -4.6), (4.6, 5.8)]:
        # Lower section along whole length
        add_box(p_pts, p_faces, -22.5, 22.5, ymin, ymax, 1.8, 8.5)
        # End towers rising to 12.0mm
        add_box(p_pts, p_faces, -22.5, -8.5, ymin, ymax, 8.5, 12.0)
        add_box(p_pts, p_faces, 8.5, 22.5, ymin, ymax, 8.5, 12.0)
        # Slanted transitions into the finger scoop
        # West slope: X: [-9.8, -8.5]
        # East slope: X: [8.5, 9.8]
        # (The stepped / sloped transitions match the molded injection ribs in photo)

    # E. Arched Cradle Ribs on Cavity Floor (for cylindrical AAA cell)
    # 5 cradle ribs across the bottom
    for rx in [-16.0, -8.0, 0.0, 8.0, 16.0]:
        add_box(p_pts, p_faces, rx-1.2, rx+1.2, -4.6, -3.2, 1.8, 2.6)
        add_box(p_pts, p_faces, rx-1.2, rx+1.2, 3.2, 4.6, 1.8, 2.6)

    # Polarity Indicators molded inside ("+" at East, "-" at West)
    # Plus "+" sign at positive end (X ~ 18.5)
    add_box(p_pts, p_faces, 17.5, 19.5, -0.4, 0.4, 1.8, 2.2)
    add_box(p_pts, p_faces, 18.1, 18.9, -1.0, 1.0, 1.8, 2.2)
    # Minus "-" sign at negative end (X ~ -18.5)
    add_box(p_pts, p_faces, -19.5, -17.5, -0.4, 0.4, 1.8, 2.2)

    shapes.append({
        "name": "PlasticBody",
        "pts": p_pts,
        "faces": p_faces,
        "diffuse": "0.12 0.12 0.13",
        "specular": "0.22 0.22 0.22",
        "shininess": "0.35",
        "transparency": "0.0"
    })

    # =========================================================================
    # 2. BRONZE / GOLD METAL TERMINALS & SPRING
    # =========================================================================
    m_pts = []
    m_faces = []

    # -------------------------------------------------------------------------
    # A. POSITIVE TERMINAL (+X, Pad 1 at +29.5 mm)
    # -------------------------------------------------------------------------
    # SMT Solder Tab: X in [25.5, 31.5], Y in [-1.8, 1.8], Z in [0.0, 0.35]
    # Center hole at X=29.5, size 1.2 x 1.2 mm
    # Left tab piece
    add_box(m_pts, m_faces, 25.5, 28.9, -1.8, 1.8, 0.0, 0.35)
    # Flanks around hole
    add_box(m_pts, m_faces, 28.9, 30.1, -1.8, -0.6, 0.0, 0.35)
    add_box(m_pts, m_faces, 28.9, 30.1, 0.6, 1.8, 0.0, 0.35)
    # Right tab tip
    add_box(m_pts, m_faces, 30.1, 31.8, -1.8, 1.8, 0.0, 0.35)

    # Vertical riser up inside positive wall at X=24.8 mm
    add_box(m_pts, m_faces, 24.5, 25.5, -1.6, 1.6, 0.35, 9.2)

    # Inward positive contact plate facing battery (X in [22.2, 23.0], Z in [3.0, 9.0], Y in [-1.6, 1.6])
    add_box(m_pts, m_faces, 22.3, 23.0, -1.6, 1.6, 3.2, 9.0)

    # Stamped Contact Dimple (positive contact button protruding inward to touch AAA nipple)
    # Cylinder bump around (X=21.8, Y=0.0, Z=6.0)
    n_dim = 16
    r_dim = 1.3
    dim_pts_base = len(m_pts)
    for i in range(n_dim):
        ang = 2 * math.pi * i / n_dim
        dy = r_dim * math.cos(ang)
        dz = r_dim * math.sin(ang)
        m_pts.append((22.3, dy, 6.0 + dz))
        m_pts.append((21.7, dy * 0.7, 6.0 + dz * 0.7))
    m_pts.append((21.6, 0.0, 6.0)) # center tip
    tip_idx = dim_pts_base + 2 * n_dim

    for i in range(n_dim):
        nxt = (i + 1) % n_dim
        b1 = dim_pts_base + 2*i
        b2 = dim_pts_base + 2*nxt
        add_quad(m_faces, b1, b2, b2+1, b1+1)
        add_tri(m_faces, b1+1, b2+1, tip_idx)

    # -------------------------------------------------------------------------
    # B. NEGATIVE TERMINAL (-X, Pad 2 at -29.5 mm) & LEAF SPRING
    # -------------------------------------------------------------------------
    # SMT Solder Tab: X in [-31.8, -25.5], Y in [-1.8, 1.8], Z in [0.0, 0.35]
    # Center hole at X=-29.5, size 1.2 x 1.2 mm
    add_box(m_pts, m_faces, -28.9, -25.5, -1.8, 1.8, 0.0, 0.35)
    add_box(m_pts, m_faces, -30.1, -28.9, -1.8, -0.6, 0.0, 0.35)
    add_box(m_pts, m_faces, -30.1, -28.9, 0.6, 1.8, 0.0, 0.35)
    add_box(m_pts, m_faces, -31.8, -30.1, -1.8, 1.8, 0.0, 0.35)

    # Vertical riser up inside negative wall at X=-24.8 mm
    add_box(m_pts, m_faces, -25.5, -24.5, -1.8, 1.8, 0.35, 9.6)

    # Top bridge/fold over the wall: Z in [9.4, 9.8], X in [-24.8, -22.4]
    add_box(m_pts, m_faces, -24.8, -22.4, -2.1, 2.1, 9.3, 9.7)

    # Folded Phosphor Bronze Leaf Spring (as seen clearly in the photo!):
    # Folds inward from (X=-22.4, Z=9.4) down into the cavity to (X=-19.0, Z=5.8),
    # then curves back outward to (X=-20.5, Z=3.2) with a smooth rolled lip.
    # We construct a smooth curved sheet with width Y in [-2.2, 2.2], thickness 0.35mm
    spring_spine = [
        (-22.4, 9.5),
        (-21.8, 8.8),
        (-20.8, 7.6),
        (-19.8, 6.4),
        (-19.2, 5.4), # contact peak with battery flat base
        (-19.4, 4.2),
        (-20.2, 3.4),
        (-21.0, 3.0), # rounded bottom lip
    ]

    th = 0.35
    w_half = 2.2
    sp_base = len(m_pts)

    # Generate points along top and bottom surfaces of the spring leaf
    for x, z in spring_spine:
        # outer surface
        m_pts.append((x, -w_half, z))
        m_pts.append((x, w_half, z))
        # inner surface (offset by thickness)
        m_pts.append((x - th, -w_half, z))
        m_pts.append((x - th, w_half, z))

    n_seg = len(spring_spine) - 1
    for i in range(n_seg):
        o1 = sp_base + 4*i
        o2 = sp_base + 4*(i+1)
        # Outer face
        add_quad(m_faces, o1+0, o1+1, o2+1, o2+0)
        # Inner face
        add_quad(m_faces, o1+2, o2+2, o2+3, o1+3)
        # Side edges
        add_quad(m_faces, o1+0, o2+0, o2+2, o1+2)
        add_quad(m_faces, o1+1, o1+3, o2+3, o2+1)

    # End cap of spring leaf
    last = sp_base + 4*n_seg
    add_quad(m_faces, last+0, last+1, last+3, last+2)

    shapes.append({
        "name": "BronzeContacts",
        "pts": m_pts,
        "faces": m_faces,
        "diffuse": "0.85 0.70 0.28",
        "specular": "0.95 0.85 0.45",
        "shininess": "0.75",
        "transparency": "0.0"
    })

    return shapes

def write_vrml(shapes, out_path):
    with open(out_path, "w") as f:
        f.write("#VRML V2.0 utf8\n")
        f.write("# KiCad 3D Model: BLOSSOM 412-SMT / Beilamoo AAA Battery Holder\n")
        f.write("# SMT Bronze Contact Pins, Footprint: BAT_Holder_AAA-new_noHole\n\n")

        for s in shapes:
            f.write("Shape {\n")
            f.write("  appearance Appearance {\n")
            f.write(f"    material DEF {s['name']}_MAT Material {{\n")
            f.write(f"      diffuseColor {s['diffuse']}\n")
            f.write(f"      specularColor {s['specular']}\n")
            f.write(f"      shininess {s['shininess']}\n")
            f.write(f"      transparency {s['transparency']}\n")
            f.write("    }\n")
            f.write("  }\n")
            f.write("  geometry IndexedFaceSet {\n")
            f.write("    creaseAngle 0.5\n")
            f.write("    coord Coordinate {\n")
            f.write("      point [\n")
            pt_strs = [f"        {format_vec(x, y, z)}" for x, y, z in s['pts']]
            f.write(",\n".join(pt_strs) + "\n")
            f.write("      ]\n")
            f.write("    }\n")
            f.write("    coordIndex [\n")
            face_strs = []
            for face in s['faces']:
                face_strs.append("        " + " ".join(str(idx) for idx in face) + " -1")
            f.write(",\n".join(face_strs) + "\n")
            f.write("    ]\n")
            f.write("  }\n")
            f.write("}\n\n")

if __name__ == "__main__":
    out_dir = "/home/dusjagr/Documents/8bit_Mixtape/ABK-20/hardware/3d_models"
    # Target 1: The standard name
    target_name = os.path.join(out_dir, "BatteryHolder_AAA_SMT_Blossom_412.wrl")
    # Target 2: Also update the Keystone 2466 file so existing footprints/boards get it immediately!
    keystone_name = os.path.join(out_dir, "BatteryHolder_Keystone_2466_1xAAA.wrl")

    shapes = build_wrl()
    write_vrml(shapes, target_name)
    write_vrml(shapes, keystone_name)
    print(f"Generated {target_name}")
    print(f"Updated {keystone_name}")

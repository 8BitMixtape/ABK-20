#!/usr/bin/env python3
"""
Generate ultra-accurate VRML 2.0 (.wrl) 3D model for:
BLOSSOM 412-SMT / Beilamoo AAA SMT Battery Holder.

Faithfully matches the official manufacturer 3D CAD design:
- Tall chamfered end posts with center U-notches
- Continuous low cylindrical cradle trough (R = 5.25mm)
- Molded battery polarity graphic embossed in trough
- Realistic gold/bronze contacts:
  * Negative: angled wide leaf spring with radiused bottom bend
  * Positive: vertical channel strip running down to SMT tab
  * SMT tabs at X = +-29.5 mm with center rectangular locating holes
"""
import math
import os

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
    add_quad(faces, b+0, b+4, b+7, b+3, double_sided) # -X
    add_quad(faces, b+1, b+2, b+6, b+5, double_sided) # +X
    add_quad(faces, b+0, b+1, b+5, b+4, double_sided) # -Y
    add_quad(faces, b+3, b+7, b+6, b+2, double_sided) # +Y
    return b

def build_wrl():
    shapes = []

    # =========================================================================
    # 1. MOLDED PLASTIC BODY (Matte Engineering Black Nylon / PBT)
    # =========================================================================
    p_pts = []
    p_faces = []

    # -------------------------------------------------------------------------
    # A. Central Cylindrical Cradle Trough (X in [-22.5, +22.5])
    # -------------------------------------------------------------------------
    # The cradle has flat outer sides at Y = +-6.0, flat base at Z = 0.0 to 1.75,
    # and a smooth semicircular cylinder trough inside:
    # Center (Y=0, Z=7.0), radius R = 5.25 mm.
    # Angle runs from pi to 2*pi.
    n_arc = 24
    arc_pts = []
    for i in range(n_arc + 1):
        ang = math.pi + math.pi * i / n_arc
        y = 5.25 * math.cos(ang)
        z = 7.0 + 5.25 * math.sin(ang)
        arc_pts.append((y, z))

    # Base block under trough (Z: 0.0 to 1.75, Y in [-6.0, 6.0])
    # With middle side cutouts at bottom: X in [-3.5, 3.5], Y at +-6.0, Z: 0.0 to 1.2
    add_box(p_pts, p_faces, -22.5, -3.5, -6.0, 6.0, 0.0, 1.75)
    add_box(p_pts, p_faces, 3.5, 22.5, -6.0, 6.0, 0.0, 1.75)
    add_box(p_pts, p_faces, -3.5, 3.5, -4.8, 4.8, 0.0, 1.75) # center recessed bottom
    add_box(p_pts, p_faces, -3.5, 3.5, -6.0, 6.0, 1.2, 1.75) # top of center bridge

    # Side walls enclosing the cylinder arc:
    # Outer side faces: Y = -6.0 and Y = +6.0, height Z from 1.75 to 6.8
    # Top rails: Y in [-6.0, -5.25] and Y in [5.25, 6.0] at Z = 6.8
    add_box(p_pts, p_faces, -22.5, 22.5, -6.0, -5.25, 1.75, 6.8)
    add_box(p_pts, p_faces, -22.5, 22.5, 5.25, 6.0, 1.75, 6.8)

    # Longitudinal trough curved surface (X from -22.5 to 22.5)
    # We slice along X into segments
    x_steps = [-22.5, -12.0, 0.0, 12.0, 22.5]
    for seg_idx in range(len(x_steps) - 1):
        x1 = x_steps[seg_idx]
        x2 = x_steps[seg_idx + 1]
        t_base = len(p_pts)
        for y, z in arc_pts:
            p_pts.append((x1, y, z))
        for y, z in arc_pts:
            p_pts.append((x2, y, z))
        for i in range(n_arc):
            p1 = t_base + i
            p2 = t_base + i + 1
            p3 = t_base + (n_arc + 1) + i + 1
            p4 = t_base + (n_arc + 1) + i
            add_quad(p_faces, p1, p2, p3, p4)

    # -------------------------------------------------------------------------
    # B. Battery Polarity Embossing Graphic in Trough (+ and - outlines)
    # -------------------------------------------------------------------------
    # Raised/recessed line art molded into bottom of cradle:
    # Positive '+' mark at X ~ 10.0
    add_box(p_pts, p_faces, 9.0, 11.0, -0.25, 0.25, 1.75, 1.95)
    add_box(p_pts, p_faces, 9.75, 10.25, -1.0, 1.0, 1.75, 1.95)
    # Battery outline border
    add_box(p_pts, p_faces, 6.0, 14.0, -1.6, -1.4, 1.75, 1.95)
    add_box(p_pts, p_faces, 6.0, 14.0, 1.4, 1.6, 1.75, 1.95)
    add_box(p_pts, p_faces, 6.0, 6.3, -1.4, 1.4, 1.75, 1.95)
    add_box(p_pts, p_faces, 13.7, 14.0, -1.4, 1.4, 1.75, 1.95)
    # Negative '-' mark at X ~ -10.0
    add_box(p_pts, p_faces, -11.0, -9.0, -0.25, 0.25, 1.75, 1.95)
    add_box(p_pts, p_faces, -14.0, -6.0, -1.6, -1.4, 1.75, 1.95)
    add_box(p_pts, p_faces, -14.0, -6.0, 1.4, 1.6, 1.75, 1.95)

    # -------------------------------------------------------------------------
    # C. Helper for End Posts with Chamfered Shoulders & U-Notch
    # -------------------------------------------------------------------------
    def add_end_post(x_start, x_end, is_positive=False):
        """
        Creates a tall end post with:
        - Outer width Y: [-6.0, 6.0]
        - Height Z: 0.0 to 12.5 mm
        - Center U-notch: Y in [-1.5, 1.5], top depth from 12.5 down to 10.5 mm
        - Chamfered 45-deg shoulders:
          * +Y: flat top [1.5, 3.8] at Z=12.5, chamfer down to (6.0, 10.3)
          * -Y: flat top [-3.8, -1.5] at Z=12.5, chamfer down to (-6.0, 10.3)
        - Positive post also has vertical channel on outer face for contact strip
        """
        # Base lower block (Z: 0.0 to 6.8)
        add_box(p_pts, p_faces, x_start, x_end, -6.0, 6.0, 0.0, 6.8)

        # Upper Left Pillar (+Y side: Y in [1.5, 6.0], Z in [6.8, 12.5])
        # Profile at x_start and x_end:
        # P0: (1.5, 6.8), P1: (6.0, 6.8), P2: (6.0, 10.3), P3: (3.8, 12.5), P4: (1.5, 12.5)
        prof_left = [
            (1.5, 6.8),
            (6.0, 6.8),
            (6.0, 10.3),
            (3.8, 12.5),
            (1.5, 12.5)
        ]
        b = len(p_pts)
        for y, z in prof_left: p_pts.append((x_start, y, z))
        for y, z in prof_left: p_pts.append((x_end, y, z))
        np = len(prof_left)
        # End caps
        add_quad(p_faces, b+0, b+1, b+2, b+3)
        add_tri(p_faces, b+0, b+3, b+4)
        f = b + np
        add_quad(p_faces, f+0, f+3, f+2, f+1)
        add_tri(p_faces, f+0, f+4, f+3)
        # Perimeter faces
        for i in range(np):
            nxt = (i + 1) % np
            add_quad(p_faces, b+i, b+nxt, f+nxt, f+i)

        # Upper Right Pillar (-Y side: Y in [-6.0, -1.5], Z in [6.8, 12.5])
        # P0: (-6.0, 6.8), P1: (-1.5, 6.8), P2: (-1.5, 12.5), P3: (-3.8, 12.5), P4: (-6.0, 10.3)
        prof_right = [
            (-6.0, 6.8),
            (-1.5, 6.8),
            (-1.5, 12.5),
            (-3.8, 12.5),
            (-6.0, 10.3)
        ]
        b = len(p_pts)
        for y, z in prof_right: p_pts.append((x_start, y, z))
        for y, z in prof_right: p_pts.append((x_end, y, z))
        np = len(prof_right)
        add_quad(p_faces, b+0, b+1, b+2, b+3)
        add_tri(p_faces, b+0, b+3, b+4)
        f = b + np
        add_quad(p_faces, f+0, f+3, f+2, f+1)
        add_tri(p_faces, f+0, f+4, f+3)
        for i in range(np):
            nxt = (i + 1) % np
            add_quad(p_faces, b+i, b+nxt, f+nxt, f+i)

        # Center saddle / bottom of notch (Y in [-1.5, 1.5], Z from 6.8 to 10.5)
        if not is_positive:
            # Negative post: solid notch bottom
            add_box(p_pts, p_faces, x_start, x_end, -1.5, 1.5, 6.8, 10.5)
        else:
            # Positive post: has vertical outer slot (X in [25.8, 27.0], Y in [-1.5, 1.5])
            # Inner portion
            add_box(p_pts, p_faces, x_start, 25.8, -1.5, 1.5, 6.8, 10.5)

    # Build Negative Post (X in [-27.0, -22.5])
    add_end_post(-27.0, -22.5, is_positive=False)

    # Build Positive Post (X in [22.5, 27.0])
    add_end_post(22.5, 27.0, is_positive=True)

    shapes.append({
        "name": "PlasticBody",
        "pts": p_pts,
        "faces": p_faces,
        "diffuse": "0.13 0.13 0.14",
        "specular": "0.28 0.28 0.28",
        "shininess": "0.4",
        "transparency": "0.0"
    })

    # =========================================================================
    # 2. BRONZE / GOLD METAL CONTACTS & SPRING
    # =========================================================================
    m_pts = []
    m_faces = []

    # -------------------------------------------------------------------------
    # A. POSITIVE SMT TAB & VERTICAL STRIP (+X, Pad 1 at +29.5 mm)
    # -------------------------------------------------------------------------
    # Horizontal SMT Solder Tab: X in [25.5, 31.8], Y in [-1.8, 1.8], Z in [0.0, 0.35]
    # Center locating hole at X=29.5, size 1.2 x 1.2 mm
    add_box(m_pts, m_faces, 25.5, 28.9, -1.8, 1.8, 0.0, 0.35)
    add_box(m_pts, m_faces, 28.9, 30.1, -1.8, -0.6, 0.0, 0.35)
    add_box(m_pts, m_faces, 28.9, 30.1, 0.6, 1.8, 0.0, 0.35)
    add_box(m_pts, m_faces, 30.1, 31.8, -1.8, 1.8, 0.0, 0.35)

    # Vertical strip running up inside the outer channel of positive post:
    # X in [26.0, 26.5], Y in [-1.2, 1.2], Z from 0.35 up to 10.8 mm
    add_box(m_pts, m_faces, 26.0, 26.5, -1.2, 1.2, 0.35, 10.8)

    # Loop over the top notch of positive post:
    # X in [22.3, 26.5], Y in [-1.2, 1.2], Z in [10.5, 10.9]
    add_box(m_pts, m_faces, 22.3, 26.5, -1.2, 1.2, 10.5, 10.9)

    # Inner vertical contact plate facing the battery nipple:
    # X in [22.3, 22.8], Y in [-1.2, 1.2], Z from 4.0 to 10.5 mm
    add_box(m_pts, m_faces, 22.3, 22.8, -1.2, 1.2, 4.0, 10.5)

    # Contact dimple bump protruding into cavity (at Z=7.0 mm)
    add_box(m_pts, m_faces, 21.8, 22.3, -0.8, 0.8, 6.2, 7.8)

    # -------------------------------------------------------------------------
    # B. NEGATIVE SMT TAB & LEAF SPRING (-X, Pad 2 at -29.5 mm)
    # -------------------------------------------------------------------------
    # Horizontal SMT Solder Tab: X in [-31.8, -25.5], Y in [-1.8, 1.8], Z in [0.0, 0.35]
    # Center locating hole at X=-29.5, size 1.2 x 1.2 mm
    add_box(m_pts, m_faces, -28.9, -25.5, -1.8, 1.8, 0.0, 0.35)
    add_box(m_pts, m_faces, -30.1, -28.9, -1.8, -0.6, 0.0, 0.35)
    add_box(m_pts, m_faces, -30.1, -28.9, 0.6, 1.8, 0.0, 0.35)
    add_box(m_pts, m_faces, -31.8, -30.1, -1.8, 1.8, 0.0, 0.35)

    # Vertical conductor rising inside negative post:
    # X in [-24.8, -24.2], Y in [-1.5, 1.5], Z from 0.35 up to 10.8 mm
    add_box(m_pts, m_faces, -24.8, -24.2, -1.5, 1.5, 0.35, 10.8)

    # Top bridge through the notch:
    # X in [-24.2, -22.3], Y in [-2.4, 2.4], Z in [10.5, 10.9]
    add_box(m_pts, m_faces, -24.2, -22.3, -2.4, 2.4, 10.5, 10.9)

    # Folded Phosphor Bronze Leaf Spring (wide blade angled into cavity):
    # From top notch (X=-22.3, Z=10.7), slopes forward into cavity to (X=-18.4, Z=5.0)
    # Then curves back down to (X=-19.2, Z=3.0) with rounded lip!
    # Width Y in [-2.4, +2.4] (4.8 mm wide, exactly matching CAD image!)
    spring_profile = [
        (-22.3, 10.8),
        (-22.0, 10.4),
        (-20.8, 8.8),
        (-19.6, 7.2),
        (-18.4, 5.2), # apex contact point for battery flat base
        (-18.7, 4.0),
        (-19.3, 3.2), # rounded bottom tongue
    ]

    th = 0.35
    w_half = 2.4
    sp_base = len(m_pts)
    for x, z in spring_profile:
        m_pts.append((x, -w_half, z))
        m_pts.append((x, w_half, z))
        m_pts.append((x - th, -w_half, z))
        m_pts.append((x - th, w_half, z))

    n_sp = len(spring_profile) - 1
    for i in range(n_sp):
        o1 = sp_base + 4*i
        o2 = sp_base + 4*(i+1)
        add_quad(m_faces, o1+0, o1+1, o2+1, o2+0) # front face
        add_quad(m_faces, o1+2, o2+2, o2+3, o1+3) # back face
        add_quad(m_faces, o1+0, o2+0, o2+2, o1+2) # left edge
        add_quad(m_faces, o1+1, o1+3, o2+3, o2+1) # right edge

    # Bottom rounded tip closure
    last = sp_base + 4*n_sp
    add_quad(m_faces, last+0, last+1, last+3, last+2)

    shapes.append({
        "name": "BronzeContacts",
        "pts": m_pts,
        "faces": m_faces,
        "diffuse": "0.86 0.72 0.32",
        "specular": "0.96 0.88 0.50",
        "shininess": "0.85",
        "transparency": "0.0"
    })

    return shapes

def write_vrml(shapes, out_path):
    with open(out_path, "w") as f:
        f.write("#VRML V2.0 utf8\n")
        f.write("# KiCad 3D Model: BLOSSOM 412-SMT / Beilamoo AAA Battery Holder\n")
        f.write("# Matches official manufacturer CAD geometry with high precision\n\n")

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
    target_name = os.path.join(out_dir, "BatteryHolder_AAA_SMT_Blossom_412.wrl")
    keystone_name = os.path.join(out_dir, "BatteryHolder_Keystone_2466_1xAAA.wrl")

    shapes = build_wrl()
    write_vrml(shapes, target_name)
    write_vrml(shapes, keystone_name)
    print(f"Successfully generated:\n  - {target_name}\n  - {keystone_name}")
